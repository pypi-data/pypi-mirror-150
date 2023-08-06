import os
import signal
import time

import azureml.contrib.services.aml_request as aml_request
from werkzeug.exceptions import HTTPException
from werkzeug.http import parse_options_header
from flask import request, g, Response

# Get (hopefully useful, but at least obvious) output from segfaults, etc.
import faulthandler

faulthandler.enable()

try:
    import spark_preamble
except ImportError:
    pass

try:
    # Workaround to ensure that MDC is imported before other modules

    # When sklern Ridge (and probably other libraries) are imported before MDC
    # MDC can't connect to storage. That doesn't happen if MDC is imported first.

    # We still don't have a root cause for this, so this is a workaround until we
    # can find a better solution
    # Bug: 494716
    from azureml.monitoring import ModelDataCollector
except ImportError:
    pass

import traceback
import json
import threading

from azureml.contrib.services.aml_request import AMLRequest
from azureml.contrib.services.aml_response import AMLResponse

from run_function_exception import RunFunctionException
from timeout_exception import TimeoutException

from create_app import app


user_main = app.user_main


class Watchdog(BaseException):
    def __init__(self, timeout, userHandler=None):  # timeout in seconds
        self.timeout = timeout
        self.handler = userHandler if userHandler is not None else self.defaultHandler
        self.timer = threading.Timer(self.timeout, self.handler)
        self.timer.start()

    def reset(self):
        self.timer.cancel()
        self.timer = threading.Timer(self.timeout, self.handler)
        self.timer.start()

    def stop(self):
        self.timer.cancel()

    def defaultHandler(self):
        raise self


def get_service_input_from_url(g, request, is_raw):
    g.apiName = "/score"

    if is_raw:
        service_input = request
        service_input.__class__ = AMLRequest  # upcast
    else:
        # Some Notes:
        #   - Request arg keys are case-sensitive(RFC 3986)
        #   - If there are repeated arg in the url, its values will be put as an array in the request body
        #
        # For example:
        #   - GET http://127.0.0.1:31311/score?foo=bar1&Foo=bar2&x=y
        #     * run() will receive
        #         {
        #             "Foo": "bar2",
        #             "foo": "bar1",
        #             "x": "y"
        #         }
        #   - GET http://127.0.0.1:31311/score?foo=bar1&foo=bar2&x=y
        #     * run() will receive
        #         {
        #             "x": "y",
        #             "foo": [
        #                 "bar1",
        #                 "bar2"
        #             ]
        #         }

        aml_input = {}
        for k in request.args.keys():
            values = request.args.getlist(k)
            if len(values) == 1:
                aml_input[k] = json.loads(values[0]) if is_json(values[0]) else values[0]
            else:
                value_list = []
                for v in values:
                    value_list.append(json.loads(v) if is_json(v) else v)

                aml_input[k] = value_list
        if app.request_is_parsed_json:
            service_input = aml_input
        else:
            service_input = json.dumps(aml_input)

    return service_input


def wrap_response(response):
    response_headers = {}
    response_body = response
    response_status_code = 200

    if isinstance(response, dict):
        if "aml_response_headers" in response:
            app.logger.info("aml_response_headers are available from run() output")
            response_body = None
            response_headers = response["aml_response_headers"]

        if "aml_response_body" in response:
            app.logger.info("aml_response_body is available from run() output")
            response_body = response["aml_response_body"]

    return AMLResponse(response_body, response_status_code, response_headers, json_str=True)


def prepare_user_params(service_input, headers, is_raw):
    if is_raw:
        params = {app.run_input_parameter_name: service_input}
    elif app.request_is_parsed_json:
        if app.wrapped:
            params = {app.run_input_parameter_name: service_input[app.wrapped_parameter_name]}
        else:
            params = service_input.copy()
    else:
        params = {app.run_input_parameter_name: service_input}
    # Flask request.headers is not python dict but werkzeug.datastructures.EnvironHeaders which is not json serializable
    # Per RFC 2616 sec 4.2,
    # 1. HTTP headers are case-insensitive: https://www.w3.org/Protocols/rfc2616/rfc2616-sec4.html#sec4.2
    #    So if user scores with header ("foo": "bar") from client, but what we give run() function could be ("FOO": "bar")
    # 2. HTTP header key could be duplicate. In this case, request_headers[key] will be a list of values.
    #    Values are connected by ", ". For example a request contains "FOO": "bAr" and "foO": "raB",
    #    the request_headers["Foo"] = "bAr, raB".

    if app.support_request_header:
        params["request_headers"] = dict(headers)

    return params


