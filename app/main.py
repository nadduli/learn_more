#!/usr/bin/python3
"""Entry point to the application"""

from fastapi import FastAPI
from app.api.v1.endpoints import users, auth
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title="Learn More API",
    description="Authentication and User Management API",
    version="1.0.0",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)


app.include_router(
    auth.router, 
    prefix=f"{settings.API_V1_STR}/auth", 
    tags=["Authentication"]
)
app.include_router(
    users.router, 
    prefix=f"{settings.API_V1_STR}/users", 
    tags=["Users"]
)


@app.get("/")
def read_root():
    """Root endpoint - API health check"""
    return {
        "message": "Learn More API is running",
        "version": "1.0.0",
        "docs": f"{settings.API_V1_STR}/docs"
    }
