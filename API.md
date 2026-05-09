# VisionStack API Documentation

**Version:** 1.0.0  
**Base URL:** `http://localhost:8000/api` (or your deployment URL)

## Table of Contents
1. [Authentication](#authentication)
2. [Projects](#projects)
3. [Team Management](#team-management)
4. [Reviews](#reviews)
5. [Admin Dashboard](#admin-dashboard)
6. [File Management](#file-management)
7. [Contact & Newsletter](#contact--newsletter)
8. [Error Handling](#error-handling)

---

## Authentication

### Register User
**POST** `/auth/register`

Create a new user account.

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

**Response (200):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user_id": "64a1b2c3d4e5f6g7h8i9j0k1"
}
```

### Login User
**POST** `/auth/login`

Authenticate and get access token.

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

**Response (200):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": "64a1b2c3d4e5f6g7h8i9j0k1",
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

### Admin Registration
**POST** `/auth/admin/register`

Register as an admin (requires admin secret key).

**Query Parameters:**
- `email`: Admin email
- `password`: Admin password
- `admin_key`: Secret key for admin registration

### Admin Login
**POST** `/auth/admin/login`

Authenticate as admin.

**Request Body:**
```json
{
  "email": "admin@example.com",
  "password": "AdminPass123!"
}
```

---

## Projects

### Submit Project
**POST** `/projects/submit`

Submit a new project requirement (requires authentication).

**Request Type:** `multipart/form-data`

**Parameters:**
- `title` (string, required): Project title (min 5 chars)
- `description` (string, required): Project description (min 20 chars)
- `budget` (number, required): Budget amount (> 0)
- `deadline` (datetime, required): Project deadline
- `tech_stack` (string, required): Comma-separated technologies
- `category` (string, required): Project category
- `priority` (string, required): Priority level (low, medium, high, urgent)
- `additional_notes` (string, optional): Additional notes
- `files` (file[], optional): Project files
- `user_email` (string, required): User email
- `user_id` (string, optional): User ID

**Response (200):**
```json
{
  "success": true,
  "message": "Project submitted successfully",
  "project_id": "64a1b2c3d4e5f6g7h8i9j0k1",
  "status": "pending"
}
```

### Get User Projects
**GET** `/projects/user/{user_email}`

Get all projects submitted by a user.

**Response (200):**
```json
[
  {
    "id": "64a1b2c3d4e5f6g7h8i9j0k1",
    "user_email": "john@example.com",
    "title": "E-commerce Platform",
    "description": "Build a modern e-commerce platform...",
    "budget": 5000,
    "deadline": "2025-03-15T00:00:00",
    "status": "pending",
    "created_at": "2024-12-15T10:30:00"
  }
]
```

### Get All Projects (Public)
**GET** `/projects/all`

Get all approved/completed projects (public view).

### Get Project Details
**GET** `/projects/{project_id}`

Get detailed information about a specific project.

### Update Project Status
**PUT** `/projects/{project_id}/status`

Update project status (admin only).

**Request Body:**
```json
{
  "status": "approved",
  "admin_notes": "Great project idea!"
}
```

**Status Values:** `pending`, `in_review`, `approved`, `rejected`, `in_progress`, `completed`

### Delete Project
**DELETE** `/projects/{project_id}`

Delete a project (admin only).

### Get Project Stats
**GET** `/projects/stats/overview`

Get project statistics.

**Response:**
```json
{
  "total_projects": 25,
  "pending": 5,
  "approved": 10,
  "in_progress": 8,
  "completed": 2
}
```

---

## Team Management

### Get Team Members
**GET** `/team/members`

Get all team members.

**Response (200):**
```json
[
  {
    "id": "64a1b2c3d4e5f6g7h8i9j0k1",
    "name": "Alice Johnson",
    "role": "Senior Developer",
    "email": "alice@example.com",
    "phone": "1234567890",
    "bio": "Experienced full-stack developer with 8 years of expertise...",
    "skills": ["Python", "JavaScript", "React", "Node.js"],
    "photo_url": "https://example.com/photo.jpg",
    "social_links": {
      "twitter": "https://twitter.com/alice",
      "linkedin": "https://linkedin.com/in/alice"
    }
  }
]
```

### Add Team Member
**POST** `/team/members/add`

Add a new team member (admin only).

**Request Type:** `multipart/form-data`

**Parameters:**
- `name` (string, required)
- `role` (string, required)
- `email` (string, required)
- `phone` (string, required)
- `bio` (string, required)
- `skills` (JSON string, required): `["Skill1", "Skill2"]`
- `photo_url` (string, optional)
- `social_links` (JSON string, optional): `{"twitter": "url", "linkedin": "url"}`

### Get Team Member Details
**GET** `/team/members/{member_id}`

Get specific team member details.

### Update Team Member
**PUT** `/team/members/{member_id}`

Update team member information (admin only).

### Delete Team Member
**DELETE** `/team/members/{member_id}`

Delete a team member (admin only).

### Get Team Stats
**GET** `/team/stats/count`

Get team statistics.

---

## Reviews

### Submit Review
**POST** `/reviews/submit`

Submit a review with optional media files.

**Request Type:** `multipart/form-data`

**Parameters:**
- `author_name` (string, required)
- `author_email` (string, required)
- `text` (string, required): Review text (min 20 chars)
- `rating` (integer, required): Rating 1-5
- `images` (file[], optional): Review images
- `videos` (file[], optional): Review videos

**Response (200):**
```json
{
  "success": true,
  "message": "Review submitted successfully",
  "review_id": "64a1b2c3d4e5f6g7h8i9j0k1",
  "approved": false
}
```

### Get Approved Reviews
**GET** `/reviews/approved`

Get all approved reviews.

**Response (200):**
```json
[
  {
    "id": "64a1b2c3d4e5f6g7h8i9j0k1",
    "author_name": "John Doe",
    "text": "Excellent service! Very professional team...",
    "rating": 5,
    "image_urls": ["https://example.com/image1.jpg"],
    "video_urls": ["https://example.com/video1.mp4"],
    "approved": true,
    "created_at": "2024-12-15T10:30:00"
  }
]
```

### Get Review Details
**GET** `/reviews/{review_id}`

Get specific review details.

### Approve Review
**PUT** `/reviews/{review_id}/approve`

Approve a review (admin only).

### Delete Review
**DELETE** `/reviews/{review_id}`

Delete a review.

### Get Reviews Stats
**GET** `/reviews/stats/overview`

Get review statistics.

---

## Admin Dashboard

### Get Dashboard Statistics
**GET** `/admin/dashboard/stats`

Get comprehensive dashboard statistics (admin only).

**Response (200):**
```json
{
  "users": {
    "total": 150
  },
  "projects": {
    "total": 45,
    "pending": 8,
    "approved": 20,
    "in_progress": 12,
    "completed": 5
  },
  "reviews": {
    "total": 85,
    "approved": 75,
    "pending": 10
  },
  "contacts": {
    "total": 32,
    "unread": 3
  },
  "team": {
    "total": 12
  },
  "newsletter": {
    "subscribers": 245
  },
  "recent_projects": [...],
  "recent_reviews": [...]
}
```

### Get All Users
**GET** `/admin/users`

Get all users (admin only).

### Get User Details
**GET** `/admin/users/{user_id}`

Get specific user details (admin only).

### Delete User
**DELETE** `/admin/users/{user_id}`

Delete a user account (admin only).

### Get Pending Projects
**GET** `/admin/projects/pending`

Get all pending projects for review (admin only).

### Get All Projects (Admin View)
**GET** `/admin/projects`

Get all projects with all statuses (admin only).

### Update Project Status
**PUT** `/admin/projects/{project_id}/status`

Update project status with notes (admin only).

### Delete Project (Admin)
**DELETE** `/admin/projects/{project_id}`

Delete a project (admin only).

### Get Pending Reviews
**GET** `/admin/reviews/pending`

Get all reviews pending approval (admin only).

### Approve Review (Admin)
**PUT** `/admin/reviews/{review_id}/approve`

Approve a review (admin only).

### Delete Review (Admin)
**DELETE** `/admin/reviews/{review_id}`

Delete a review (admin only).

### Get All Contact Messages
**GET** `/admin/contacts`

Get all contact form submissions (admin only).

### Mark Contact Read
**PUT** `/admin/contacts/{message_id}/mark-read`

Mark a contact message as read (admin only).

### Delete Contact Message
**DELETE** `/admin/contacts/{message_id}`

Delete a contact message (admin only).

### Get Newsletter Subscribers
**GET** `/admin/newsletter/subscribers`

Get all newsletter subscribers (admin only).

### Remove Subscriber
**DELETE** `/admin/newsletter/subscribers/{subscriber_id}`

Remove a newsletter subscriber (admin only).

---

## File Management

### Upload File
**POST** `/files/upload`

Upload a file (requires authentication).

**Request Type:** `multipart/form-data`

**Parameters:**
- `file` (file, required): File to upload (max 50MB)

**Allowed Types:**
- Images: JPEG, PNG, GIF, WebP
- Videos: MP4, WebM, QuickTime
- Documents: PDF

**Response (200):**
```json
{
  "url": "/uploads/uuid_filename.ext",
  "file_id": "64a1b2c3d4e5f6g7h8i9j0k1"
}
```

### Get My Files
**GET** `/files/my`

Get user's uploaded files (requires authentication).

---

## Contact & Newsletter

### Submit Contact Message
**POST** `/contact`

Submit a contact form message.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "subject": "Project Inquiry",
  "message": "I have a project proposal..."
}
```

### Subscribe Newsletter
**POST** `/newsletter/subscribe`

Subscribe to the newsletter.

**Request Body:**
```json
{
  "email": "subscriber@example.com"
}
```

---

## Error Handling

### Error Response Format

All errors follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common HTTP Status Codes

- `200 OK` - Successful request
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request parameters
- `401 Unauthorized` - Missing or invalid authentication token
- `403 Forbidden` - Insufficient permissions (e.g., non-admin accessing admin endpoint)
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

### Common Error Messages

| Error | Status | Cause |
|-------|--------|-------|
| Invalid or expired token | 401 | Token missing or expired |
| Admin access required | 403 | User is not an admin |
| Email already registered | 400 | User account already exists |
| Project not found | 404 | Project ID doesn't exist |
| File type not allowed | 400 | Unsupported file type |
| File too large | 400 | File exceeds 50MB limit |

---

## Authentication Headers

Include JWT token in all authenticated requests:

```
Authorization: Bearer {access_token}
```

## Rate Limiting

No strict rate limiting implemented. Production deployment should add:
- Rate limiting per IP address
- Request validation
- DDoS protection

## Security Notes

⚠️ **Important for Production:**
1. Change `SECRET_KEY` in `.env`
2. Use HTTPS only
3. Implement CORS restrictions
4. Add request validation
5. Implement rate limiting
6. Use environment-specific database URLs
7. Enable MongoDB authentication
8. Add request logging and monitoring
9. Implement API versioning
10. Add pagination for large result sets

---

## Example Requests (curl)

### Register User
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "password": "SecurePass123!"
  }'
```

### Login User
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123!"
  }'
```

### Submit Project
```bash
curl -X POST http://localhost:8000/api/projects/submit \
  -H "Authorization: Bearer {token}" \
  -F "title=E-commerce Platform" \
  -F "description=Build a modern e-commerce platform" \
  -F "budget=5000" \
  -F "deadline=2025-03-15T00:00:00" \
  -F "tech_stack=Python,JavaScript,React" \
  -F "category=ecommerce" \
  -F "priority=high" \
  -F "user_email=john@example.com" \
  -F "files=@project_document.pdf"
```

### Get Dashboard Stats
```bash
curl -X GET http://localhost:8000/api/admin/dashboard/stats \
  -H "Authorization: Bearer {admin_token}"
```

---

## Support

For issues or questions, contact: support@visionstack.com
