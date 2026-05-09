"""Routers module for VisionStack API"""
from .projects_router import router as projects_router
from .team_router import router as team_router
from .reviews_router import router as reviews_router
from .admin_router import router as admin_router

__all__ = [
    "projects_router",
    "team_router",
    "reviews_router",
    "admin_router",
]
