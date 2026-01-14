from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
import sys

from app.core.config import settings
from app.api.router import api_router
from app.core.exceptions import (
    AppException, 
    app_exception_handler, 
    http_exception_handler, 
    validation_exception_handler,
    general_exception_handler
)
from app.core.middleware import auto_extend_timeout_middleware

# Configure logging
def setup_logging():
    """
    Set up the application logging system
    
    Configures log level, format, and handlers based on application settings.
    Outputs logs to stdout for container compatibility.
    """
    log_level = getattr(logging, settings.LOG_LEVEL)
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    # Get root logger
    root_logger = logging.getLogger()
    
    # Set root log level
    log_level = getattr(logging, settings.LOG_LEVEL)
    root_logger.setLevel(log_level)
    
    # Log setup completion
    logging.info("Sandbox logging system initialized with level: %s", settings.LOG_LEVEL)

# Initialize logging
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    version="1.0.0",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("Sandbox API server starting")

# Register middleware
app.middleware("http")(auto_extend_timeout_middleware)

# Register exception handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Register routes
app.include_router(api_router, prefix="/api/v1")

logger.info("Sandbox API routes registered and server ready")