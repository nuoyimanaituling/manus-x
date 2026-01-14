from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import Any
from app.schemas.response import Response
import logging

# Get logger
logger = logging.getLogger(__name__)

# Custom exception classes
class AppException(Exception):
    """Base application exception class"""
    def __init__(
        self, 
        message: str = "An error occurred", 
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        data: Any = None
    ):
        self.message = message
        self.status_code = status_code
        self.data = data
        logger.error("AppException: %s (code: %d)", message, status_code)
        super().__init__(self.message)

class ResourceNotFoundException(AppException):
    """Resource not found exception"""
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)

class BadRequestException(AppException):
    """Bad request exception"""
    def __init__(self, message: str = "Bad request"):
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST)

class UnauthorizedException(AppException):
    """Unauthorized exception"""
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message=message, status_code=status.HTTP_401_UNAUTHORIZED)

# Exception handlers
async def app_exception_handler(request: Request, exc: AppException):
    """Handle application custom exceptions"""
    logger.error("Processing application exception: %s", exc.message)
    response = Response.error(
        message=exc.message,
        data=exc.data
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump()
    )

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions"""
    logger.error("Processing HTTP exception: %s (code: %d)", exc.detail, exc.status_code)
    response = Response.error(
        message=str(exc.detail)
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump()
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation exceptions"""
    errors = exc.errors()
    error_messages = []
    for error in errors:
        error_messages.append({
            "loc": error.get("loc", []),
            "msg": error.get("msg", ""),
            "type": error.get("type", "")
        })
    
    logger.error("Validation error: %s", error_messages)
    response = Response.error(
        message="Request data validation failed",
        data=error_messages
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=response.model_dump()
    )

async def general_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions"""
    error_message = f"Internal server error: {str(exc)}"
    logger.error("Unhandled exception: %s", error_message, exc_info=True)
    response = Response.error(
        message=error_message
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response.model_dump()
    ) 