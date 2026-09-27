"""Logging configuration"""

import logging
import sys
from app.core.config import settings

# Create logger
logger = logging.getLogger(__name__)

# Set log level based on environment
log_level = logging.DEBUG if settings.DEBUG else logging.INFO

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(log_level)

# Formatter
formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
console_handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(console_handler)
logger.setLevel(log_level)

# Disable uvicorn access logs in production
if not settings.DEBUG:
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


def get_logger(name: str = __name__) -> logging.Logger:
    """Get a logger instance"""
    return logging.getLogger(name)
