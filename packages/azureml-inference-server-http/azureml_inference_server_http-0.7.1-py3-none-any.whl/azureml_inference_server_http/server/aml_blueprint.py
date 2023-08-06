import inspect
import json
import logging
import os
import sys
import tempfile
import time
import traceback

from aml_logger import AMLLogger
from appinsights_client import AppInsightsClient
from flask import Flask
from print_hook import PrintHook

from middleware_headers import WSGIRequest as HeadersWrapper
from middleware_appinsights import WSGIWrapper as AppInsightsWrapper
from middleware_debuggability import init_debuggability


AML_APP_ROOT = os.environ.get("AML_APP_ROOT", "/var/azureml-app")
AML_SERVER_ROOT = os.environ.get("AML_SERVER_ROOT", os.path.dirname(os.path.realpath(__file__)))
AML_ENTRY_SCRIPT = os.environ.get("AZUREML_ENTRY_SCRIPT")
AML_SOURCE_DIR = os.environ.get("AZUREML_SOURCE_DIRECTORY")

# Amount of time we wait before exiting the application when errors occur for exception log sending
WAIT_EXCEPTION_UPLOAD_IN_SECONDS = 30
SCORING_TIMEOUT_ENV_VARIABLE = "SCORING_TIMEOUT_MS"

sys.path.append(AML_APP_ROOT)

if AML_SOURCE_DIR:
    source_dir = os.path.join(AML_APP_ROOT, AML_SOURCE_DIR)
    sys.path.append(source_dir)

if AML_ENTRY_SCRIPT:
    import importlib.util as imp

    script_location = os.path.join(AML_APP_ROOT, AML_ENTRY_SCRIPT.replace("/", os.sep))
    main_module_spec = imp.spec_from_file_location("entry_module", script_location)
    main = imp.module_from_spec(main_module_spec)
    main_module_spec.loader.exec_module(main)
else:
    try:
        import main
    except:

        # Errors here indicate there are issues within the score script while trying to load script
        print(f"Encountered exception while trying to load score script: {traceback.format_exc()}")

        # If main is not found, this indicates score script is not in expected location
        if "No module named 'main'" in traceback.format_exc():
            print("No score script found. Expected score script main.py.")
            print(f"Expected script to be found in PYTHONPATH: {sys.path}")
            if os.path.isdir(AML_APP_ROOT):
                print(f"Current contents of AML_APP_ROOT: {os.listdir(AML_APP_ROOT)}")
            else:
                print(f"The directory {AML_APP_ROOT} not an accessible directory in the container.")

        sys.exit(3)


