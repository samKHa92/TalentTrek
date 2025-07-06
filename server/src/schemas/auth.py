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

# User report schemas (for job scraping reports)
class UserReportBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None

class UserReportCreate(UserReportBase):
    jobs_data: str  # JSON string of scraped jobs
    keyword: Optional[str] = None
    sources_used: Optional[str] = None  # JSON string of source IDs
    job_count: Optional[int] = 0

class UserReportResponse(UserReportBase):
    id: int
    user_id: int
    created_at: datetime
    jobs_data: str
    keyword: Optional[str] = None
    sources_used: Optional[str] = None
    job_count: Optional[int] = 0

    class Config:
        from_attributes = True 