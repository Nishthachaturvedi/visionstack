"""
Configuration module for VisionStack application
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings"""
    
    # MongoDB
    MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017"),
    DB_NAME = os.getenv("DB_NAME", "VisionStack")
    
    # Security
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY", 
        "visionstack-secret-key-change-in-production"
    )
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440")
    )
    
    # File Upload
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")
    
    # Ensure upload directory exists
    @staticmethod
    def ensure_upload_dir():
        os.makedirs(Settings.UPLOAD_DIR, exist_ok=True)

# Create settings instance
settings = Settings()
settings.ensure_upload_dir()
