"""
Quick Start Guide for VisionStack API
"""

# =====================================================
# 1. SETUP THE PROJECT
# =====================================================

# Install dependencies
pip install -r requirements.txt

# Initialize database (creates indexes)
python db_init.py

# Start the API server
uvicorn main:app --reload


# =====================================================
# 2. REGISTER & LOGIN
# =====================================================

# Register a new user
POST http://localhost:8000/api/auth/register
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "password": "SecurePassword123"
}

# Response:
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "user_id": "507f1f77bcf86cd799439011"
}

# Login
POST http://localhost:8000/api/auth/login
{
    "email": "john@example.com",
    "password": "SecurePassword123"
}

# Use the access_token in Authorization header for protected endpoints
Authorization: Bearer <access_token>


# =====================================================
# 3. SUBMIT A PROJECT REQUEST (DYNAMIC STORAGE)
# =====================================================

POST http://localhost:8000/api/projects/request
{
    "title": "E-commerce Website",
    "description": "Build a modern e-commerce platform",
    "email": "client@example.com",
    "phone": "+1234567890",
    "company": "ABC Corporation",
    "budget": 15000,
    "timeline": "3 months"
}

# Data is automatically saved to MongoDB:
# Collection: project_requests
# - Status: pending (default)
# - created_at: ISO datetime
# - Updated in real-time


# =====================================================
# 4. UPLOAD A FILE (DYNAMIC STORAGE)
# =====================================================

POST http://localhost:8000/api/files/upload
Headers: Authorization: Bearer <token>
Body: multipart/form-data
  - file: <select file>

# File is saved to:
# - Physical: uploads/<uuid_filename>
# - Metadata: uploaded_files collection in MongoDB
# Includes: filename, size, type, uploader, upload time


# =====================================================
# 5. SUBMIT FEEDBACK (DYNAMIC STORAGE)
# =====================================================

POST http://localhost:8000/api/feedback
Headers: Authorization: Bearer <token>
{
    "project_id": "507f1f77bcf86cd799439011",
    "rating": 5,
    "message": "Excellent work! Highly satisfied with the results."
}

# Automatically saved to feedbacks collection:
# - user_email: extracted from token
# - created_at: current timestamp
# - All data indexed for quick retrieval


# =====================================================
# 6. SUBMIT A REVIEW (DYNAMIC STORAGE)
# =====================================================

POST http://localhost:8000/api/reviews
{
    "author_name": "Jane Smith",
    "author_email": "jane@example.com",
    "rating": 5,
    "title": "Outstanding Service",
    "content": "Best web development team we've worked with!"
}

# Automatically saved to reviews collection:
# - approved: false (requires admin approval)
# - created_at: current timestamp
# - Email indexed for easy lookup


# =====================================================
# 7. CONTACT FORM (DYNAMIC STORAGE)
# =====================================================

POST http://localhost:8000/api/contact
{
    "name": "Michael Johnson",
    "email": "michael@example.com",
    "subject": "Inquiry about services",
    "message": "I'd like to know more about your web development services."
}

# Automatically saved to contact_messages collection:
# - status: "unread" (default)
# - created_at: current timestamp
# - Indexed for admin dashboard queries


# =====================================================
# 8. NEWSLETTER SIGNUP (DYNAMIC STORAGE)
# =====================================================

POST http://localhost:8000/api/newsletter/subscribe
{
    "email": "subscriber@example.com"
}

# Automatically saved to newsletters collection:
# - subscribed_at: current timestamp
# - Duplicate emails prevented (unique index)


# =====================================================
# 9. GET USER PROFILE
# =====================================================

GET http://localhost:8000/api/user/profile
Headers: Authorization: Bearer <token>

# Returns user data from users collection:
{
    "id": "507f1f77bcf86cd799439011",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "profile_complete": false,
    "created_at": "2024-01-01T10:00:00",
    "updated_at": "2024-01-01T10:00:00"
}


# =====================================================
# 10. UPDATE PROFILE
# =====================================================