def alarm_handler(signum, frame):
    error_message = "Scoring timeout after {} ms".format(app.scoring_timeout_in_ms)
    raise TimeoutException(error_message)


def is_json(input_string):
    try:
        json.loads(input_string)
    except ValueError:
        return False
    return True


@app.route("/swagger.json", methods=["GET"])
def get_swagger_specification():
    version = request.args.get("version")
    g.apiName = "/swagger.json"

    # Setting default version where no query parameters passed
    if version == None:
        version = "2"

    # If the version is not 2 or 3 or None (for default), it is not supported
    if version and version != "3" and version != "2":
        app.logger.info(
            f"Swagger version {version} requested from url query string is not supported. Supported versions: 2, 3."
        )
        return AMLResponse(
            f"Swagger version {version} requested from url query string is not supported. Supported versions: 2, 3",
            404,
            json_str=True,
        )

    # If the version is 3 we return the OpenAPI3 spec
    if version == "3" and app.swagger3:
        return AMLResponse(app.swagger3, 200, json_str=True)
    # If the version is unspecified or 2, we return the Swagger 2 spec
    elif version == "2" and app.swagger2:
        return AMLResponse(app.swagger2, 200, json_str=True)
    else:
        if not app.gen_swagger:
            app.logger.info("No decorators provided or failed to parse. Swagger file not generated.")
            return AMLResponse("Swagger not found. No decorators provided or failed to parse.", 404, json_str=True)
        app.logger.info(f"Swagger version {version} not supported for this scenario. Swagger not found.")
        return AMLResponse(
            f"Swagger version {version} not supported for this scenario. Swagger file not found.", 404, json_str=True
        )


# Health probe endpoint
@app.route("/", methods=["GET"])
def health_probe():
    return "Healthy"


# Errors from User Run Function
@app.errorhandler(RunFunctionException)
def handle_run_exception(error):
    app.logger.debug("Run function exception caught")
    app.stop_hooks()
    app.logger.error("Encountered Exception: {0}".format(traceback.format_exc()))
    return AMLResponse(error.message, error.status_code, json_str=False, run_function_failed=True)


# Errors of Scoring Timeout
@app.errorhandler(TimeoutException)
def handle_timeout_exception(error):
    app.logger.debug("Run function timeout caught")
    app.stop_hooks()
    app.logger.error("Encountered Exception: {0}".format(traceback.format_exc()))
    return AMLResponse(error.message, error.status_code, json_str=False, run_function_failed=True)


# Errors from Server Side
@app.errorhandler(HTTPException)
def handle_http_exception(ex: HTTPException):
    if 400 <= ex.code < 500:
        app.logger.debug("Client request exception caught")
    elif 500 <= ex.code < 600:
        app.logger.debug("Server side exception caught")
    else:
        app.logger.debug("Caught an HTTP exception")

    app.stop_hooks()
    app.logger.error("Encountered Exception: {0}".format(traceback.format_exc()))
    return AMLResponse(ex.get_description(), ex.code, json_str=False)


# Unhandled Error
# catch all unhandled exceptions here and return the stack encountered in the response body
@app.errorhandler(Exception)
def all_unhandled_exception(error):
    app.stop_hooks()
    app.logger.debug("Unhandled exception generated")
    error_message = "Encountered Exception: {0}".format(traceback.format_exc())
    app.logger.error(error_message)
    internal_error = "An unexpected internal error occurred. {0}".format(error_message)
    return AMLResponse(internal_error, 500, json_str=False)


# log all response status code after request is done
@app.after_request
def after_request(response):
    if getattr(g, "apiName", None):
        app.logger.info(response.status_code)
    return response


@app.route("/score", methods=["GET"], provide_automatic_options=False)
def get_prediction_realtime():
    service_input = get_service_input_from_url(g, request, aml_request._rawHttpRequested)

    # run the user-provided run function
    return run_scoring(
        service_input,
        request.headers,
        request.environ.get("REQUEST_ID", "00000000-0000-0000-0000-000000000000"),
        request.environ.get("CLIENT_REQUEST_ID", ""),
    )


