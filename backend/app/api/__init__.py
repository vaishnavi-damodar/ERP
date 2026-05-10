"""API router initialization"""
from fastapi import APIRouter
from app.api.routes import auth, admin, faculty, student

api_router = APIRouter()

# Include routers
api_router.include_router(auth.router)
api_router.include_router(admin.router)
api_router.include_router(faculty.router)
api_router.include_router(student.router)

__all__ = ["api_router"]
