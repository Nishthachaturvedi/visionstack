"""
Pydantic models for VisionStack API
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

# ========================
# AUTH MODELS
# ========================

class UserRegister(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str = Field(min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenData(BaseModel):
    email: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str
    user: Optional[dict] = None

# ========================
# USER MODELS
# ========================

class UserResponse(BaseModel):
    id: Optional[str] = None
    first_name: str
    last_name: str
    email: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@example.com",
                "created_at": "2024-01-01T12:00:00",
                "updated_at": "2024-01-01T12:00:00"
            }
        }

# ========================
# PROJECT REQUEST MODELS
# ========================

class ProjectStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"

class ProjectRequest(BaseModel):
    title: str
    description: str
    budget: Optional[float] = None
    timeline: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    company: Optional[str] = None

class ProjectResponse(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    budget: Optional[float] = None
    timeline: Optional[str] = None
    email: str
    phone: Optional[str] = None
    company: Optional[str] = None
    status: ProjectStatus = ProjectStatus.PENDING
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# ========================
# FEEDBACK MODELS
# ========================

class Feedback(BaseModel):
    project_id: str
    user_email: str
    rating: int = Field(ge=1, le=5)
    message: str
    
class FeedbackResponse(BaseModel):
    id: Optional[str] = None
    project_id: str
    user_email: str
    rating: int
    message: str
    created_at: Optional[datetime] = None

# ========================
# REVIEW MODELS
# ========================

class Review(BaseModel):
    author_name: str
    author_email: str
    rating: int = Field(ge=1, le=5)
    title: str
    content: str
    approved: bool = False

class ReviewResponse(BaseModel):
    id: Optional[str] = None
    author_name: str
    author_email: str
    rating: int
    title: str
    content: str
    approved: bool
    created_at: Optional[datetime] = None

# ========================
# CONTACT & NEWSLETTER MODELS
# ========================

class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str

class ContactResponse(BaseModel):
    id: Optional[str] = None
    name: str
    email: str
    subject: str
    message: str
    status: str = "new"
    created_at: Optional[datetime] = None

class NewsletterSignup(BaseModel):
    email: EmailStr

class NewsletterResponse(BaseModel):
    id: Optional[str] = None
    email: str
    subscribed_at: Optional[datetime] = None

# ========================
# FILE UPLOAD MODELS
# ========================

class UploadedFileResponse(BaseModel):
    id: Optional[str] = None
    filename: str
    original_filename: str
    file_size: int
    file_type: str
    file_path: str
    uploader_email: str
    created_at: Optional[datetime] = None
