class ResponseTypes:
    PARAMETERS_ERROR = "ParametersError"
    RESOURCE_ERROR = "ResourceError"
    SYSTEM_ERROR = "SystemError"
    SUCCESS = "Success"
    NOT_FOUND = "NOT_FOUND"
    BAD_REQUEST = "BadRequest"
    INTERNAL_CONFIGURATION_ERROR = "SYSTEM_INTERNAL_CONFIGURATION_ERROR"

    def response_types(self):
        return {
            "parameter_failed": "ParametersError"
        }


class ResponseCodes:
    SUCCESS = 200
    PARAMETERS_ERROR = 400
    BAD_REQUEST = 400
    NOT_FOUND = 404
    SYSTEM_ERROR = 500
    SERVICE_UNAVAILABLE = 503
    SYSTEM_INTERNAL_CONFIGURATION_ERROR = 506


class ResponseFailure:
    def __init__(self, type_, message, status_code):
        self.type = type_
        self.message = self._format_message(message)
        self.status_code = status_code

    def _format_message(self, msg):
        if isinstance(msg, Exception):
            return "{}: {}".format(msg.__class__.__name__, "{}".format(msg))
        return msg

    @property
    def value(self):
        return {
            "response": {"error_type": self.type, "message": self.message},
            "status_code": self.status_code,
        }

    def __bool__(self):
        return False


class ResponseSuccess:
    def __init__(self, message=None, status_code=None):
        self.status_code = status_code or ResponseCodes.SUCCESS
        self.type = ResponseTypes.SUCCESS
        self.message = message

    @property
    def value(self):
        return {"response": self.message, "status_code": self.status_code}

    def __bool__(self):
        return True


def build_response_from_invalid_request(invalid_request):
    message = "\n".join(
        ["{}: {}".format(err["parameter"], err["message"]) for err in invalid_request.errors]
    )
    return ResponseFailure(ResponseTypes.PARAMETERS_ERROR, message, ResponseCodes.BAD_REQUEST)
