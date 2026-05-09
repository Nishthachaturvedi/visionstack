#!/usr/bin/env python3
"""
VisionStack Setup Verification Script
Verifies that all files and dependencies are in place
"""

import os
import sys
import importlib
from pathlib import Path

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def check_file(filepath, description):
    """Check if a file exists"""
    if os.path.isfile(filepath):
        print(f"✅ {description}")
        return True
    else:
        print(f"❌ {description} - NOT FOUND: {filepath}")
        return False

def check_directory(dirpath, description):
    """Check if a directory exists"""
    if os.path.isdir(dirpath):
        print(f"✅ {description}")
        return True
    else:
        print(f"❌ {description} - NOT FOUND: {dirpath}")
        return False

def check_module(module_name, description):
    """Check if a Python module is installed"""
    try:
        importlib.import_module(module_name)
        print(f"✅ {description}")
        return True
    except ImportError:
        print(f"❌ {description} - NOT INSTALLED")
        return False

def main():
    print_header("VisionStack Setup Verification")
    
    all_checks_passed = True
    
    # Check Python Version
    print("Python Version Check:")
    py_version = sys.version_info
    if py_version.major >= 3 and py_version.minor >= 9:
        print(f"✅ Python {py_version.major}.{py_version.minor} (required: 3.9+)")
    else:
        print(f"❌ Python {py_version.major}.{py_version.minor} (required: 3.9+)")
        all_checks_passed = False
    
    # Check Root Files
    print_header("Root Files")
    root_files = [
        ("main.py", "main.py - FastAPI application"),
        ("config.py", "config.py - Configuration"),
        ("database.py", "database.py - Database connection"),
        ("models.py", "models.py - Original data models"),
        ("models_v2.py", "models_v2.py - Enhanced data models"),
        ("db_init.py", "db_init.py - Database initialization"),
        ("requirements.txt", "requirements.txt - Dependencies"),
        (".env", ".env - Environment variables"),
        ("index.html", "index.html - Frontend"),
    ]
    
    for filepath, description in root_files:
        if not check_file(filepath, description):
            all_checks_passed = False
    
    # Check Routers
    print_header("Router Files")
    routers = [
        ("routers/__init__.py", "routers/__init__.py"),
        ("routers/projects_router.py", "projects_router.py"),
        ("routers/team_router.py", "team_router.py"),
        ("routers/reviews_router.py", "reviews_router.py"),
        ("routers/admin_router.py", "admin_router.py"),
    ]
    
    for filepath, description in routers:
        if not check_file(filepath, description):
            all_checks_passed = False
    
    # Check JavaScript Modules
    print_header("JavaScript Modules")
    js_files = [
        ("js/api.js", "api.js - API client"),
        ("js/projects.js", "projects.js - Project management"),
        ("js/team.js", "team.js - Team management"),
        ("js/reviews.js", "reviews.js - Review management"),
        ("js/dashboard.js", "dashboard.js - User dashboard"),
        ("js/admin.js", "admin.js - Admin dashboard"),
    ]
    
    for filepath, description in js_files:
        if not check_file(filepath, description):
            all_checks_passed = False
    
    # Check Documentation
    print_header("Documentation Files")
    docs = [
        ("README.md", "README.md - Project overview"),
        ("QUICKSTART.md", "QUICKSTART.md - Quick start guide"),
        ("SETUP_COMPLETE.md", "SETUP_COMPLETE.md - Setup notes"),
        ("API.md", "API.md - API documentation"),
        ("IMPLEMENTATION.md", "IMPLEMENTATION.md - Integration guide"),
        ("PRODUCTION_SUMMARY.md", "PRODUCTION_SUMMARY.md - Production overview"),
        ("DEPLOYMENT_CHECKLIST.md", "DEPLOYMENT_CHECKLIST.md - Deployment guide"),
        ("DOCUMENTATION_INDEX.md", "DOCUMENTATION_INDEX.md - Documentation index"),
    ]
    
    for filepath, description in docs:
        if not check_file(filepath, description):
            all_checks_passed = False
    
    # Check Directories
    print_header("Directories")
    directories = [
        ("routers", "routers/ - Router modules"),
        ("js", "js/ - JavaScript modules"),
        ("uploads", "uploads/ - File uploads"),
    ]
    
    for dirpath, description in directories:
        if not check_directory(dirpath, description):
            all_checks_passed = False
    
    # Check Python Packages
    print_header("Python Packages")
    packages = [
        ("fastapi", "FastAPI - Web framework"),
        ("uvicorn", "Uvicorn - ASGI server"),
        ("motor", "Motor - Async MongoDB driver"),
        ("pymongo", "PyMongo - MongoDB driver"),
        ("pydantic", "Pydantic - Data validation"),
        ("jose", "python-jose - JWT tokens"),
        ("passlib", "passlib - Password hashing"),
        ("dotenv", "python-dotenv - Environment variables"),
    ]
    
    for package, description in packages:
        if not check_module(package, description):
            all_checks_passed = False
    
    # Check Environment Variables
    print_header("Environment Variables")
    env_vars = [
        ("MONGO_URL", "MongoDB connection string"),
        ("DB_NAME", "Database name"),
        ("SECRET_KEY", "JWT secret key"),
    ]
    
    for env_var, description in env_vars:
        if os.getenv(env_var):
            print(f"✅ {description}")
        else:
            print(f"⚠️  {description} - Not set in environment")
    
    # File Content Checks
    print_header("File Content Verification")
    
    # Check if main.py imports routers
    with open("main.py", "r") as f:
        main_content = f.read()
        if "from routers import" in main_content or "import routers" in main_content:
            print("✅ main.py imports routers")
        else:
            print("❌ main.py doesn't import routers")
            all_checks_passed = False
    
    # Check if models_v2.py has ProjectCreate
    with open("models_v2.py", "r") as f:
        models_content = f.read()
        if "class ProjectCreate" in models_content:
            print("✅ models_v2.py has ProjectCreate model")
        else:
            print("❌ models_v2.py missing ProjectCreate model")
            all_checks_passed = False
    
    # Check if database.py has get_team_collection
    with open("database.py", "r") as f:
        db_content = f.read()
        if "def get_team_collection" in db_content:
            print("✅ database.py has get_team_collection function")
        else:
            print("❌ database.py missing get_team_collection function")
            all_checks_passed = False
    
    # Check if api.js has API client
    with open("js/api.js", "r") as f:
        api_content = f.read()
        if "class APIClient" in api_content:
            print("✅ api.js has APIClient class")
        else:
            print("❌ api.js missing APIClient class")
            all_checks_passed = False
    
    # Summary
    print_header("Verification Summary")
    
    if all_checks_passed:
        print("✅ All checks passed!")
        print("\n🎉 VisionStack is ready to run!")
        print("\nNext steps:")
        print("1. Configure .env file with MongoDB credentials")
        print("2. Run: python db_init.py")
        print("3. Run: uvicorn main:app --reload")
        print("4. Visit: http://localhost:8000")
        return 0
    else:
        print("❌ Some checks failed. Please review the issues above.")
        print("\nTo fix:")
        print("1. Install missing packages: pip install -r requirements.txt")
        print("2. Create missing directories: mkdir -p routers js uploads")
        print("3. Download missing files from repository")
        return 1

if __name__ == "__main__":
    sys.exit(main())