class AMLInferenceApp(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.appinsights_client = None
        self.appinsights_enabled = None
        self.gen_swagger = False
        self.swagger2 = False
        self.swagger3 = False
        self.swagger2_spec_path = os.path.join(AML_APP_ROOT, "swagger2.json")
        self.swagger3_spec_path = os.path.join(AML_APP_ROOT, "swagger3.json")
        self.support_request_header = False
        self.run_input_parameter_name = "input"
        self.request_is_parsed_json = False
        self.wrapped = False
        self.wrapped_parameter_name = None
        self.scoring_timeout_in_ms = 3600 * 1000
        self.logger = None
        self.user_main = main

        self._stdout_hook = None
        self._stderr_hook = None

    # init wrapper that handles request id and server version generation
    def _init_headers_generator(self):
        try:
            self.logger.info("Starting up request id generator")
            self.wsgi_app = HeadersWrapper(self.wsgi_app)
        except:
            self.logger.error(
                "Encountered exception while starting up request_id generator: {0}".format(traceback.format_exc())
            )
            sys.exit(3)

    def _init_logger(self):
        try:
            print("Initializing logger")
            self.logger = AMLLogger()

            logging.getLogger("gunicorn.access").addFilter(lambda record: "GET / HTTP/1." not in record.getMessage())
        except:
            print("logger initialization failed: {0}".format(traceback.format_exc()))
            sys.exit(3)

    def _gen_swagger_json(self, wrapped, swagger_version, get_input_schema, get_output_schema):
        service_name = os.getenv("SERVICE_NAME", "ML service")
        service_path_prefix = os.getenv("SERVICE_PATH_PREFIX", "")
        service_version = os.getenv("SERVICE_VERSION", "1.0")

        if swagger_version == "3":
            template_file = "swagger3_template.json"
        else:
            template_file = "swagger2_template.json"

        with open(os.path.join(AML_SERVER_ROOT, template_file), "r") as f:
            swagger_spec_str = f.read()

        if service_path_prefix and not service_path_prefix.startswith("/"):
            service_path_prefix = "/{}".format(service_path_prefix)
        service_path_prefix = service_path_prefix.rstrip("/")

        swagger_spec_str = (
            swagger_spec_str.replace("$SERVICE_NAME$", service_name)
            .replace("$SERVICE_VERSION$", service_version)
            .replace("$PATH_PREFIX$", service_path_prefix)
        )

        swagger_spec_json = json.loads(swagger_spec_str)

        input_schema = get_input_schema(main.run) if not wrapped else get_input_schema(main.driver_module.run)
        output_schema = get_output_schema(main.run) if not wrapped else get_output_schema(main.driver_module.run)

        if swagger_version == "3":
            swagger_spec_json["components"]["schemas"]["ServiceInput"] = input_schema
            swagger_spec_json["components"]["schemas"]["ServiceOutput"] = output_schema
        else:
            swagger_spec_json["definitions"]["ServiceInput"] = input_schema
            swagger_spec_json["definitions"]["ServiceOutput"] = output_schema

        # Write the swagger json to a temporary file for futher reference.
        # Write to a file in AML_APP_ROOT can fail, if AML_APP_ROOT is read-only.
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as swagger_file:
            print(f"Generating swagger file for version {swagger_version}: {swagger_file.name}")

            if swagger_version == "3":
                self.swagger3_spec_path = swagger_file.name
            else:
                self.swagger2_spec_path = swagger_file.name
            json.dump(swagger_spec_json, swagger_file, indent=4)

        return swagger_spec_json

    def _get_swagger(self, swagger_version):
        try:
            from inference_schema.schema_util import (
                get_input_schema,
                get_output_schema,
                is_schema_decorated,
                get_supported_versions,
            )

            gen_swagger = False
            wrapped = False
            func_to_check = None
            if is_schema_decorated(main.run):
                gen_swagger = True
                func_to_check = main.run
            elif hasattr(main, "driver_module") and is_schema_decorated(main.driver_module.run):
                gen_swagger = True
                wrapped = True
                func_to_check = main.driver_module.run
            self.gen_swagger = gen_swagger
            # If request swagger version not supported, this will remain None
            if gen_swagger and any(item.startswith(swagger_version) for item in get_supported_versions(func_to_check)):
                return self._gen_swagger_json(
                    wrapped,
                    swagger_version=swagger_version,
                    get_input_schema=get_input_schema,
                    get_output_schema=get_output_schema,
                )

        except:
            self.logger.error(
                "Encountered exception while generating swagger file: {0}".format(traceback.format_exc())
            )

        if swagger_version == "3":
            swagger_load_path = self.swagger3_spec_path
        else:
            swagger_load_path = self.swagger2_spec_path

        if os.path.exists(swagger_load_path):
            print(f"Found swagger file for version {swagger_version}: {swagger_load_path}")
            with open(swagger_load_path, "r") as file:
                data = json.load(file)
                print("Swagger file loaded.")
                return data

        return None

    # AML App Insights Wrapper
    def _init_appinsights(self):
        try:
            self.logger.info("Starting up app insights client")
            self.appinsights_client = AppInsightsClient()
            self.wsgi_app = AppInsightsWrapper(self.wsgi_app, self.appinsights_client)
            self._stdout_hook = PrintHook(PrintHook.stdout_fd)
            self._stderr_hook = PrintHook(PrintHook.stderr_fd)
        except:
            self.logger.error(
                "Encountered exception while initializing App Insights/Logger {0}".format(traceback.format_exc())
            )
            sys.exit(3)

    def send_exception_to_app_insights(self, request_id="NoRequestId", client_request_id=""):
        if self.appinsights_client is not None:
            self.appinsights_client.send_exception_log(sys.exc_info(), request_id, client_request_id)

    # The default prefix of zeros acts as default request id
    def start_hooks(self, prefix="00000000-0000-0000-0000-000000000000", client_request_id=""):
        try:
            if self._stdout_hook is not None:
                self._stdout_hook.start_hook(prefix, client_request_id)
            if self._stderr_hook is not None:
                self._stderr_hook.start_hook(prefix, client_request_id)
        except:
            pass

    def stop_hooks(self):
        try:
            if self._stdout_hook is not None:
                self._stdout_hook.stop_hook()
            if self._stderr_hook is not None:
                self._stderr_hook.stop_hook()
        except:
            pass

    def setup(self):
        # initiliaze request generator, logger and app insights
        self._init_logger()
        self._init_appinsights()
        self._init_headers_generator()

        # start the hooks to listen to init print events
        try:
            self.logger.info("Starting up app insight hooks")
            self.start_hooks()
        except:
            self.logger.error("Starting up app insight hooks failed")
            if self.appinsights_client is not None:
                self.appinsights_client.send_exception_log(sys.exc_info())
                self.logger.info("Waiting for logs to be sent to Application Insights before exit.")
                self.logger.info("Waiting %d seconds for upload." % (WAIT_EXCEPTION_UPLOAD_IN_SECONDS))
                time.sleep(WAIT_EXCEPTION_UPLOAD_IN_SECONDS)
            sys.exit(3)

        # actually get init started
        try:
            self.logger.info("Invoking user's init function")
            main.init()
            self.logger.info("Users's init has completed successfully")
        except:
            self.logger.error("User's init function failed")
            self.logger.error("Encountered Exception {0}".format(traceback.format_exc()))
            if self.appinsights_client is not None:
                self.appinsights_client.send_exception_log(sys.exc_info())
                self.logger.info("Waiting for logs to be sent to Application Insights before exit.")
                self.logger.info("Waiting %d seconds for upload." % (WAIT_EXCEPTION_UPLOAD_IN_SECONDS))
                time.sleep(WAIT_EXCEPTION_UPLOAD_IN_SECONDS)
            sys.exit(3)
        finally:
            self.stop_hooks()

        # init debug middlewares after user init to make env var set in user init take effect
        init_debuggability(self.logger, self)

        # set has_swagger value
        self.swagger3 = self._get_swagger(swagger_version="3")
        self.swagger2 = self._get_swagger(swagger_version="2")

        # check if run() support handling request header
        run_args = inspect.signature(main.run).parameters.keys()
        run_args_list = list(run_args)

        try:
            from inference_schema.schema_util import is_schema_decorated

            # check if user run has schema decorators
            if is_schema_decorated(main.run):
                self.request_is_parsed_json = True
            # check if main was actually wrapped by the sdk, and see if the wrapped module is
            # schema decorated
            elif hasattr(main, "driver_module") and is_schema_decorated(main.driver_module.run):
                self.request_is_parsed_json = True
                self.wrapped = True
                wrapped_run_args = inspect.signature(main.driver_module.run).parameters.keys()
                wrapped_run_args_list = list(wrapped_run_args)
                self.wrapped_parameter_name = (
                    wrapped_run_args_list[0]
                    if wrapped_run_args_list[0] != "request_headers"
                    else wrapped_run_args_list[1]
                )
        except:
            pass

        if not self.request_is_parsed_json and len(run_args) > 2:
            self.logger.error("run() has too many parameters")
            sys.exit(3)

        if len(run_args) == 0:
            raise TypeError("run() has zero parameters, but needs to have at least one")
        elif len(run_args) == 1:
            self.support_request_header = False
            self.run_input_parameter_name = run_args_list[0]
        elif "request_headers" in run_args:
            self.support_request_header = True
            self.run_input_parameter_name = (
                run_args_list[0] if run_args_list[0] != "request_headers" else run_args_list[1]
            )

        if SCORING_TIMEOUT_ENV_VARIABLE in os.environ.keys() and self.is_int(os.environ[SCORING_TIMEOUT_ENV_VARIABLE]):
            self.scoring_timeout_in_ms = int(os.environ[SCORING_TIMEOUT_ENV_VARIABLE])
            self.logger.info("Scoring timeout is found from os.environ: {} ms".format(self.scoring_timeout_in_ms))
        else:
            self.logger.info(
                "Scoring timeout setting is not found. Use default timeout: {} ms".format(self.scoring_timeout_in_ms)
            )

    @staticmethod
    def is_int(value):
        try:
            int(value)
            return True
        except ValueError:
            return False
