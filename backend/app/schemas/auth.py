"""
Authentication Schemas
Pydantic models for auth requests/responses
"""

from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    """Login request schema"""
    email: EmailStr
    password: str


class UserSignup(BaseModel):
    """Signup request schema"""
    email: EmailStr
    password: str
    full_name: str
    company: str | None = None


class Token(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """User info response"""
    id: int
    email: str
    full_name: str
    is_active: bool
    is_superuser: bool
    is_verified: bool
    
    class Config:
        from_attributes = True
