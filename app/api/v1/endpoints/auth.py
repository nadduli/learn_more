#!/usr/bin/python3
"""Authentication endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.db.database import get_db
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse
from app.db.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.core.security import verify_password, create_access_token
from app.api.deps import CurrentUser

router = APIRouter()


async def get_user_service(session: AsyncSession = Depends(get_db)) -> UserService:
    """
    Dependency helper to initialize the Service with the Repository
    and Database session.
    """
    repo = UserRepository(session)
    return UserService(repo)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate, 
    service: UserService = Depends(get_user_service)
):
    """
    Register a new user.
    
    - **email**: Valid email address
    - **password**: Minimum 8 characters
    - **full_name**: User's full name
    - **phone**: Optional phone number
    - **role_id**: UUID of the role to assign
    """
    return await service.register_user(user_in.model_dump())


@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_db)
):
    """
    OAuth2 compatible token login.
    
    - **username**: User's email address
    - **password**: User's password
    
    Returns an access token for authentication.
    """
    user_repo = UserRepository(session)
    user = await user_repo.get_by_email(form_data.username)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.email})
    
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: CurrentUser):
    """
    Get current authenticated user information.
    
    Requires authentication token in the Authorization header.
    """
    return current_user


@router.post("/refresh", response_model=Token)
async def refresh_token(current_user: CurrentUser):
    """
    Refresh access token.
    
    Requires a valid authentication token.
    Returns a new access token.
    """
    access_token = create_access_token(data={"sub": current_user.email})
    return Token(access_token=access_token, token_type="bearer")
