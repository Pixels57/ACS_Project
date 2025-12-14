"""
Authentication routes
VULNERABLE: Broken Authentication implementation
"""

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
from database import get_db
from models.user import User, UserRole
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import hashlib  # VULNERABLE: Using weak hashing (MD5)

router = APIRouter()


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenRequest(BaseModel):
    email: str
    password: str


class PasswordResetRequest(BaseModel):
    email: str


# VULNERABLE: Weak password hashing (MD5)
def hash_password(password: str) -> str:
    """Hash password using MD5 - VULNERABLE"""
    return hashlib.md5(password.encode()).hexdigest()


# VULNERABLE: No password complexity requirements
def validate_password(password: str) -> bool:
    """Password validation - VULNERABLE: No complexity requirements"""
    return len(password) > 0  # Accepts any non-empty password


@router.post("/login")
async def login(
    login_data: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Login endpoint
    VULNERABLE: Weak password hashing, no rate limiting, session fixation
    """
    # Find user
    user = db.query(User).filter(User.email == login_data.email).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # VULNERABLE: Compare with MD5 hash
    password_hash = hash_password(login_data.password)
    if user.password_hash != password_hash:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # VULNERABLE: Session cookie without HttpOnly and Secure flags
    # This will be set in the actual implementation
    response.set_cookie(
        key="sid",
        value=f"session_{user.id}",  # VULNERABLE: Predictable session ID
        # Missing: httponly=True, secure=True, samesite="Strict"
        max_age=86400  # 24 hours
    )
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    return {
        "message": "Login successful",
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role.value
        }
    }


@router.post("/logout")
async def logout(response: Response):
    """Logout endpoint"""
    response.delete_cookie(key="sid")
    return {"message": "Logout successful"}


@router.post("/token")
async def get_token(
    token_data: TokenRequest,
    db: Session = Depends(get_db)
):
    """
    Generate JWT token for API clients
    VULNERABLE: Weak token signing, no expiration
    """
    user = db.query(User).filter(User.email == token_data.email).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    password_hash = hash_password(token_data.password)
    if user.password_hash != password_hash:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # VULNERABLE: Simple token generation (should use proper JWT)
    import base64
    token_data = f"{user.id}:{user.email}:{user.role.value}"
    token = base64.b64encode(token_data.encode()).decode()
    
    return {"token": token, "type": "Bearer"}


@router.post("/reset-password")
async def reset_password(
    reset_data: PasswordResetRequest,
    db: Session = Depends(get_db)
):
    """
    Password reset endpoint
    VULNERABLE: Weak reset mechanism
    """
    user = db.query(User).filter(User.email == reset_data.email).first()
    
    if user:
        # VULNERABLE: In production, this should send an email
        # For now, just return success (information disclosure)
        return {
            "message": "If account exists, reset link sent",
            "user_id": user.id  # VULNERABLE: Information disclosure
        }
    
    return {"message": "If account exists, reset link sent"}

