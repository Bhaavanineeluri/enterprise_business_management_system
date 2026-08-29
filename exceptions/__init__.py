class BusinessException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = 400,
        error_code: str = "BUSINESS_ERROR",
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code

        super().__init__(self.message)


class ResourceNotFoundException(BusinessException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(
            message=message,
            status_code=404,
            error_code="RESOURCE_NOT_FOUND",
        )


class ResourceAlreadyExistsException(BusinessException):
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(
            message=message,
            status_code=409,
            error_code="RESOURCE_ALREADY_EXISTS",
        )


class PermissionDeniedException(BusinessException):
    def __init__(self, message: str = "Permission denied"):
        super().__init__(
            message=message,
            status_code=403,
            error_code="PERMISSION_DENIED",
        )
