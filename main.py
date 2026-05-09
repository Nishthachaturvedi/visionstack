"""
VisionStack Backend - FastAPI + MongoDB Atlas
Run: uvicorn main:app --reload
"""

from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from bson import ObjectId
import os
import uuid
# Import configuration and models
from config import settings
from routers import projects_router, team_router, reviews_router, admin_router
from models import (
    UserRegister, UserLogin, Token, TokenData, UserResponse,
    ProjectStatus, ProjectRequest, ProjectResponse,
    Feedback, FeedbackResponse,
    Review, ReviewResponse,
    ContactMessage, ContactResponse,
    NewsletterSignup, NewsletterResponse,
    UploadedFileResponse
)
from database import (
    Database,
    get_users_collection,
    get_admins_collection,
    get_projects_collection,
    get_feedbacks_collection,
    get_reviews_collection,
    get_files_collection,
    get_contacts_collection,
    get_newsletters_collection
)

# ========================
# APP SETUP
# ========================
app = FastAPI(
    title="VisionStack API",
    version="1.0.0",
    description="FastAPI Backend with MongoDB Atlas Integration"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# ========================
# SECURITY
# ========================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain, hashed)

def create_token(data: dict, expires_delta: timedelta = None) -> str:
    """Create JWT token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def serialize(doc) -> dict:
    """Convert MongoDB document to JSON-serializable dict"""
    if doc is None:
        return None
    doc["id"] = str(doc.pop("_id", ""))
    return doc

# ========================
# DEPENDENCIES
# ========================

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        role: str = payload.get("role", "user")
        if email is None:
            raise credentials_exception
        return {"email": email, "role": role}
    except JWTError:
        raise credentials_exception

async def require_admin(current_user=Depends(get_current_user)):
    """Require admin role"""
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

# ========================
# LIFESPAN EVENTS
# ========================

@app.on_event("startup")
async def startup():
    """Connect to MongoDB on startup"""
    await Database.connect_db()

@app.on_event("shutdown")
async def shutdown():
    """Close MongoDB connection on shutdown"""
    await Database.close_db()

# ========================
# ROUTES: AUTH
# ========================

@app.post("/api/auth/register", response_model=dict, tags=["Auth"])
async def register_user(data: UserRegister):
    """Register a new user"""
    users_col = get_users_collection()
    
    # Check if user exists
    existing = await users_col.find_one({"email": data.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user document
    user_doc = {
        "first_name": data.first_name,
        "last_name": data.last_name,
        "email": data.email,
        "password": hash_password(data.password),
        "role": "user",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "profile_complete": False,
    }
    
    result = await users_col.insert_one(user_doc)
    print("USER SAVED:", user_doc)
    
    # Create token
    token = create_token(
        {"sub": data.email, "role": "user"},
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": str(result.inserted_id)
    }

@app.post("/api/auth/login", response_model=Token, tags=["Auth"])
async def login_user(data: UserLogin):
    """Login user"""
    users_col = get_users_collection()
    
    user = await users_col.find_one({"email": data.email})
    if not user or not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = create_token(
        {"sub": data.email, "role": "user"},
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": str(user["_id"]),
            "name": f"{user['first_name']} {user['last_name']}",
            "email": user["email"]
        }
    }

@app.post("/api/auth/admin/register", response_model=dict, tags=["Auth"])
async def register_admin(email: str, password: str, admin_key: str):
    """Register admin user"""
    admins_col = get_admins_collection()
    
    ADMIN_SECRET = os.getenv("ADMIN_SECRET_KEY", "visionstack-admin-2025")
    if admin_key != ADMIN_SECRET:
        raise HTTPException(status_code=403, detail="Invalid admin registration key")
    
    existing = await admins_col.find_one({"email": email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    admin_doc = {
        "email": email,
        "password": hash_password(password),
        "role": "admin",
        "created_at": datetime.utcnow(),
    }
    
    result = await admins_col.insert_one(admin_doc)
    token = create_token(
        {"sub": email, "role": "admin"},
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "admin_id": str(result.inserted_id)
    }

@app.post("/api/auth/admin/login", response_model=Token, tags=["Auth"])
async def login_admin(data: UserLogin):
    """Login admin"""
    admins_col = get_admins_collection()
    
    admin = await admins_col.find_one({"email": data.email})
    if not admin or not verify_password(data.password, admin["password"]):
        raise HTTPException(status_code=401, detail="Invalid admin credentials")
    
    token = create_token(
        {"sub": data.email, "role": "admin"},
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"email": data.email, "role": "admin"}
    }

# ========================
# ROUTES: PROJECT REQUESTS
# ========================

@app.post("/api/projects/request", response_model=dict, tags=["Projects"])
async def submit_project_request(data: ProjectRequest):
    """Submit a new project request"""
    projects_col = get_projects_collection()
    
    doc = {
        **data.dict(),
        "status": ProjectStatus.PENDING,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "admin_notes": "",
    }
    
    result = await projects_col.insert_one(doc)
    
    return {
        "message": "Project request submitted successfully",
        "id": str(result.inserted_id)
    }

@app.get("/api/projects/my", response_model=list, tags=["Projects"])
async def get_my_projects(current_user=Depends(get_current_user)):
    """Get user's project requests"""
    projects_col = get_projects_collection()
    
    cursor = projects_col.find({"email": current_user["email"]}).sort("created_at", -1)
    docs = [serialize(d) async for d in cursor]
    return docs

@app.get("/api/projects/all", response_model=list, tags=["Admin"])
async def get_all_projects(admin=Depends(require_admin)):
    """Get all project requests (admin only)"""
    projects_col = get_projects_collection()
    
    cursor = projects_col.find({}).sort("created_at", -1)
    docs = [serialize(d) async for d in cursor]
    return docs

@app.put("/api/projects/{project_id}/status", tags=["Admin"])
async def update_project_status(
    project_id: str,
    status: ProjectStatus,
    message: str = "",
    admin=Depends(require_admin)
):
    """Update project status"""
    projects_col = get_projects_collection()
    
    result = await projects_col.update_one(
        {"_id": ObjectId(project_id)},
        {"$set": {
            "status": status,
            "admin_notes": message,
            "updated_at": datetime.utcnow()
        }}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {"message": "Status updated successfully"}

@app.delete("/api/projects/{project_id}", tags=["Admin"])
async def delete_project(project_id: str, admin=Depends(require_admin)):
    """Delete project request"""
    projects_col = get_projects_collection()
    
    await projects_col.delete_one({"_id": ObjectId(project_id)})
    return {"message": "Project deleted"}

# ========================
# ROUTES: FILE UPLOAD
# ========================

@app.post("/api/files/upload", response_model=dict, tags=["Files"])
async def upload_file(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user)
):
    """Upload a file"""
    files_col = get_files_collection()
    
    # Validate file type
    allowed_types = [
        "image/jpeg", "image/png", "image/webp", "image/gif",
        "application/pdf", "video/mp4", "video/webm"
    ]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="File type not allowed")
    
    # Validate file size (50MB max)
    MAX_SIZE = 50 * 1024 * 1024
    content = await file.read()
    if len(content) > MAX_SIZE:
        raise HTTPException(status_code=400, detail="File too large (max 50MB)")
    
    # Save file
    filename = f"{uuid.uuid4()}_{file.filename}"
    filepath = os.path.join(settings.UPLOAD_DIR, filename)
    
    with open(filepath, "wb") as f:
        f.write(content)
    
    # Save metadata to MongoDB
    doc = {
        "original_name": file.filename,
        "stored_name": filename,
        "content_type": file.content_type,
        "size": len(content),
        "uploaded_by": current_user["email"],
        "uploaded_at": datetime.utcnow(),
        "url": f"/uploads/{filename}",
    }
    
    result = await files_col.insert_one(doc)
    
    return {
        "url": f"/uploads/{filename}",
        "file_id": str(result.inserted_id)
    }

