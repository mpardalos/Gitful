from flask import jsonify

from . import api


class ResponseException(Exception):
    status_code = 500
    message = "An unknown Exception occurred"

    def __init__(self, status_code=None, message=None):
        self.status_code = status_code or type(self).status_code
        self.message = message or type(self).message


@api.errorhandler(ResponseException)
def response_exception_handler(error):
    response = jsonify({
        "type": type(error).__name__,
        "message": error.message
    })
    response.status_code = error.status_code
    return response


class RepoNotFound(ResponseException):
    status_code = 404
    message = "The Repo you requested was not found"


class InvalidRequest(ResponseException):
    status_code = 400  # Bad Request
    message = "The request you made was not valid"
