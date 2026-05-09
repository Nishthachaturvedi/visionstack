"""
Advanced Reviews Router - Handles reviews with media support
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
import uuid
import os

from models_v2 import ReviewCreate, ReviewResponse
from database import get_reviews_collection, get_files_collection
from config import settings

router = APIRouter(prefix="/api/reviews", tags=["Reviews"])

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
ALLOWED_VIDEO_TYPES = {"video/mp4", "video/webm", "video/quicktime"}

def serialize(doc) -> dict:
    """Convert MongoDB document to JSON-serializable dict"""
    if doc is None:
        return None
    doc["id"] = str(doc.pop("_id", ""))
    return doc

# ========================
# REVIEW ENDPOINTS
# ========================

@router.post("/submit", response_model=dict)
async def submit_review(
    author_name: str = Form(...),
    author_email: str = Form(...),
    text: str = Form(...),
    rating: int = Form(...),
    images: Optional[List[UploadFile]] = File(None),
    videos: Optional[List[UploadFile]] = File(None),
):
    """Submit a new review with media support"""
    reviews_col = get_reviews_collection()
    files_col = get_files_collection()
    
    try:
        image_urls = []
        video_urls = []
        
        # Process image uploads
        if images:
            for image in images:
                if image.content_type not in ALLOWED_IMAGE_TYPES:
                    raise HTTPException(status_code=400, detail="Invalid image type")
                
                filename = f"review_img_{uuid.uuid4()}_{image.filename}"
                filepath = os.path.join(settings.UPLOAD_DIR, filename)
                
                content = await image.read()
                with open(filepath, "wb") as f:
                    f.write(content)
                
                image_urls.append(f"/uploads/{filename}")
                
                await files_col.insert_one({
                    "original_name": image.filename,
                    "stored_name": filename,
                    "content_type": image.content_type,
                    "size": len(content),
                    "uploaded_by": author_email,
                    "uploaded_at": datetime.utcnow(),
                    "url": f"/uploads/{filename}",
                    "review_related": True,
                })
        
        # Process video uploads
        if videos:
            for video in videos:
                if video.content_type not in ALLOWED_VIDEO_TYPES:
                    raise HTTPException(status_code=400, detail="Invalid video type")
                
                filename = f"review_vid_{uuid.uuid4()}_{video.filename}"
                filepath = os.path.join(settings.UPLOAD_DIR, filename)
                
                content = await video.read()
                with open(filepath, "wb") as f:
                    f.write(content)
                
                video_urls.append(f"/uploads/{filename}")
                
                await files_col.insert_one({
                    "original_name": video.filename,
                    "stored_name": filename,
                    "content_type": video.content_type,
                    "size": len(content),
                    "uploaded_by": author_email,
                    "uploaded_at": datetime.utcnow(),
                    "url": f"/uploads/{filename}",
                    "review_related": True,
                })
        
        review_doc = {
            "author_name": author_name,
            "author_email": author_email,
            "text": text,
            "rating": rating,
            "image_urls": image_urls,
            "video_urls": video_urls,
            "approved": False,
            "created_at": datetime.utcnow(),
            "approved_at": None,
        }
        
        result = await reviews_col.insert_one(review_doc)
        
        return {
            "success": True,
            "message": "Review submitted successfully. Awaiting admin approval.",
            "review_id": str(result.inserted_id),
            "approved": False
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error submitting review: {str(e)}")

@router.get("/approved", response_model=List[dict])
async def get_approved_reviews():
    """Get all approved reviews"""
    reviews_col = get_reviews_collection()
    
    cursor = reviews_col.find({"approved": True}).sort("created_at", -1)
    reviews = [serialize(doc) async for doc in cursor]
    
    return reviews

@router.get("/{review_id}", response_model=dict)
async def get_review(review_id: str):
    """Get review details"""
    reviews_col = get_reviews_collection()
    
    review = await reviews_col.find_one({"_id": ObjectId(review_id)})
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    return serialize(review)

@router.put("/{review_id}/approve", response_model=dict)
async def approve_review(review_id: str):
    """Approve a review (admin only)"""
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

@router.put("/{review_id}/reject", response_model=dict)
async def reject_review(review_id: str):
    """Reject a review (admin only)"""
    reviews_col = get_reviews_collection()
    
    result = await reviews_col.delete_one({"_id": ObjectId(review_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Review not found")
    
    return {"success": True, "message": "Review rejected and removed"}

@router.delete("/{review_id}")
async def delete_review(review_id: str):
    """Delete a review"""
    reviews_col = get_reviews_collection()
    
    result = await reviews_col.delete_one({"_id": ObjectId(review_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Review not found")
    
    return {"success": True, "message": "Review deleted"}

@router.get("/stats/overview")
async def get_reviews_stats():
    """Get review statistics"""
    reviews_col = get_reviews_collection()
    
    total = await reviews_col.count_documents({})
    approved = await reviews_col.count_documents({"approved": True})
    pending = await reviews_col.count_documents({"approved": False})
    
    avg_rating_data = await reviews_col.aggregate([
        {"$group": {"_id": None, "avg_rating": {"$avg": "$rating"}}}
    ]).to_list(1)
    
    avg_rating = avg_rating_data[0]["avg_rating"] if avg_rating_data else 0
    
    return {
        "total_reviews": total,
        "approved_reviews": approved,
        "pending_reviews": pending,
        "average_rating": round(avg_rating, 2)
    }
