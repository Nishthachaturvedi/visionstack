# VisionStack Production Upgrade - Implementation Guide

## Overview

This guide explains the production-grade features added to VisionStack and how to integrate them into your frontend.

## What's New

### 1. **Project Requirements System**
- Users can submit detailed project proposals
- Projects tracked through status workflow: pending → in_review → approved → in_progress → completed
- Supports file uploads, tech stack specification, budget, and deadlines
- Admin dashboard for project management and approval

### 2. **Team Management**
- Display company team members with profiles
- Skills showcase, social media links
- Team member photos and bios
- Admin ability to manage team directory

### 3. **Advanced Reviews System**
- Reviews with image and video support
- Rating system (1-5 stars)
- Approval workflow for quality control
- Review carousel on homepage

### 4. **Admin Dashboard**
- Comprehensive statistics (users, projects, reviews, team members)
- Project approval management
- Review moderation
- Contact message management
- Newsletter subscriber management

### 5. **Modular JavaScript Architecture**
Separated monolithic JavaScript into 6 focused modules:
- **api.js** - Centralized API communication with token management
- **projects.js** - Project submission and management
- **team.js** - Team display and management
- **reviews.js** - Review submission and carousel
- **dashboard.js** - User dashboard and file management
- **admin.js** - Admin dashboard functions

### 6. **Enhanced Database Structure**
- New collections: `project_requests`, `team_members`
- Indexes for performance optimization
- Proper MongoDB integration with Motor (async driver)

---

## Frontend Integration Steps

### Step 1: Add Script Imports to index.html

Add these script imports before closing `</body>` tag in your HTML:

```html
<!-- Modular JavaScript Modules -->
<script src="js/api.js"></script>
<script src="js/projects.js"></script>
<script src="js/team.js"></script>
<script src="js/reviews.js"></script>
<script src="js/dashboard.js"></script>
<script src="js/admin.js"></script>
```

### Step 2: Create Project Submission Modal

Add this HTML section to your index.html (in the appropriate section for projects):

```html
<!-- Project Submission Modal -->
<div id="projectModal" class="modal" style="display: none;">
    <div class="modal-content" style="max-width: 700px;">
        <span class="close" onclick="projectsModule.closeProjectModal()">&times;</span>
        <h2>Submit Your Project</h2>
        
        <form id="projectSubmitForm" enctype="multipart/form-data">
            <div class="form-group">
                <label for="projectTitle">Project Title *</label>
                <input type="text" id="projectTitle" name="title" required minlength="5">
            </div>

            <div class="form-group">
                <label for="projectDescription">Description *</label>
                <textarea id="projectDescription" name="description" required minlength="20" rows="4"></textarea>
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label for="projectBudget">Budget ($) *</label>
                    <input type="number" id="projectBudget" name="budget" required min="0" step="100">
                </div>
                <div class="form-group">
                    <label for="projectDeadline">Deadline *</label>
                    <input type="datetime-local" id="projectDeadline" name="deadline" required>
                </div>
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label for="projectCategory">Category *</label>
                    <select id="projectCategory" name="category" required>
                        <option value="">Select Category</option>
                        <option value="web_app">Web App</option>
                        <option value="mobile_app">Mobile App</option>
                        <option value="ecommerce">E-commerce</option>
                        <option value="saas">SaaS</option>
                        <option value="startup">Startup</option>
                        <option value="enterprise">Enterprise</option>
                        <option value="other">Other</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="projectPriority">Priority *</label>
                    <select id="projectPriority" name="priority" required>
                        <option value="">Select Priority</option>
                        <option value="low">Low</option>
                        <option value="medium">Medium</option>
                        <option value="high">High</option>
                        <option value="urgent">Urgent</option>
                    </select>
                </div>
            </div>

            <div class="form-group">
                <label for="projectTechStack">Technology Stack *</label>
                <input type="text" id="projectTechStack" placeholder="Type technology and press Enter">
                <div id="techStackTags" style="margin-top: 10px; display: flex; flex-wrap: wrap; gap: 10px;"></div>
                <input type="hidden" name="tech_stack" value="">
            </div>

            <div class="form-group">
                <label for="projectNotes">Additional Notes</label>
                <textarea id="projectNotes" name="additional_notes" rows="3"></textarea>
            </div>

            <div class="form-group">
                <label for="projectFiles">Upload Files</label>
                <input type="file" id="projectFiles" name="files" multiple>
            </div>

            <button type="submit" class="btn-primary">Submit Project</button>
        </form>
    </div>
</div>
```

### Step 3: Create Review Submission Modal

Add this HTML to your reviews section:

