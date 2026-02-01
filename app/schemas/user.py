#!/usr/bin/python3
"""User Schema"""

from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str
    phone: Optional[str] = None
    role_id: UUID


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str
    is_active: bool
    role_id: UUID

    class Config:
        from_attributes = True