@app.get("/api/files/my", response_model=list, tags=["Files"])
async def get_my_files(current_user=Depends(get_current_user)):
    """Get user's uploaded files"""
    files_col = get_files_collection()
    
    cursor = files_col.find({"uploaded_by": current_user["email"]}).sort("uploaded_at", -1)
    docs = [serialize(d) async for d in cursor]
    return docs

# ========================
# ROUTES: FEEDBACK & REVIEWS
# ========================

@app.post("/api/feedback", response_model=dict, tags=["Feedback"])
async def submit_feedback(data: Feedback, current_user=Depends(get_current_user)):
    """Submit feedback"""
    feedbacks_col = get_feedbacks_collection()
    
    doc = {
        **data.dict(),
        "user_email": current_user["email"],
        "created_at": datetime.utcnow(),
    }
    
    result = await feedbacks_col.insert_one(doc)
    
    return {
        "message": "Feedback submitted successfully",
        "id": str(result.inserted_id)
    }

@app.post("/api/reviews", response_model=dict, tags=["Reviews"])
async def submit_review(data: Review):
    """Submit a review"""
    reviews_col = get_reviews_collection()
    
    doc = {
        **data.dict(),
        "approved": False,
        "created_at": datetime.utcnow(),
    }
    
    result = await reviews_col.insert_one(doc)
    
    return {
        "message": "Review submitted, pending approval",
        "id": str(result.inserted_id)
    }

