"""Standard response schemas"""

from pydantic import BaseModel
from typing import Any, Optional, List


class ErrorDetail(BaseModel):
    """Error detail schema"""
    code: str
    message: str
    details: Optional[List[str]] = None


class SuccessResponse(BaseModel):
    """Standard success response"""
    success: bool = True
    data: Any
    message: Optional[str] = None


class ErrorResponse(BaseModel):
    """Standard error response"""
    success: bool = False
    error: ErrorDetail


class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    database: str
    cache: Optional[str] = None
    vector_db: Optional[str] = None
