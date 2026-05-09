"""
Team Members Router - Handles team management
"""
from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
import uuid
import os
import json

from models_v2 import TeamMemberCreate, TeamMemberResponse
from database import get_team_collection, get_files_collection
from config import settings

router = APIRouter(prefix="/api/team", tags=["Team"])

def serialize(doc) -> dict:
    """Convert MongoDB document to JSON-serializable dict"""
    if doc is None:
        return None
    doc["id"] = str(doc.pop("_id", ""))
    return doc

# ========================
# TEAM ENDPOINTS
# ========================

@router.get("/members", response_model=List[dict])
async def get_team_members():
    """Get all team members"""
    team_col = get_team_collection()
    
    cursor = team_col.find({}).sort("created_at", 1)
    members = [serialize(doc) async for doc in cursor]
    
    return members

@router.post("/members/add", response_model=dict)
async def add_team_member(
    name: str,
    role: str,
    email: str,
    phone: str,
    bio: str,
    skills: str,  # JSON string
    photo_url: Optional[str] = None,
    social_links: Optional[str] = None,  # JSON string
):
    """Add a new team member (admin only)"""
    team_col = get_team_collection()
    
    try:
        skills_list = json.loads(skills) if isinstance(skills, str) else skills
        social_dict = json.loads(social_links) if social_links else {}
        
        member_doc = {
            "name": name,
            "role": role,
            "email": email,
            "phone": phone,
            "bio": bio,
            "skills": skills_list,
            "photo_url": photo_url or "",
            "social_links": social_dict,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }
        
        result = await team_col.insert_one(member_doc)
        
        return {
            "success": True,
            "message": "Team member added successfully",
            "member_id": str(result.inserted_id)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error adding team member: {str(e)}")

@router.get("/members/{member_id}", response_model=dict)
async def get_team_member(member_id: str):
    """Get team member details"""
    team_col = get_team_collection()
    
    member = await team_col.find_one({"_id": ObjectId(member_id)})
    if not member:
        raise HTTPException(status_code=404, detail="Team member not found")
    
    return serialize(member)

@router.put("/members/{member_id}", response_model=dict)
async def update_team_member(
    member_id: str,
    name: Optional[str] = None,
    role: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    bio: Optional[str] = None,
    skills: Optional[str] = None,
    photo_url: Optional[str] = None,
    social_links: Optional[str] = None,
):
    """Update team member"""
    team_col = get_team_collection()
    
    try:
        update_data = {}
        if name:
            update_data["name"] = name
        if role:
            update_data["role"] = role
        if email:
            update_data["email"] = email
        if phone:
            update_data["phone"] = phone
        if bio:
            update_data["bio"] = bio
        if skills:
            update_data["skills"] = json.loads(skills) if isinstance(skills, str) else skills
        if photo_url:
            update_data["photo_url"] = photo_url
        if social_links:
            update_data["social_links"] = json.loads(social_links) if isinstance(social_links, str) else social_links
        
        update_data["updated_at"] = datetime.utcnow()
        
        result = await team_col.update_one(
            {"_id": ObjectId(member_id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Team member not found")
        
        return {"success": True, "message": "Team member updated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating team member: {str(e)}")

@router.delete("/members/{member_id}")
async def delete_team_member(member_id: str):
    """Delete team member (admin only)"""
    team_col = get_team_collection()
    
    result = await team_col.delete_one({"_id": ObjectId(member_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Team member not found")
    
    return {"success": True, "message": "Team member deleted"}

@router.get("/stats/count")
async def get_team_stats():
    """Get team statistics"""
    team_col = get_team_collection()
    
    total = await team_col.count_documents({})
    
    cursor = team_col.find({}).limit(5).sort("created_at", -1)
    recent = [serialize(doc) async for doc in cursor]
    
    return {
        "total_members": total,
        "recent_members": recent
    }