@app.get("/api/reviews/approved", response_model=list, tags=["Reviews"])
async def get_approved_reviews():
    """Get approved reviews"""
    reviews_col = get_reviews_collection()
    
    cursor = reviews_col.find({"approved": True}).sort("created_at", -1)
    docs = [serialize(d) async for d in cursor]
    return docs

@app.put("/api/reviews/{review_id}/approve", tags=["Admin"])
async def approve_review(review_id: str, admin=Depends(require_admin)):
    """Approve a review"""
    reviews_col = get_reviews_collection()
    
    await reviews_col.update_one(
        {"_id": ObjectId(review_id)},
        {"$set": {"approved": True, "approved_at": datetime.utcnow()}}
    )
    
    return {"message": "Review approved"}

@app.delete("/api/reviews/{review_id}", tags=["Admin"])
async def delete_review(review_id: str, admin=Depends(require_admin)):
    """Delete a review"""
    reviews_col = get_reviews_collection()
    
    await reviews_col.delete_one({"_id": ObjectId(review_id)})
    return {"message": "Review deleted"}

# ========================
# ROUTES: CONTACT
# ========================

@app.post("/api/contact", response_model=dict, tags=["Contact"])
async def submit_contact(data: ContactMessage):
    """Submit contact message"""
    contacts_col = get_contacts_collection()
    
    doc = {
        **data.dict(),
        "status": "unread",
        "created_at": datetime.utcnow(),
    }
    
    await contacts_col.insert_one(doc)
    
    return {"message": "Message received. We'll respond within 24 hours."}

@app.get("/api/contact/all", response_model=list, tags=["Admin"])
async def get_all_contacts(admin=Depends(require_admin)):
    """Get all contact messages (admin only)"""
    contacts_col = get_contacts_collection()
    
    cursor = contacts_col.find({}).sort("created_at", -1)
    docs = [serialize(d) async for d in cursor]
    return docs

@app.put("/api/contact/{message_id}/mark-read", tags=["Admin"])
async def mark_contact_read(message_id: str, admin=Depends(require_admin)):
    """Mark contact message as read"""
    contacts_col = get_contacts_collection()
    
    await contacts_col.update_one(
        {"_id": ObjectId(message_id)},
        {"$set": {"status": "read"}}
    )
    
    return {"message": "Marked as read"}

# ========================
# ROUTES: NEWSLETTER
# ========================

@app.post("/api/newsletter/subscribe", response_model=dict, tags=["Newsletter"])
async def subscribe_newsletter(data: NewsletterSignup):
    """Subscribe to newsletter"""
    newsletters_col = get_newsletters_collection()
    
    existing = await newsletters_col.find_one({"email": data.email})
    if existing:
        return {"message": "Already subscribed"}
    
    await newsletters_col.insert_one({
        "email": data.email,
        "subscribed_at": datetime.utcnow()
    })
    
    return {"message": "Successfully subscribed to newsletter"}

