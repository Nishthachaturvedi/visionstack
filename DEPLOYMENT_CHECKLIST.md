# VisionStack Production Deployment Checklist

## Pre-Deployment Review

### ✅ Code Review
- [x] All new routers created and tested
- [x] API endpoints documented
- [x] JavaScript modules are modular and reusable
- [x] Database schema is optimized
- [x] Error handling is comprehensive
- [x] Input validation is in place

### ✅ Documentation
- [x] API.md - Complete endpoint documentation
- [x] IMPLEMENTATION.md - Step-by-step integration guide
- [x] PRODUCTION_SUMMARY.md - Overview of changes
- [x] Code comments are clear and helpful
- [x] README.md explains the project

---

## Before Going Live

### 1. Security Configuration
- [ ] Change `SECRET_KEY` in `.env` (currently: `visionstack-secret-key-change-in-production`)
  ```env
  SECRET_KEY=your-secure-random-key-here
  ```
- [ ] Change `ADMIN_SECRET_KEY` in `.env`
  ```env
  ADMIN_SECRET_KEY=your-admin-key-here
  ```
- [ ] Verify MongoDB credentials are correct
  ```env
  MONGO_URL=your-production-connection-string
  ```
- [ ] Update ALGORITHM if needed (default: HS256)
- [ ] Set ACCESS_TOKEN_EXPIRE_MINUTES to appropriate value (default: 1440 = 24h)

### 2. Database Configuration
- [ ] Test MongoDB Atlas connection
  ```bash
  python -c "import asyncio; from database import Database; asyncio.run(Database.connect_db())"
  ```
- [ ] Configure IP whitelist in MongoDB Atlas
  - Go to MongoDB Atlas Dashboard
  - Network Access → IP Whitelist
  - Add your server's IP address
- [ ] Create database backups
- [ ] Verify all 9 collections exist after running:
  ```bash
  python db_init.py
  ```
- [ ] Test collection indexes are created
  ```bash
  python -c "import asyncio; from db_init import init_db; asyncio.run(init_db())"
  ```

### 3. Frontend Configuration
- [ ] Update API base URL if using custom domain
  ```javascript
  // In api.js, line 9:
  this.baseURL = 'https://your-domain.com/api';
  ```
- [ ] Test all JavaScript modules are loading
  - Check browser console for errors
  - Verify api.js initializes correctly
- [ ] Test form submissions
  - User registration
  - Project submission
  - Review submission
- [ ] Test file uploads
  - Test file size validation
  - Test file type validation
  - Verify uploads directory exists and is writable

### 4. Server Configuration
- [ ] Install all dependencies
  ```bash
  pip install -r requirements.txt
  ```
- [ ] Create uploads directory if it doesn't exist
  ```bash
  mkdir -p uploads
  chmod 755 uploads
  ```
- [ ] Set environment variables for production
  ```bash
  export ENVIRONMENT=production
  export LOG_LEVEL=INFO
  ```
- [ ] Configure uvicorn for production
  - Use appropriate worker count
  - Enable access logging
  - Set proper timeouts

### 5. CORS & Network
- [ ] Update CORS allowed origins in `main.py`
  ```python
  # Change from ["*"] to specific domains
  allow_origins=["https://yourdomain.com", "https://www.yourdomain.com"]
  ```
- [ ] Configure HTTPS/SSL certificate
- [ ] Set up domain DNS records
- [ ] Test CORS headers are correct

### 6. Testing & Validation
- [ ] Test all 40+ API endpoints
  ```bash
  # Example tests provided in API.md
  ```
- [ ] Test user registration workflow
  ```bash
  curl -X POST https://yourdomain.com/api/auth/register \
    -H "Content-Type: application/json" \
    -d '{"first_name": "Test", "last_name": "User", "email": "test@example.com", "password": "TestPass123!"}'
  ```
- [ ] Test admin features
  - Admin registration
  - Admin login
  - Dashboard access
- [ ] Test file uploads (images, videos, documents)
- [ ] Test database operations
  - Create, read, update, delete
  - Verify data persistence
- [ ] Test error handling
  - Invalid inputs
  - Unauthorized access
  - File upload limits
- [ ] Load testing
  - Simulate concurrent users
  - Monitor database performance
  - Check for memory leaks

### 7. Performance Optimization
- [ ] Enable caching headers for static files
- [ ] Configure CDN for static assets
- [ ] Set up database query monitoring
- [ ] Enable slow query logging
- [ ] Monitor API response times
- [ ] Test pagination performance
- [ ] Optimize images on homepage

### 8. Logging & Monitoring
- [ ] Set up request logging
  ```python
  # In main.py - add logging middleware
  ```
- [ ] Configure error tracking (e.g., Sentry)
- [ ] Set up performance monitoring
- [ ] Create admin alerts for critical errors
- [ ] Monitor database connection pool
- [ ] Log all admin actions

### 9. Backup & Disaster Recovery
- [ ] Configure automated MongoDB backups
  - Frequency: Daily
  - Retention: 30 days
  - Test restore process
- [ ] Backup uploaded files
  - Set up automated file backups
  - Test file recovery
- [ ] Document recovery procedures
- [ ] Create runbook for common issues

### 10. User Support
- [ ] Create support email address
  ```env
  SUPPORT_EMAIL=support@yourdomain.com
  ```
- [ ] Set up help documentation
- [ ] Create FAQ page
- [ ] Set up contact form responses
- [ ] Establish SLA for support response
- [ ] Create admin notification system