```html
<!-- Review Submission Modal -->
<div id="reviewModal" class="modal" style="display: none;">
    <div class="modal-content" style="max-width: 600px;">
        <span class="close" onclick="reviewsModule.closeReviewModal()">&times;</span>
        <h2>Share Your Review</h2>
        
        <form id="reviewSubmitForm" enctype="multipart/form-data">
            <div class="form-group">
                <label for="authorName">Your Name *</label>
                <input type="text" id="authorName" name="author_name" required>
            </div>

            <div class="form-group">
                <label for="authorEmail">Your Email *</label>
                <input type="email" id="authorEmail" name="author_email" required>
            </div>

            <div class="form-group">
                <label for="reviewText">Your Review *</label>
                <textarea id="reviewText" name="text" required minlength="20" rows="5"></textarea>
            </div>

            <div class="form-group">
                <label for="reviewRating">Rating *</label>
                <select id="reviewRating" name="rating" required>
                    <option value="">Select Rating</option>
                    <option value="5">⭐⭐⭐⭐⭐ Excellent (5)</option>
                    <option value="4">⭐⭐⭐⭐ Very Good (4)</option>
                    <option value="3">⭐⭐⭐ Good (3)</option>
                    <option value="2">⭐⭐ Fair (2)</option>
                    <option value="1">⭐ Poor (1)</option>
                </select>
            </div>

            <div class="form-group">
                <label for="reviewImages">Images (Optional)</label>
                <input type="file" id="reviewImages" name="images" multiple accept="image/*">
            </div>

            <div class="form-group">
                <label for="reviewVideos">Videos (Optional)</label>
                <input type="file" id="reviewVideos" name="videos" multiple accept="video/*">
            </div>

            <button type="submit" class="btn-primary">Submit Review</button>
        </form>
    </div>
</div>

<!-- Review Carousel -->
<div id="reviewCarousel" style="margin: 40px 0;">
    <!-- Populated by reviewsModule -->
</div>
```

### Step 4: Create Team Section

Add this HTML to your team section:

```html
<section class="team-section">
    <div class="container">
        <h2>Our Team</h2>
        <p class="section-subtitle">Meet our talented professionals</p>
        
        <div id="teamGrid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; margin-top: 40px;">
            <!-- Team members populated by teamModule -->
        </div>
    </div>
</section>

<style>
.team-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 15px;
    padding: 30px;
    text-align: center;
    transition: all 0.3s ease;
}

.team-card:hover {
    border-color: var(--primary-color);
    box-shadow: 0 10px 30px rgba(139, 92, 246, 0.2);
}

.team-photo {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    margin: 0 auto 20px;
    object-fit: cover;
}

.team-role {
    color: var(--primary-color);
    font-weight: 600;
    margin: 10px 0;
}

.team-skills {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    margin: 15px 0;
}

.skill-tag {
    background: rgba(139, 92, 246, 0.2);
    color: var(--primary-color);
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.85em;
}
</style>
```

### Step 5: Create User Dashboard Page

Create a `dashboard.html` file:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Dashboard - VisionStack</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="dashboard-container">
        <aside class="dashboard-sidebar">
            <h2>Dashboard</h2>
            <ul class="dashboard-menu">
                <li><a href="#profile" class="menu-item active">Profile</a></li>
                <li><a href="#projects" class="menu-item">My Projects</a></li>
                <li><a href="#files" class="menu-item">Files</a></li>
                <li><a href="#settings" class="menu-item">Settings</a></li>
                <li><a href="#" onclick="dashboardModule.logout()" class="menu-item logout">Logout</a></li>
            </ul>
        </aside>

        <main class="dashboard-content">
            <div id="userInfo"></div>

            <section id="projects">
                <h3>My Projects</h3>
                <button onclick="projectsModule.openProjectModal()" class="btn-primary">Submit New Project</button>
                <div id="projectsContainer" style="margin-top: 20px;"></div>
            </section>

            <section id="files">
                <h3>My Files</h3>
                <button onclick="dashboardModule.openUploadModal()" class="btn-primary">Upload File</button>
                <div id="userFiles" style="margin-top: 20px;"></div>
            </section>
        </main>
    </div>

    <!-- Upload Modal -->
    <div id="uploadModal" class="modal" style="display: none;">
        <div class="modal-content">
            <span class="close" onclick="dashboardModule.closeUploadModal()">&times;</span>
            <h2>Upload File</h2>
            <form id="uploadForm">
                <div class="form-group">
                    <label for="fileInput">Select File *</label>
                    <input type="file" id="fileInput" required>
                </div>
                <button type="submit" class="btn-primary">Upload</button>
            </form>
        </div>
    </div>

    <script src="js/api.js"></script>
    <script src="js/projects.js"></script>
    <script src="js/dashboard.js"></script>