@app.get("/api/newsletter/subscribers", tags=["Admin"])
async def get_newsletter_subscribers(admin=Depends(require_admin)):
    """Get all newsletter subscribers (admin only)"""
    newsletters_col = get_newsletters_collection()
    
    cursor = newsletters_col.find({}).sort("subscribed_at", -1)
    docs = [serialize(d) async for d in cursor]
    return docs

# ========================
# ROUTES: USER DASHBOARD
# ========================

@app.get("/api/user/profile", response_model=UserResponse, tags=["User"])
async def get_profile(current_user=Depends(get_current_user)):
    """Get user profile"""
    users_col = get_users_collection()
    
    user = await users_col.find_one({"email": current_user["email"]})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.pop("password", None)
    return serialize(user)

@app.put("/api/user/profile", tags=["User"])
async def update_profile(data: dict, current_user=Depends(get_current_user)):
    """Update user profile"""
    users_col = get_users_collection()
    
    # Don't allow password change here
    data.pop("password", None)
    data["updated_at"] = datetime.utcnow()
    
    await users_col.update_one(
        {"email": current_user["email"]},
        {"$set": data}
    )
    
    return {"message": "Profile updated successfully"}

# ========================
# ROUTES: ADMIN DASHBOARD
# ========================

@app.get("/api/admin/stats", tags=["Admin"])
async def get_admin_stats(admin=Depends(require_admin)):
    """Get admin dashboard statistics"""
    users_col = get_users_collection()
    projects_col = get_projects_collection()
    contacts_col = get_contacts_collection()
    reviews_col = get_reviews_collection()
    
    total_users = await users_col.count_documents({})
    total_projects = await projects_col.count_documents({})
    pending = await projects_col.count_documents({"status": ProjectStatus.PENDING})
    completed = await projects_col.count_documents({"status": ProjectStatus.COMPLETED})
    total_contacts = await contacts_col.count_documents({})
    pending_reviews = await reviews_col.count_documents({"approved": False})
    
    return {
        "total_users": total_users,
        "total_projects": total_projects,
        "pending_projects": pending,
        "completed_projects": completed,
        "total_contacts": total_contacts,
        "pending_reviews": pending_reviews,
    }

@app.get("/api/admin/users", response_model=list, tags=["Admin"])
async def get_all_users(admin=Depends(require_admin)):
    """Get all users (admin only)"""
    users_col = get_users_collection()
    
    cursor = users_col.find({}, {"password": 0}).sort("created_at", -1)
    docs = [serialize(d) async for d in cursor]
    return docs

@app.delete("/api/admin/users/{user_id}", tags=["Admin"])
async def delete_user(user_id: str, admin=Depends(require_admin)):
    """Delete user"""
    users_col = get_users_collection()
    
    await users_col.delete_one({"_id": ObjectId(user_id)})
    return {"message": "User deleted"}

@app.get("/api/admin/feedback", response_model=list, tags=["Admin"])
async def get_all_feedback(admin=Depends(require_admin)):
    """Get all feedback (admin only)"""
    feedbacks_col = get_feedbacks_collection()
    
    cursor = feedbacks_col.find({}).sort("created_at", -1)
    docs = [serialize(d) async for d in cursor]
    return docs

# ========================
# INCLUDE ROUTERS
# ========================

app.include_router(projects_router)
app.include_router(team_router)
app.include_router(reviews_router)
app.include_router(admin_router)

# ========================
# HEALTH CHECK
# ========================

@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint"""
    return {
        "status": "VisionStack API is running",
        "version": "1.0.0",
        "database": "MongoDB Atlas"
    }

@app.get("/api/health", tags=["Health"])
async def health():
    """Health check with timestamp"""
    try:
        # Verify database connection
        db = Database.get_db()
        await db.command("ping")
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow(),
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow(),
            "error": str(e)
        }
