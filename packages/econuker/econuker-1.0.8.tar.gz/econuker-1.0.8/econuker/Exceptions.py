class EconukerException(Exception):
    """
    Exception raised for other EcoNuker-API exceptions, that don't fall under defined exceptions.

    Also the base exception class.
    """
    pass


class Forbidden(EconukerException):
    """
    Exception raised when there is insufficient token authentication level to perform a certain operation.
    """
    pass


class Unauthorized(EconukerException):
    """
    Exception raised when the request lacks valid authentication credentials.
    """
    pass


class NotFound(EconukerException):
    """
    Exception raised when a requested resource is not found.
    """
    pass


class InternalServerError(EconukerException):
    """
    Exception raised when the server encounters an internal error.
    """
    pass


class RateLimited(EconukerException):
    """
    Exception raised when the rate limit for requests has been exceeded.
    """
    pass


class InvalidAuthToken(EconukerException):
    """
    Exception raised when an invalid authentication token is provided.
    """
    pass


# Additional aliases for convenience
EconukerForbidden = Forbidden
EconukerUnauthorized = Unauthorized
EconukerNotFound = NotFound
EconukerInternalServerError = InternalServerError
EconukerRateLimited = RateLimited
EconukerInvalidAuthToken = InvalidAuthToken