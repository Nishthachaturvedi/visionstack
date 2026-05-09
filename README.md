# VisionStack API - FastAPI + MongoDB Atlas

A modern FastAPI backend with MongoDB Atlas integration for the VisionStack project management platform.

## Features

- ✅ User Authentication (JWT tokens)
- ✅ Admin Management
- ✅ Project Request Management
- ✅ File Upload & Storage
- ✅ Feedback & Reviews System
- ✅ Contact Messages
- ✅ Newsletter Subscriptions
- ✅ MongoDB Atlas Integration
- ✅ Async/Await with Motor
- ✅ CORS Support
- ✅ Type Hints & Pydantic Validation

## Project Structure

```
├── main.py                 # FastAPI application & routes
├── config.py              # Configuration settings
├── models.py              # Pydantic models
├── database.py            # MongoDB connection & collections
├── db_init.py             # Database initialization
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (local)
├── uploads/               # File upload directory
└── README.md              # This file
```

## Prerequisites

- Python 3.9+
- MongoDB Atlas account (free tier available)
- pip or poetry

## Installation

### 1. Clone/Setup Project

```bash
cd c:\Users\nisht\Downloads\files
```

### 2. Create Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

The `.env` file is already configured with your MongoDB Atlas credentials:

```env
MONGO_URL=mongodb+srv://nishtha_db_user:Nistha1@cluster0.agln8yx.mongodb.net/?retryWrites=true&w=majority
DB_NAME=visionstack
SECRET_KEY=visionstack-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
UPLOAD_DIR=uploads
```

**Important:** Keep your `.env` file secure and never commit it to version control.

## Database Setup

### Initialize MongoDB Database

Run the initialization script to create indexes:

```bash
python db_init.py
```

Output:
```
🚀 Initializing VisionStack Database...
📍 Connecting to: mongodb+srv://nishtha_db_user:Nistha1@cluster0.agln8yx.mongodb.net/?retryWrites=true&w=majority
✅ Connected to MongoDB Atlas successfully
📇 Creating indexes...
  ✓ Users collection indexed
  ✓ Admins collection indexed
  ...
✅ Database initialization completed successfully!
🎉 Ready to start the VisionStack API
```

## Running the Application

### Start Development Server

```bash
uvicorn main:app --reload
```

Server will be available at: `http://localhost:8000`

### Access API Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Collections & Data Models

### Users
```json
{
  "_id": ObjectId,
  "first_name": "string",
  "last_name": "string",
  "email": "email@example.com",
  "password": "hashed_password",
  "role": "user",
  "profile_complete": false,
  "created_at": "ISO datetime",
  "updated_at": "ISO datetime"
}
```

### Project Requests
```json
{
  "_id": ObjectId,
  "title": "string",
  "description": "string",
  "email": "email@example.com",
  "budget": 5000,
  "timeline": "string",
  "status": "pending|approved|in_progress|completed|rejected",
  "created_at": "ISO datetime",
  "updated_at": "ISO datetime",
  "admin_notes": "string"
}
```

### Files
```json
{
  "_id": ObjectId,
  "original_name": "string",
  "stored_name": "uuid_string",
  "content_type": "mime/type",
  "size": 1024,
  "uploaded_by": "email@example.com",
  "uploaded_at": "ISO datetime",
  "url": "/uploads/filename"
}
```

### Feedback
```json
{
  "_id": ObjectId,
  "project_id": "ObjectId string",
  "user_email": "email@example.com",
  "rating": 5,
  "message": "string",
  "created_at": "ISO datetime"
}
```

### Reviews
```json
{
  "_id": ObjectId,
  "author_name": "string",
  "author_email": "email@example.com",
  "rating": 5,
  "title": "string",
  "content": "string",
  "approved": false,
  "created_at": "ISO datetime"
}
```

### Contact Messages
```json
{
  "_id": ObjectId,
  "name": "string",
  "email": "email@example.com",
  "subject": "string",
  "message": "string",
  "status": "unread|read",
  "created_at": "ISO datetime"
}
```

### Newsletter
```json
{
  "_id": ObjectId,
  "email": "email@example.com",
  "subscribed_at": "ISO datetime"
}
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/admin/register` - Register admin
- `POST /api/auth/admin/login` - Login admin

### Projects
- `POST /api/projects/request` - Submit project request
- `GET /api/projects/my` - Get user's projects
- `GET /api/projects/all` - Get all projects (admin)
- `PUT /api/projects/{id}/status` - Update project status (admin)
- `DELETE /api/projects/{id}` - Delete project (admin)

