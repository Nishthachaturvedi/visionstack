"""
VisionStack - MongoDB Database Initialization Script
Initializes database indexes and creates initial collections.
Run once before starting the application.

Usage: python db_init.py
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from config import settings

async def init_db():
    """Initialize MongoDB database with indexes"""
    print("🚀 Initializing VisionStack Database...")
    print(f"📍 Connecting to: {settings.MONGO_URL}")
    
    try:
        client = AsyncIOMotorClient(settings.MONGO_URL)
        db = client[settings.DB_NAME]
        
        # Test connection
        await client.admin.command('ping')
        print("✅ Connected to MongoDB Atlas successfully")
        
        # Create indexes
        print("📇 Creating indexes...")
        
        # Users collection
        await db.users.create_index("email", unique=True)
        await db.users.create_index("created_at")
        print("  ✓ Users collection indexed")
        
        # Admins collection
        await db.admins.create_index("email", unique=True)
        print("  ✓ Admins collection indexed")
        
        # Project requests
        await db.project_requests.create_index("email")
        await db.project_requests.create_index("status")
        await db.project_requests.create_index("created_at")
        print("  ✓ Project requests collection indexed")
        
        # Feedbacks
        await db.feedbacks.create_index("project_id")
        await db.feedbacks.create_index("user_email")
        print("  ✓ Feedbacks collection indexed")
        
        # Reviews
        await db.reviews.create_index("approved")
        await db.reviews.create_index("rating")
        await db.reviews.create_index("created_at")
        print("  ✓ Reviews collection indexed")
        
        # Team members (NEW)
        await db.team_members.create_index("email", unique=True)
        await db.team_members.create_index("created_at")
        print("  ✓ Team members collection indexed")
        
        # Contact messages
        await db.contact_messages.create_index("status")
        await db.contact_messages.create_index("created_at")
        print("  ✓ Contact messages collection indexed")
        
        # Newsletter
        await db.newsletters.create_index("email", unique=True)
        print("  ✓ Newsletter collection indexed")
        
        # Uploaded files
        await db.uploaded_files.create_index("uploaded_by")
        await db.uploaded_files.create_index("uploaded_at")
        print("  ✓ Uploaded files collection indexed")
        
        print("\n✅ Database initialization completed successfully!")
        print("🎉 Ready to start the VisionStack API")
        print(f"   Database: {settings.DB_NAME}")
        print(f"   Collections: users, admins, project_requests, team_members, feedbacks, reviews, uploaded_files, contact_messages, newsletters")
        
        # Close connection
        client.close()
        
    except Exception as e:
        print(f"\n❌ Database initialization failed: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(init_db())
