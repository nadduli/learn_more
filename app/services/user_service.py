#!/usr/bin/python3
"""user service"""

from app.db.repositories.user_repository import UserRepository
from app.models.user import User
from app.core.security import hash_password
from fastapi import HTTPException, status
import uuid


class UserService:
    """user service class"""

    def __init__(self, user_repo: UserRepository):
        """Initialize user repository"""
        self.user_repo = user_repo

    async def register_user(self, user_data: dict) -> User:
        """Register new user"""
        existing_user = await self.user_repo.get_by_email(user_data["email"])
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        hashed_pwd = hash_password(user_data.pop("password"))

        new_user = User(**user_data, hashed_password=hashed_pwd)

        return await self.user_repo.create(new_user)