PUT http://localhost:8000/api/user/profile
Headers: Authorization: Bearer <token>
{
    "first_name": "John",
    "last_name": "Doe Updated",
    "profile_complete": true
}

# Automatically updates in users collection with:
# - updated_at: current timestamp


# =====================================================
# 11. ADMIN: GET ALL PROJECTS
# =====================================================

GET http://localhost:8000/api/projects/all
Headers: Authorization: Bearer <admin_token>

# Returns all projects from project_requests collection:
[
    {
        "id": "507f1f77bcf86cd799439012",
        "title": "E-commerce Website",
        "email": "client@example.com",
        "status": "pending",
        "budget": 15000,
        "created_at": "2024-01-01T10:00:00"
    }
]


# =====================================================
# 12. ADMIN: UPDATE PROJECT STATUS
# =====================================================

PUT http://localhost:8000/api/projects/507f1f77bcf86cd799439012/status
Headers: Authorization: Bearer <admin_token>
{
    "status": "approved",
    "message": "Approved. Starting work next week."
}

# Automatically updates project_requests collection:
# - status: "approved"
# - admin_notes: "Approved. Starting work next week."
# - updated_at: current timestamp


# =====================================================
# 13. ADMIN: DASHBOARD STATISTICS
# =====================================================

GET http://localhost:8000/api/admin/stats
Headers: Authorization: Bearer <admin_token>

# Returns aggregated data from all collections:
{
    "total_users": 42,
    "total_projects": 28,
    "pending_projects": 5,
    "completed_projects": 23,
    "total_contacts": 156,
    "pending_reviews": 3
}


# =====================================================
# 14. CHECK API HEALTH
# =====================================================

GET http://localhost:8000/api/health

# Returns:
{
    "status": "healthy",
    "timestamp": "2024-01-01T10:00:00",
    "database": "connected"
}


# =====================================================
# MONGODB COLLECTIONS STRUCTURE
# =====================================================

Database: visionstack

Collections (auto-created on first write):
1. users - User accounts with hashed passwords
2. admins - Admin accounts
3. project_requests - Project submission requests
4. feedbacks - User feedback on projects
5. reviews - Reviews (require approval)
6. contact_messages - Contact form submissions
7. newsletters - Email subscribers
8. uploaded_files - File upload metadata

All collections have:
✓ Proper indexes for fast queries
✓ Validation rules (email unique, ratings 1-5, etc.)
✓ Timestamps (created_at, updated_at)
✓ MongoDB automatic _id field


# =====================================================
# COMMON QUERIES
# =====================================================

# Find user by email
users.findOne({ "email": "john@example.com" })

# Get all pending projects
project_requests.find({ "status": "pending" }).sort({ "created_at": -1 })

# Get approved reviews
reviews.find({ "approved": true }).sort({ "created_at": -1 })

# Count total newsletter subscribers
newsletters.countDocuments({})

# Get user's uploaded files
uploaded_files.find({ "uploaded_by": "john@example.com" })

# Get unread contact messages
contact_messages.find({ "status": "unread" })


# =====================================================
# TESTING WITH CURL
# =====================================================

# Test health endpoint
curl http://localhost:8000/api/health

# Register user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"first_name":"John","last_name":"Doe","email":"john@example.com","password":"SecurePassword123"}'

# Subscribe to newsletter
curl -X POST http://localhost:8000/api/newsletter/subscribe \
  -H "Content-Type: application/json" \
  -d '{"email":"subscriber@example.com"}'


# =====================================================
# PRODUCTION CHECKLIST
# =====================================================

[ ] Change SECRET_KEY to a strong random value
[ ] Enable HTTPS/SSL
[ ] Restrict CORS to specific domain
[ ] Set strong MongoDB password
[ ] Enable MongoDB IP whitelist
[ ] Set proper file upload limits
[ ] Enable rate limiting
[ ] Configure logging
[ ] Use environment-specific .env files
[ ] Back up MongoDB data regularly
[ ] Monitor API performance
[ ] Set up error tracking (Sentry)
[ ] Enable API authentication for all endpoints
