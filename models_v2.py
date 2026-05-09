"""
Enhanced Pydantic models for VisionStack API
Includes Projects, Team Management, and Advanced Reviews
"""
from pydantic import BaseModel, EmailStr, Field, HttpUrl
from typing import Optional, List
from datetime import datetime
from enum import Enum

# ========================
# AUTH MODELS (Existing - Keep as is)
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

class UserResponse(BaseModel):
    id: Optional[str] = None
    first_name: str
    last_name: str
    email: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# ========================
# PROJECT MODELS (NEW)
# ========================

class ProjectPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class ProjectCategory(str, Enum):
    WEB_APP = "web_app"
    MOBILE_APP = "mobile_app"
    ECOMMERCE = "ecommerce"
    SAAS = "saas"
    STARTUP = "startup"
    ENTERPRISE = "enterprise"
    OTHER = "other"

class ProjectStatus(str, Enum):
    PENDING = "pending"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class ProjectCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., min_length=20)
    budget: float = Field(..., gt=0)
    deadline: datetime
    tech_stack: List[str]
    category: ProjectCategory
    priority: ProjectPriority
    additional_notes: Optional[str] = None

class ProjectResponse(BaseModel):
    id: Optional[str] = None
    user_email: str
    user_id: Optional[str] = None
    title: str
    description: str
    budget: float
    deadline: datetime
    tech_stack: List[str]
    category: str
    priority: str
    status: ProjectStatus = ProjectStatus.PENDING
    file_urls: List[str] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    admin_notes: Optional[str] = None

# ========================
# TEAM MODELS (NEW)
# ========================

class TeamMemberCreate(BaseModel):
    name: str = Field(..., min_length=3)
    role: str = Field(..., min_length=3)
    email: EmailStr
    phone: str = Field(..., min_length=10)
    bio: str = Field(..., min_length=20)
    skills: List[str]
    photo_url: Optional[str] = None
    social_links: Optional[dict] = None

class TeamMemberResponse(BaseModel):
    id: Optional[str] = None
    name: str
    role: str
    email: str
    phone: str
    bio: str
    skills: List[str]
    photo_url: Optional[str] = None
    social_links: Optional[dict] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# ========================
# ADVANCED REVIEW MODELS (NEW)
# ========================

class ReviewCreate(BaseModel):
    author_name: str = Field(..., min_length=3)
    author_email: EmailStr
    text: str = Field(..., min_length=20)
    rating: int = Field(..., ge=1, le=5)
    image_urls: Optional[List[str]] = []
    video_urls: Optional[List[str]] = []

class ReviewResponse(BaseModel):
    id: Optional[str] = None
    author_name: str
    author_email: str
    text: str
    rating: int
    image_urls: Optional[List[str]] = []
    video_urls: Optional[List[str]] = []
    approved: bool = False
    created_at: Optional[datetime] = None
    approved_at: Optional[datetime] = None

# ========================
# FEEDBACK MODELS (Existing)
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
# CONTACT MODELS (Existing)
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

# ========================
# NEWSLETTER MODELS (Existing)
# ========================

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

# ========================
# ADMIN MODELS (NEW)
# ========================

class DashboardStats(BaseModel):
    total_users: int
    total_projects: int
    pending_projects: int
    completed_projects: int
    total_reviews: int
    pending_reviews: int
    total_team_members: int
    recent_projects: List[dict]
    recent_reviews: List[dict]

class AdminApproval(BaseModel):
    status: str  # approved, rejected
    notes: Optional[str] = None