### Files
- `POST /api/files/upload` - Upload file
- `GET /api/files/my` - Get user's files

### Feedback & Reviews
- `POST /api/feedback` - Submit feedback
- `POST /api/reviews` - Submit review
- `GET /api/reviews/approved` - Get approved reviews
- `PUT /api/reviews/{id}/approve` - Approve review (admin)
- `DELETE /api/reviews/{id}` - Delete review (admin)

### Contact & Newsletter
- `POST /api/contact` - Submit contact message
- `GET /api/contact/all` - Get all contacts (admin)
- `PUT /api/contact/{id}/mark-read` - Mark message as read (admin)
- `POST /api/newsletter/subscribe` - Subscribe to newsletter
- `GET /api/newsletter/subscribers` - Get subscribers (admin)

### User Dashboard
- `GET /api/user/profile` - Get user profile
- `PUT /api/user/profile` - Update user profile

### Admin Dashboard
- `GET /api/admin/stats` - Get dashboard statistics
- `GET /api/admin/users` - Get all users
- `DELETE /api/admin/users/{id}` - Delete user
- `GET /api/admin/feedback` - Get all feedback

### Health Check
- `GET /` - Root endpoint
- `GET /api/health` - Health check

## Dynamic Data Storage

All data is **automatically stored dynamically** in MongoDB Atlas:

1. **User Registration** → Saved to `users` collection
2. **Project Submission** → Saved to `project_requests` collection
3. **File Upload** → File stored in `uploads/`, metadata in `uploaded_files` collection
4. **Feedback** → Saved to `feedbacks` collection
5. **Reviews** → Saved to `reviews` collection
6. **Contact Messages** → Saved to `contact_messages` collection
7. **Newsletter Signup** → Saved to `newsletters` collection

All collections have proper indexes for fast queries and validation rules for data integrity.

## Environment Variables

| Variable | Value | Purpose |
|----------|-------|---------|
| `MONGO_URL` | MongoDB Atlas connection string | Database connection |
| `DB_NAME` | visionstack | Database name |
| `SECRET_KEY` | Your secret key | JWT token signing |
| `ALGORITHM` | HS256 | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 1440 | Token expiration (24 hours) |
| `UPLOAD_DIR` | uploads | File upload directory |

## Security Considerations

1. ✅ **Password Hashing** - Bcrypt hashing for user passwords
2. ✅ **JWT Authentication** - Token-based authentication
3. ✅ **Input Validation** - Pydantic models for type safety
4. ✅ **File Validation** - Size and type restrictions
5. ⚠️ **Production Setup:**
   - Change `SECRET_KEY` to a strong random value
   - Use environment-specific configurations
   - Enable HTTPS in production
   - Restrict CORS origins to specific domains
   - Enable MongoDB IP whitelist

## Common Tasks

### Add a New API Endpoint

1. Define Pydantic model in `models.py`
2. Import model in `main.py`
3. Create async function with `@app.get/post/put/delete` decorator
4. Use collection getters from `database.py`
5. Return JSON response

Example:
```python
@app.post("/api/custom", tags=["Custom"])
async def custom_endpoint(data: CustomModel):
    col = get_custom_collection()
    result = await col.insert_one(data.dict())
    return {"id": str(result.inserted_id)}
```

### Query Data from MongoDB

```python
# Find one
user = await users_col.find_one({"email": "user@example.com"})

# Find multiple
cursor = users_col.find({}).sort("created_at", -1)
users = [serialize(d) async for d in cursor]

# Update
await users_col.update_one(
    {"_id": ObjectId(user_id)},
    {"$set": {"updated_at": datetime.utcnow()}}
)

# Delete
await users_col.delete_one({"_id": ObjectId(user_id)})

# Count
count = await users_col.count_documents({})
```

## Troubleshooting

### Connection Issues

```bash
# Test MongoDB connection
python db_init.py
```

### Import Errors

```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### File Upload Issues

- Check `uploads/` directory permissions
- Verify file size doesn't exceed 50MB limit
- Check allowed MIME types in `main.py`

## Development Tips

1. Use VS Code with Python extension
2. Enable Pylance for better intellisense
3. Use Postman or Thunder Client for API testing
4. Check MongoDB Atlas dashboard for data validation
5. Enable API docs at `/docs` for interactive testing

## Deployment

### Using Gunicorn (Production)

```bash
pip install gunicorn
gunicorn main:app -w 4 -b 0.0.0.0:8000
```

### Using Docker

```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

## License

Proprietary - VisionStack

## Support

For issues or questions, contact the development team.