@app.route("/score", methods=["POST"], provide_automatic_options=False)
def score_realtime():
    g.apiName = "/score"

    if aml_request._rawHttpRequested:
        service_input = request
        service_input.__class__ = AMLRequest  # upcast
    else:
        if app.request_is_parsed_json:
            # enforce content-type json as either the sdk or the user code is expected to json deserialize this
            app.logger.info("Validation Request Content-Type")
            if (
                "Content-Type" not in request.headers
                or parse_options_header(request.headers["Content-Type"])[0] != "application/json"
            ):
                return AMLResponse({"message": "Expects Content-Type to be application/json"}, 415, json_str=True)

            service_input = request.get_json()
        else:
            # expect the response to be utf-8 encodeable
            service_input = request.data.decode("utf-8")

    # run the user-provided run function
    return run_scoring(
        service_input,
        request.headers,
        request.environ.get("REQUEST_ID", "00000000-0000-0000-0000-000000000000"),
        request.environ.get("CLIENT_REQUEST_ID", ""),
    )


@app.route("/score", methods=["OPTIONS"], provide_automatic_options=False)
def score_options_realtime():
    g.apiName = "/score"

    if aml_request._rawHttpRequested:
        service_input = request
        service_input.__class__ = AMLRequest  # upcast
    else:
        return AMLResponse("Method not allowed", 405, json_str=True)

    # run the user-provided run function
    return run_scoring(
        service_input,
        request.headers,
        request.environ.get("REQUEST_ID", "00000000-0000-0000-0000-000000000000"),
        request.environ.get("CLIENT_REQUEST_ID", ""),
    )


def run_scoring(service_input, request_headers, request_id=None, client_request_id=""):

    # If x-request-id and x-ms-request-id header values are differenet then it is a bad request
    if request.environ.get("LEGACY_REQUEST_ID") != request.environ.get("REQUEST_ID"):
        return AMLResponse(
            {
                "message": "x-request-id and x-ms-request-id header value should be same (if you are sending both in the request)"
            },
            400,
            json_str=True,
        )

    app.start_hooks(request_id, client_request_id)

    try:
        response, time_taken_ms = invoke_user_with_timer(service_input, request_headers)
        app.appinsights_client.send_model_data_log(request_id, client_request_id, service_input, response)
    except TimeoutException:
        app.stop_hooks()
        app.send_exception_to_app_insights(request_id, client_request_id)
        raise
    except Exception as exc:
        app.stop_hooks()
        app.send_exception_to_app_insights(request_id, client_request_id)
        raise RunFunctionException(str(exc))
    finally:
        app.stop_hooks()

    if isinstance(response, Response):  # this covers both AMLResponse and flask.Response
        app.logger.info("run() output is HTTP Response")
    else:
        response = wrap_response(response)

    # we're formatting time_taken_ms explicitly to get '0.012' and not '1.2e-2'
    response.headers.add("x-ms-run-fn-exec-ms", f"{time_taken_ms:.3f}")
    return response


def capture_time_taken(func):
    """Captures time taken in milliseconds to run a function."""

    def timer(*args, **kwargs):
        t1 = time.perf_counter()
        result = func(*args, **kwargs)
        t2 = time.perf_counter()
        time_taken = t2 - t1
        # convert to milliseconds
        time_taken *= 1000
        return result, time_taken

    return timer


def invoke_user_with_timer(service_input, headers):
    params = prepare_user_params(service_input, headers, aml_request._rawHttpRequested)

    # Signals can only be used in the main thread.
    if os.name != "nt" and threading.current_thread() is threading.main_thread():
        old_handler = signal.signal(signal.SIGALRM, alarm_handler)
        signal.setitimer(signal.ITIMER_REAL, app.scoring_timeout_in_ms / 1000)
        app.logger.info("Scoring Timer is set to {} seconds".format(app.scoring_timeout_in_ms / 1000))

        result, time_taken_ms = capture_time_taken(user_main.run)(**params)

        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, old_handler)

    else:
        watchdog = Watchdog(app.scoring_timeout_in_ms / 1000)

        try:
            result, time_taken_ms = capture_time_taken(user_main.run)(**params)
        except Watchdog:
            error_message = "Scoring timeout after {} ms".format(app.scoring_timeout_in_ms)
            raise TimeoutException(error_message)
        finally:
            watchdog.stop()

    return result, time_taken_ms
