"""Custom exceptions"""

from fastapi import HTTPException, status


class APIException(HTTPException):
    """Base API exception"""

    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        error_code: str = "ERROR",
        message: str = "An error occurred",
        details: list = None,
    ):
        self.error_code = error_code
        self.details = details or []
        detail = {
            "success": False,
            "error": {
                "code": error_code,
                "message": message,
                "details": self.details,
            }
        }
        super().__init__(status_code=status_code, detail=detail)


class ValidationError(APIException):
    """Validation error"""

    def __init__(self, message: str, details: list = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="VALIDATION_ERROR",
            message=message,
            details=details,
        )


class UnauthorizedError(APIException):
    """Unauthorized error"""

    def __init__(self, message: str = "Unauthorized"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="UNAUTHORIZED",
            message=message,
        )


class ForbiddenError(APIException):
    """Forbidden error"""

    def __init__(self, message: str = "Access forbidden"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="FORBIDDEN",
            message=message,
        )


class NotFoundError(APIException):
    """Not found error"""

    def __init__(self, resource: str = "Resource"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="NOT_FOUND",
            message=f"{resource} not found",
        )


class ConflictError(APIException):
    """Conflict error"""

    def __init__(self, message: str = "Resource already exists"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            error_code="CONFLICT",
            message=message,
        )


class RateLimitError(APIException):
    """Rate limit exceeded"""

    def __init__(self, message: str = "Too many requests"):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_code="RATE_LIMIT",
            message=message,
        )


class ServiceUnavailableError(APIException):
    """Service unavailable"""

    def __init__(self, service: str = "Service"):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error_code="SERVICE_UNAVAILABLE",
            message=f"{service} is temporarily unavailable",
        )