</body>
</html>
```

### Step 6: Create Admin Dashboard Page

Create an `admin-dashboard.html` file:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Dashboard - VisionStack</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="admin-dashboard">
        <header class="admin-header">
            <h1>Admin Dashboard</h1>
            <button onclick="adminModule.logout()" class="btn-danger">Logout</button>
        </header>

        <nav class="admin-tabs">
            <button class="admin-tab-btn active" data-tab="stats">Statistics</button>
            <button class="admin-tab-btn" data-tab="projects">Projects</button>
            <button class="admin-tab-btn" data-tab="reviews">Reviews</button>
            <button class="admin-tab-btn" data-tab="contacts">Contacts</button>
            <button class="admin-tab-btn" data-tab="users">Users</button>
        </nav>

        <!-- Statistics Tab -->
        <div id="tab-stats" class="admin-tab-content">
            <h2>Dashboard Statistics</h2>
            <div id="adminStats" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;"></div>
        </div>

        <!-- Projects Tab -->
        <div id="tab-projects" class="admin-tab-content" style="display: none;">
            <h2>Pending Projects</h2>
            <div id="pendingProjects"></div>
        </div>

        <!-- Reviews Tab -->
        <div id="tab-reviews" class="admin-tab-content" style="display: none;">
            <h2>Pending Reviews</h2>
            <div id="pendingReviews"></div>
        </div>

        <!-- Contacts Tab -->
        <div id="tab-contacts" class="admin-tab-content" style="display: none;">
            <h2>Contact Messages</h2>
            <div id="allContacts"></div>
        </div>

        <!-- Users Tab -->
        <div id="tab-users" class="admin-tab-content" style="display: none;">
            <h2>All Users</h2>
            <div id="allUsers"></div>
        </div>
    </div>

    <style>
    .admin-dashboard {
        padding: 20px;
    }

    .stat-card {
        background: rgba(139, 92, 246, 0.1);
        border: 1px solid var(--primary-color);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }

    .stat-card h3 {
        font-size: 2.5em;
        color: var(--primary-color);
        margin: 0;
    }

    .admin-item {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        margin: 10px 0;
        border-radius: 10px;
        border-left: 4px solid var(--primary-color);
    }

    .item-actions {
        margin-top: 15px;
        display: flex;
        gap: 10px;
    }
    </style>

    <script src="js/api.js"></script>
    <script src="js/admin.js"></script>
</body>
</html>
```

---

## Backend Integration

### 1. Start the Server

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database (one time)
python db_init.py

# Start the server
uvicorn main:app --reload
```

### 2. Database Collections

The following collections are automatically created and indexed:

- **users** - User accounts
- **projects_requests** (or **project_requests**) - Project submissions
- **team_members** - Team directory
- **reviews** - Customer reviews
- **contacts** - Contact form submissions
- **newsletters** - Newsletter subscribers
- **uploaded_files** - File storage metadata
- **admins** - Admin accounts

### 3. Environment Configuration

Ensure your `.env` file contains:

```env
MONGO_URL=mongodb+srv://VisionStack:vision123@cluster0.agln8yx.mongodb.net/?appName=Cluster0
DB_NAME=VisionStack
SECRET_KEY=visionstack-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
UPLOAD_DIR=uploads
ADMIN_SECRET_KEY=visionstack-admin-2025
```

---

## Testing the Features

### 1. Register and Login

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "password": "SecurePass123!"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123!"
  }'
```

### 2. Submit a Project

Use the frontend form in `dashboard.html` or:

```bash
curl -X POST http://localhost:8000/api/projects/submit \
  -H "Authorization: Bearer {token}" \
  -F "title=My Website" \
  -F "description=I need a professional website" \
  -F "budget=3000" \
  -F "deadline=2025-06-30T00:00:00" \
  -F "tech_stack=HTML,CSS,JavaScript" \
  -F "category=web_app" \
  -F "priority=high" \
  -F "user_email=john@example.com"
```

### 3. Admin Features

**Admin Login:**
```bash
curl -X POST http://localhost:8000/api/auth/admin/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "AdminPass123!"
  }'
```

**Get Dashboard Stats:**
```bash
curl http://localhost:8000/api/admin/dashboard/stats \
  -H "Authorization: Bearer {admin_token}"
```

---

## Production Deployment Checklist

- [ ] Change all default passwords and secret keys
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS for production domains
- [ ] Set up database backups
- [ ] Enable request logging and monitoring
- [ ] Implement rate limiting
- [ ] Add request validation
- [ ] Set up error tracking (Sentry, etc.)
- [ ] Configure CDN for static files
- [ ] Set up automated tests
- [ ] Configure production database
- [ ] Set up environment-specific `.env` files
- [ ] Enable database authentication
- [ ] Configure MongoDB IP whitelist
- [ ] Set up automated deployments (CI/CD)
- [ ] Add API documentation
- [ ] Set up user support email
- [ ] Configure email notifications
- [ ] Add analytics tracking
- [ ] Set up status page

---

## Troubleshooting

### Issue: "Admin access required"
**Solution:** Ensure you're logged in as admin and using the admin token, not user token.

### Issue: Files not uploading
**Solution:** Check that `uploads/` directory exists and has write permissions.

### Issue: MongoDB connection error
**Solution:** Verify `.env` credentials and ensure IP whitelist is configured in MongoDB Atlas.

### Issue: CORS errors
**Solution:** Check CORS middleware configuration in main.py.

---

## Support & Documentation

For more information, see:
- [API Documentation](API.md)
- [README.md](README.md)
- [Project structure guide](STRUCTURE.md)

---

**Version:** 1.0.0  
**Last Updated:** December 2024
