#!/usr/bin/python3
"""security module"""

from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from .config import get_settings
from jose import jwt

settings = get_settings()

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash the password"""
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> str:
    """verify password"""
    return pwd_context.verify(password, hashed)


def create_access_token(data: dict) -> str:
    """create access token"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt
