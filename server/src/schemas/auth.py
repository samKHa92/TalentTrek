from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# Simplified user schemas for local database only
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Token schema for API responses
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # minutes

# User report schemas (still needed for our app functionality)
class UserReportBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    report_type: str = Field(..., pattern="^(scrape|analysis|trends)$")

class UserReportCreate(UserReportBase):
    report_data: str  # JSON string

class UserReportResponse(UserReportBase):
    id: int
    user_id: int
    created_at: datetime
    report_data: str

    class Config:
        from_attributes = True 