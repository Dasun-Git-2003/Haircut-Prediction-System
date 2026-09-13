from fastapi import HTTPException, status, Request
from fastapi.responses import JSONResponse

class AppError(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class NotFoundError(AppError):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class UnauthorizedError(AppError):
    def __init__(self, detail: str = "Not authenticated"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class ForbiddenError(AppError):
    def __init__(self, detail: str = "Not enough permissions"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class ImageValidationError(AppError):
    def __init__(self, detail: str = "Invalid image"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class AIProviderError(AppError):
    def __init__(self, detail: str = "AI Provider Error"):
        super().__init__(status_code=status.HTTP_502_BAD_GATEWAY, detail=detail)

async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

exception_handlers = {
    AppError: app_error_handler,
    NotFoundError: app_error_handler,
    UnauthorizedError: app_error_handler,
    ForbiddenError: app_error_handler,
    ImageValidationError: app_error_handler,
    AIProviderError: app_error_handler
}
