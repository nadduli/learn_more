# app/dependencies.py
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.repositories.user_repository import UserRepository


async def get_user_repo(db: AsyncSession = Depends(get_db)):
    return UserRepository(db)
