"""Authentication schemas"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class RegisterRequest(BaseModel):
    """User registration request"""
    email: EmailStr
    password: str = Field(..., min_length=8)
    password_confirm: str
    first_name: str
    last_name: str


class LoginRequest(BaseModel):
    """User login request"""
    email: EmailStr
    password: str
    otp_code: Optional[str] = Field(None, pattern=r"^\d{6}$")


class TokenResponse(BaseModel):
    """Token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RegisterResponse(BaseModel):
    """Registration outcome: either a sign-in (verification disabled) or a pending confirmation."""
    requires_verification: bool
    message: str
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: str = "bearer"


class VerifyEmailRequest(BaseModel):
    """Email verification request"""
    token: str


class PasswordResetRequest(BaseModel):
    """Password reset request"""
    email: EmailStr


class PasswordResetConfirmRequest(BaseModel):
    """Password reset confirmation"""
    token: str
    new_password: str = Field(..., min_length=8)
    password_confirm: str


class ChangePasswordRequest(BaseModel):
    """Change password request"""
    old_password: str
    new_password: str = Field(..., min_length=8)
    password_confirm: str


class UserResponse(BaseModel):
    """User response"""
    id: int
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[str] = None
    status: str
    email_verified_at: Optional[datetime] = None
    last_login_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