### 11. Analytics & Metrics
- [ ] Set up Google Analytics / custom analytics
- [ ] Monitor user registration trends
- [ ] Track feature usage
- [ ] Monitor API endpoint usage
- [ ] Create admin dashboard metrics
- [ ] Set up performance alerts

---

## Deployment Steps

### Step 1: Prepare Production Server
```bash
# SSH into production server
ssh user@your-production-server

# Clone repository
git clone https://github.com/yourusername/visionstack.git
cd visionstack

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment
```bash
# Create .env file for production
nano .env

# Add production values:
# MONGO_URL=your-production-db-url
# SECRET_KEY=your-secure-key
# ENVIRONMENT=production
```

### Step 3: Initialize Database
```bash
# Run one-time database initialization
python db_init.py

# You should see:
# ✅ Connected to MongoDB successfully
# ✅ Database initialization completed successfully!
```

### Step 4: Start Server
```bash
# Option A: Development (for testing)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Option B: Production (with Gunicorn)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 main:app

# Option C: Production (with Systemd)
# Create /etc/systemd/system/visionstack.service
# (See template below)
sudo systemctl start visionstack
```

### Step 5: Set up Reverse Proxy (Nginx)
```nginx
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /uploads/ {
        alias /path/to/visionstack/uploads/;
        expires 30d;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

### Step 6: Set up SSL Certificate
```bash
# Using Let's Encrypt with Certbot
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

### Step 7: Create Systemd Service (Optional)
```ini
# /etc/systemd/system/visionstack.service
[Unit]
Description=VisionStack API Server
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/home/username/visionstack
Environment="PATH=/home/username/visionstack/venv/bin"
ExecStart=/home/username/visionstack/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 main:app
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

Then enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable visionstack
sudo systemctl start visionstack
```

---

## Post-Deployment Verification

### ✅ Smoke Tests
- [ ] Homepage loads correctly
- [ ] Can access `/api/health` endpoint
- [ ] Database connection works
- [ ] File uploads work
- [ ] Forms submit successfully

### ✅ Functional Tests
```bash
# Test registration
curl -X POST https://yourdomain.com/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Test","last_name":"User","email":"test@example.com","password":"TestPass123!"}'

# Test login
curl -X POST https://yourdomain.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestPass123!"}'

# Test project submission
# (See API.md for full request)

# Test admin dashboard
curl https://yourdomain.com/api/admin/dashboard/stats \
  -H "Authorization: Bearer {admin_token}"
```

### ✅ Performance Checks
- [ ] Page load time < 3 seconds
- [ ] API response time < 500ms
- [ ] Database queries < 100ms
- [ ] File upload < 10MB/second
- [ ] Concurrent user test (100+ users)

### ✅ Security Checks
- [ ] HTTPS/SSL working
- [ ] Passwords not visible in logs
- [ ] Database credentials not exposed
- [ ] CORS headers correct
- [ ] Admin endpoints require authentication
- [ ] File upload validation working
- [ ] SQL injection prevention working
- [ ] CSRF protection in place

---

## Monitoring & Maintenance

### Daily
- [ ] Check error logs
- [ ] Monitor database performance
- [ ] Monitor server resources (CPU, memory, disk)
- [ ] Check API response times

### Weekly
- [ ] Review admin dashboard metrics
- [ ] Check user registration trends
- [ ] Monitor file storage usage
- [ ] Review support tickets

### Monthly
- [ ] Update dependencies
  ```bash
  pip list --outdated
  pip install --upgrade package-name
  ```
- [ ] Test backup/restore procedures
- [ ] Optimize slow queries
- [ ] Review security logs
- [ ] Plan feature releases

### Quarterly
- [ ] Security audit
- [ ] Performance optimization review
- [ ] Capacity planning
- [ ] Architecture review

---

## Troubleshooting Quick Links

| Issue | Solution |
|-------|----------|
| 502 Bad Gateway | Check if API server is running: `systemctl status visionstack` |
| 404 Not Found | Verify API endpoint exists in API.md |
| 401 Unauthorized | Check JWT token validity and expiration |
| 403 Forbidden | Verify user has admin role for admin endpoints |
| CORS Error | Check CORS configuration in main.py |
| File Upload Failed | Check uploads directory permissions and disk space |
| Database Connection Error | Verify MongoDB Atlas IP whitelist and connection string |
| Slow API Response | Check MongoDB indexes and query performance |

---

## Success Indicators

You'll know deployment is successful when:
- ✅ All endpoints respond with correct status codes
- ✅ Database operations complete without errors
- ✅ File uploads work for all supported formats
- ✅ Admin dashboard displays correct statistics
- ✅ Users can register, login, and submit projects
- ✅ Project approval workflow functions correctly
- ✅ Performance metrics are within acceptable ranges
- ✅ No security warnings in logs
- ✅ Backups are running automatically
- ✅ Monitoring alerts are configured

---

## Rollback Plan

If issues occur post-deployment:

1. **Quick Rollback (< 1 minute)**
   ```bash
   sudo systemctl stop visionstack
   git revert HEAD  # Or checkout previous version
   python db_init.py  # Reinitialize if needed
   sudo systemctl start visionstack
   ```

2. **Database Rollback**
   - Restore from automated backup
   - Verify data integrity
   - Test functionality

3. **Communication**
   - Notify users of downtime
   - Provide status updates
   - Send all-clear notification once resolved

---

## Contact & Escalation

**Deployment Team Lead:** [Your name]  
**On-Call Support:** [On-call email/phone]  
**Emergency Contact:** [Emergency contact]  

---

**Last Updated:** December 2024  
**Status:** Ready for Production Deployment
