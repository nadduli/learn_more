#!/usr/bin/python3
"""User management routes"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas.user import UserResponse
from app.db.repositories.user_repository import UserRepository
from app.api.deps import CurrentUser

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_my_profile(current_user: CurrentUser):
    """
    Get current user's profile.
    
    Requires authentication.
    """
    return current_user
