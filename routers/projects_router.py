"""
Projects Router - Handles all project-related endpoints
"""
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
import uuid
import os

from models_v2 import ProjectCreate, ProjectResponse, ProjectStatus
from database import get_projects_collection, get_files_collection
from config import settings

router = APIRouter(prefix="/api/projects", tags=["Projects"])

def serialize(doc) -> dict:
    """Convert MongoDB document to JSON-serializable dict"""
    if doc is None:
        return None
    doc["id"] = str(doc.pop("_id", ""))
    return doc

# ========================
# PROJECT ENDPOINTS
# ========================

@router.post("/submit", response_model=dict)
async def submit_project(
    title: str = Form(...),
    description: str = Form(...),
    budget: float = Form(...),
    deadline: str = Form(...),
    tech_stack: str = Form(...),
    category: str = Form(...),
    priority: str = Form(...),
    additional_notes: Optional[str] = Form(None),
    files: Optional[List[UploadFile]] = File(None),
    user_email: str = Form(...),
    user_id: Optional[str] = Form(None),
):
    """Submit a new project requirement"""
    projects_col = get_projects_collection()
    files_col = get_files_collection()
    
    try:
        file_urls = []
        
        # Process uploaded files
        if files:
            for file in files:
                try:
                    filename = f"{uuid.uuid4()}_{file.filename}"
                    filepath = os.path.join(settings.UPLOAD_DIR, filename)
                    
                    content = await file.read()
                    with open(filepath, "wb") as f:
                        f.write(content)
                    
                    file_urls.append(f"/uploads/{filename}")
                    
                    # Save file metadata
                    file_doc = {
                        "original_name": file.filename,
                        "stored_name": filename,
                        "content_type": file.content_type,
                        "size": len(content),
                        "uploaded_by": user_email,
                        "uploaded_at": datetime.utcnow(),
                        "url": f"/uploads/{filename}",
                        "project_related": True,
                    }
                    await files_col.insert_one(file_doc)
                except Exception as e:
                    print(f"File upload error: {e}")
        
        # Create project document
        project_doc = {
            "user_email": user_email,
            "user_id": user_id,
            "title": title,
            "description": description,
            "budget": budget,
            "deadline": datetime.fromisoformat(deadline),
            "tech_stack": [t.strip() for t in tech_stack.split(",")],
            "category": category,
            "priority": priority,
            "status": ProjectStatus.PENDING.value,
            "file_urls": file_urls,
            "additional_notes": additional_notes or "",
            "admin_notes": "",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        
        result = await projects_col.insert_one(project_doc)
        
        return {
            "success": True,
            "message": "Project submitted successfully",
            "project_id": str(result.inserted_id),
            "status": "pending"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error submitting project: {str(e)}")

@router.get("/user/{user_email}", response_model=List[dict])
async def get_user_projects(user_email: str):
    """Get all projects submitted by a user"""
    projects_col = get_projects_collection()
    
    cursor = projects_col.find({"user_email": user_email}).sort("created_at", -1)
    projects = [serialize(doc) async for doc in cursor]
    
    return projects

@router.get("/all", response_model=List[dict])
async def get_all_projects():
    """Get all projects (public view - only approved/completed)"""
    projects_col = get_projects_collection()
    
    cursor = projects_col.find({
        "status": {"$in": ["approved", "in_progress", "completed"]}
    }).sort("created_at", -1)
    
    projects = [serialize(doc) async for doc in cursor]
    return projects

@router.get("/{project_id}", response_model=dict)
async def get_project(project_id: str):
    """Get project details"""
    projects_col = get_projects_collection()
    
    project = await projects_col.find_one({"_id": ObjectId(project_id)})
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return serialize(project)

@router.put("/{project_id}/status", response_model=dict)
async def update_project_status(
    project_id: str,
    status: ProjectStatus,
    admin_notes: Optional[str] = None
):
    """Update project status (admin only)"""
    projects_col = get_projects_collection()
    
    result = await projects_col.update_one(
        {"_id": ObjectId(project_id)},
        {"$set": {
            "status": status.value,
            "admin_notes": admin_notes or "",
            "updated_at": datetime.utcnow()
        }}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {
        "success": True,
        "message": f"Project status updated to {status.value}"
    }

@router.delete("/{project_id}")
async def delete_project(project_id: str):
    """Delete a project"""
    projects_col = get_projects_collection()
    
    result = await projects_col.delete_one({"_id": ObjectId(project_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {"success": True, "message": "Project deleted"}

@router.get("/stats/overview")
async def get_projects_stats():
    """Get project statistics"""
    projects_col = get_projects_collection()
    
    total = await projects_col.count_documents({})
    pending = await projects_col.count_documents({"status": "pending"})
    approved = await projects_col.count_documents({"status": "approved"})
    completed = await projects_col.count_documents({"status": "completed"})
    in_progress = await projects_col.count_documents({"status": "in_progress"})
    
    return {
        "total_projects": total,
        "pending": pending,
        "approved": approved,
        "in_progress": in_progress,
        "completed": completed,
    }
