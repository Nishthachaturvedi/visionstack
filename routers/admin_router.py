"""
Admin Dashboard Router - Admin-only endpoints with authentication
"""
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

from database import (
    get_users_collection,
    get_projects_collection,
    get_reviews_collection,
    get_team_collection,
    get_files_collection,
    get_contacts_collection,
    get_newsletters_collection,
    get_admins_collection
)

router = APIRouter(prefix="/api/admin", tags=["Admin"])

def serialize(doc) -> dict:
    """Convert MongoDB document to JSON-serializable dict"""
    if doc is None:
        return None
    doc["id"] = str(doc.pop("_id", ""))
    return doc

# ========================
# ADMIN DASHBOARD STATISTICS
# ========================

@router.get("/dashboard/stats")
async def get_dashboard_stats():
    """Get comprehensive dashboard statistics"""
    users_col = get_users_collection()
    projects_col = get_projects_collection()
    reviews_col = get_reviews_collection()
    team_col = get_team_collection()
    contacts_col = get_contacts_collection()
    newsletters_col = get_newsletters_collection()
    
    # Fetch statistics
    total_users = await users_col.count_documents({})
    total_projects = await projects_col.count_documents({})
    pending_projects = await projects_col.count_documents({"status": "pending"})
    approved_projects = await projects_col.count_documents({"status": "approved"})
    in_progress = await projects_col.count_documents({"status": "in_progress"})
    completed_projects = await projects_col.count_documents({"status": "completed"})
    
    total_reviews = await reviews_col.count_documents({})
    approved_reviews = await reviews_col.count_documents({"approved": True})
    pending_reviews = await reviews_col.count_documents({"approved": False})
    
    total_contacts = await contacts_col.count_documents({})
    unread_contacts = await contacts_col.count_documents({"status": "unread"})
    
    total_team = await team_col.count_documents({})
    newsletter_subs = await newsletters_col.count_documents({})
    
    # Recent projects
    recent_projects_cursor = projects_col.find({}).sort("created_at", -1).limit(5)
    recent_projects = [serialize(doc) async for doc in recent_projects_cursor]
    
    # Recent reviews
    recent_reviews_cursor = reviews_col.find({}).sort("created_at", -1).limit(5)
    recent_reviews = [serialize(doc) async for doc in recent_reviews_cursor]
    
    return {
        "users": {
            "total": total_users
        },
        "projects": {
            "total": total_projects,
            "pending": pending_projects,
            "approved": approved_projects,
            "in_progress": in_progress,
            "completed": completed_projects,
        },
        "reviews": {
            "total": total_reviews,
            "approved": approved_reviews,
            "pending": pending_reviews,
        },
        "contacts": {
            "total": total_contacts,
            "unread": unread_contacts,
        },
        "team": {
            "total": total_team,
        },
        "newsletter": {
            "subscribers": newsletter_subs,
        },
        "recent_projects": recent_projects,
        "recent_reviews": recent_reviews,
    }

# ========================
# USER MANAGEMENT
# ========================

@router.get("/users")
async def get_all_users():
    """Get all users"""
    users_col = get_users_collection()
    
    cursor = users_col.find({}, {"password": 0}).sort("created_at", -1)
    users = [serialize(doc) async for doc in cursor]
    
    return users

@router.get("/users/{user_id}")
async def get_user(user_id: str):
    """Get user details"""
    users_col = get_users_collection()
    
    user = await users_col.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.pop("password", None)
    return serialize(user)

@router.delete("/users/{user_id}")
async def delete_user(user_id: str):
    """Delete a user"""
    users_col = get_users_collection()
    
    result = await users_col.delete_one({"_id": ObjectId(user_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"success": True, "message": "User deleted"}

# ========================
# PROJECT MANAGEMENT
# ========================

@router.get("/projects/pending")
async def get_pending_projects():
    """Get all pending projects for review"""
    projects_col = get_projects_collection()
    
    cursor = projects_col.find({"status": "pending"}).sort("created_at", 1)
    projects = [serialize(doc) async for doc in cursor]
    
    return projects

@router.get("/projects")
async def get_all_admin_projects():
    """Get all projects with all statuses"""
    projects_col = get_projects_collection()
    
    cursor = projects_col.find({}).sort("created_at", -1)
    projects = [serialize(doc) async for doc in cursor]
    
    return projects

@router.put("/projects/{project_id}/status")
async def update_project_status(
    project_id: str,
    status: str,
    admin_notes: Optional[str] = None
):
    """Update project status"""
    projects_col = get_projects_collection()
    
    result = await projects_col.update_one(
        {"_id": ObjectId(project_id)},
        {"$set": {
            "status": status,
            "admin_notes": admin_notes or "",
            "updated_at": datetime.utcnow()
        }}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {"success": True, "message": f"Project status updated to {status}"}

@router.delete("/projects/{project_id}")
async def delete_project_admin(project_id: str):
    """Delete a project"""
    projects_col = get_projects_collection()
    
    result = await projects_col.delete_one({"_id": ObjectId(project_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {"success": True, "message": "Project deleted"}

# ========================
# REVIEW MANAGEMENT
# ========================

@router.get("/reviews/pending")
async def get_pending_reviews():
    """Get all pending reviews for approval"""
    reviews_col = get_reviews_collection()
    
    cursor = reviews_col.find({"approved": False}).sort("created_at", 1)
    reviews = [serialize(doc) async for doc in cursor]
    
    return reviews

@router.put("/reviews/{review_id}/approve")
async def admin_approve_review(review_id: str):
    """Approve a review"""
    reviews_col = get_reviews_collection()
    
    result = await reviews_col.update_one(
        {"_id": ObjectId(review_id)},
        {"$set": {
            "approved": True,
            "approved_at": datetime.utcnow()
        }}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Review not found")
    
    return {"success": True, "message": "Review approved"}

@router.delete("/reviews/{review_id}")
async def admin_delete_review(review_id: str):
    """Delete a review"""
    reviews_col = get_reviews_collection()
    
    result = await reviews_col.delete_one({"_id": ObjectId(review_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Review not found")
    
    return {"success": True, "message": "Review deleted"}

# ========================
# CONTACT MESSAGES
# ========================

@router.get("/contacts")
async def get_all_contacts():
    """Get all contact messages"""
    contacts_col = get_contacts_collection()
    
    cursor = contacts_col.find({}).sort("created_at", -1)
    contacts = [serialize(doc) async for doc in cursor]
    
    return contacts

@router.put("/contacts/{message_id}/mark-read")
async def mark_contact_read(message_id: str):
    """Mark contact message as read"""
    contacts_col = get_contacts_collection()
    
    result = await contacts_col.update_one(
        {"_id": ObjectId(message_id)},
        {"$set": {"status": "read"}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Message not found")
    
    return {"success": True, "message": "Marked as read"}

@router.delete("/contacts/{message_id}")
async def delete_contact(message_id: str):
    """Delete a contact message"""
    contacts_col = get_contacts_collection()
    
    result = await contacts_col.delete_one({"_id": ObjectId(message_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Message not found")
    
    return {"success": True, "message": "Message deleted"}

# ========================
# NEWSLETTER MANAGEMENT
# ========================

@router.get("/newsletter/subscribers")
async def get_newsletter_subscribers():
    """Get all newsletter subscribers"""
    newsletters_col = get_newsletters_collection()
    
    cursor = newsletters_col.find({}).sort("subscribed_at", -1)
    subscribers = [serialize(doc) async for doc in cursor]
    
    return subscribers

@router.delete("/newsletter/subscribers/{subscriber_id}")
async def remove_subscriber(subscriber_id: str):
    """Remove newsletter subscriber"""
    newsletters_col = get_newsletters_collection()
    
    result = await newsletters_col.delete_one({"_id": ObjectId(subscriber_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    
    return {"success": True, "message": "Subscriber removed"}

# ========================
# FILE MANAGEMENT
# ========================

@router.get("/files")
async def get_all_files():
    """Get all uploaded files"""
    files_col = get_files_collection()
    
    cursor = files_col.find({}).sort("uploaded_at", -1)
    files = [serialize(doc) async for doc in cursor]
    
    return files

@router.delete("/files/{file_id}")
async def delete_file(file_id: str):
    """Delete a file"""
    files_col = get_files_collection()
    
    result = await files_col.delete_one({"_id": ObjectId(file_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="File not found")
    
    return {"success": True, "message": "File deleted"}
