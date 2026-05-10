"""Core application configuration and security"""
from app.core.config import settings
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user,
    get_current_admin,
    get_current_faculty,
    get_current_student
)
from app.core.database import db, get_db

__all__ = [
    "settings",
    "hash_password",
    "verify_password",
    "create_access_token",
    "create_refresh_token",
    "decode_token",
    "get_current_user",
    "get_current_admin",
    "get_current_faculty",
    "get_current_student",
    "db",
    "get_db"
]
