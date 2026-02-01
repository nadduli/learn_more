#!/usr/bin/python3
"""Token schemas"""

from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Token payload schema"""
    sub: Optional[str] = None  # subject (user email)
    exp: Optional[int] = None  # expiration time
