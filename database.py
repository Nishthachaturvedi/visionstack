"""
Database module for MongoDB connection and collections management
"""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from config import settings
from typing import Optional

class Database:
    client =None
    db = None

    @classmethod
    async def connect_db(cls):
        """Initialize database connection"""
        print("🔌 Connecting to MongoDB Atlas...")
        cls.client = AsyncIOMotorClient(settings.MONGO_URL)
        cls.db = cls.client[settings.DB_NAME]
        
        # Test connection
        try:
            await cls.client.admin.command('ping')
            print("✅ Connected to MongoDB Atlas successfully")
        except Exception as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            raise

    @classmethod
    async def close_db(cls):
        """Close database connection"""
        if cls.client:
            cls.client.close()
            print("🔌 Disconnected from MongoDB")

    @classmethod
    def get_db(cls):
        """Get database instance"""
        if cls.db is None:
            raise RuntimeError("Database not connected. Call connect_db first.")
        return cls.db

    @classmethod
    def get_collection(cls, collection_name: str):
        """Get specific collection"""
        db = cls.get_db()
        return db[collection_name]


# Convenience functions for collections
def get_users_collection():
    return Database.get_collection("users")

def get_admins_collection():
    return Database.get_collection("admins")

def get_projects_collection():
    return Database.get_collection("project_requests")

def get_feedbacks_collection():
    return Database.get_collection("feedbacks")

def get_reviews_collection():
    return Database.get_collection("reviews")

def get_files_collection():
    return Database.get_collection("uploaded_files")

def get_contacts_collection():
    return Database.get_collection("contact_messages")

def get_newsletters_collection():
    return Database.get_collection("newsletters")

def get_team_collection():
    return Database.get_collection("team_members")