### Interactive Features
- Multi-step project request modal (3 steps + success)
- Client login/register auth modal
- Live chatbot UI with smart replies
- Portfolio category filtering
- Scroll-triggered reveal animations
- Mobile hamburger nav drawer
- Responsive design (desktop/tablet/mobile)

---

## ⚙️ Backend API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | User login → JWT token |
| POST | `/api/auth/admin/register` | Register admin (requires secret key) |
| POST | `/api/auth/admin/login` | Admin login → JWT token |

### Projects
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/projects/request` | Submit project request |
| GET | `/api/projects/my` | Get user's own projects |
| GET | `/api/projects/all` | Admin: Get all projects |
| PUT | `/api/projects/{id}/status` | Admin: Update project status |
| DELETE | `/api/projects/{id}` | Admin: Delete project |

### Files
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/files/upload` | Upload file (image/pdf/video) |
| GET | `/api/files/my` | Get user's uploaded files |

### Feedback & Reviews
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/feedback` | Submit project feedback |
| POST | `/api/reviews` | Submit public review |
| GET | `/api/reviews/approved` | Get all approved reviews |
| PUT | `/api/reviews/{id}/approve` | Admin: Approve review |

### Contact & Newsletter
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/contact` | Send contact message |
| GET | `/api/contact/all` | Admin: Get all messages |
| POST | `/api/newsletter/subscribe` | Subscribe to newsletter |

### User & Admin
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/user/profile` | Get logged-in user profile |
| PUT | `/api/user/profile` | Update profile |
| GET | `/api/admin/stats` | Admin dashboard stats |
| GET | `/api/admin/users` | All users list |
| DELETE | `/api/admin/users/{id}` | Delete user |
| GET | `/api/admin/feedback` | All feedback |

---

## 🗃️ MongoDB Collections

```
visionstack/
├── users                   # Registered users
├── admins                  # Admin accounts
├── project_requests        # Client project submissions
├── feedbacks               # Project feedback (authenticated)
├── reviews                 # Public testimonials (moderated)
├── uploaded_files          # File upload metadata
├── contact_messages        # Contact form submissions
└── newsletters             # Email subscribers
```

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+
- MongoDB 6.0+ (local or Atlas)
- Node.js (optional, for serving frontend)

### 1. Backend Setup

```bash
cd visionstack/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your MongoDB URL and secrets

# Initialize database (create indexes & seed data)
python db_init.py

# Start the API server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`
API Docs (Swagger): `http://localhost:8000/docs`

### 2. Frontend Setup

Simply open `frontend/index.html` in a browser, OR serve it:

```bash
# Using Python (from frontend directory)
cd visionstack/frontend
python -m http.server 3000

# Using Node.js
npx serve .
```

Frontend will be at: `http://localhost:3000`

### 3. Connect Frontend to Backend

In `frontend/index.html`, update API calls to point to your backend:

```javascript
// Replace alert() calls in form handlers with actual fetch() calls:
const response = await fetch('http://localhost:8000/api/projects/request', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(formData)
});
```

---

## 🔐 Security Notes

- JWT tokens expire after 24 hours
- Passwords are hashed using bcrypt
- File uploads are validated for type and size (50MB max)
- Admin routes require JWT + admin role
- **Change SECRET_KEY and ADMIN_SECRET_KEY in production!**
- Use HTTPS in production
- Set CORS origins to your specific domain in production

---

## 🌐 Deployment

### Backend (Railway / Render / DigitalOcean)
```bash
# Set environment variables in your hosting platform
MONGO_URL=mongodb+srv://...
SECRET_KEY=your-production-secret
ADMIN_SECRET_KEY=your-admin-secret
```

### Frontend
- Deploy to Vercel, Netlify, or Cloudflare Pages
- Upload the `frontend/` folder
- Update API base URL in JavaScript

### MongoDB Atlas (Cloud)
1. Create account at mongodb.com/atlas
2. Create a free M0 cluster
3. Get connection string
4. Set as MONGO_URL in .env

---

## 🎯 Color Reference

| Color | Hex | Usage |
|-------|-----|-------|
| Royal Gold | `#c9a227` | Primary accent, borders, highlights |
| Gold Light | `#e8c547` | Hover states, text accents |
| Deep Purple | `#1a0533` | Background gradient |
| Purple Mid | `#2d0760` | Card backgrounds |
| Purple Glow | `#7b2fff` | Particle effects, orbs |
| Silver | `#c0c8d8` | Body text |
| Silver Dim | `#7a8399` | Secondary text |
| Black | `#050508` | Primary background |

---

Built with 💛 by VisionStack — *Where Vision Meets Technology*
