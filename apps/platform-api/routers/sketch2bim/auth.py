"""
Authentication routes
Token validation and user info
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from database.sketch2bim import get_db
from auth.sketch2bim import get_current_user
from models.sketch2bim import User
from models.sketch2bim_schemas import UserResponse, UserUpdate

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    user: User = Depends(get_current_user)
):
    """Get current user information"""
    return user


@router.patch("/me", response_model=UserResponse)
def update_current_user(
    user_data: UserUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user information"""
    if user_data.name is not None:
        user.name = user_data.name
    if user_data.credits is not None:
        # Only allow admins to update credits directly
        # For regular users, credits are managed through payments
        pass
    if user_data.subscription_tier is not None:
        # Only allow admins to update subscription tier directly
        # For regular users, subscription tier is managed through Razorpay
        pass
    db.commit()
    db.refresh(user)
    return user

