"""
Referral system routes
REST API for generating referral links and tracking referrals
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict
import secrets
import string
from loguru import logger

from ..database import get_db
from ..auth import get_current_user
from ..models import User, Referral
from ..exceptions import NotFoundError, ValidationError

router = APIRouter(prefix="/referrals", tags=["referrals"])


def generate_referral_code() -> str:
    """Generate a unique referral code"""
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(8))


@router.post("/generate")
async def generate_referral(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, str]:
    """
    Generate a unique referral link for the current user
    
    Returns:
        Dictionary with referral_code and referral_url
    """
    # Check if user already has an active referral code
    existing = db.query(Referral).filter(
        Referral.referrer_id == user.id,
        Referral.status == "pending"
    ).first()
    
    if existing:
        referral_code = existing.referral_code
    else:
        # Generate new referral code
        referral_code = generate_referral_code()
        
        # Ensure uniqueness
        while db.query(Referral).filter(Referral.referral_code == referral_code).first():
            referral_code = generate_referral_code()
        
        # Create referral record
        referral = Referral(
            referrer_id=user.id,
            referral_code=referral_code,
            status="pending"
        )
        db.add(referral)
        db.commit()
    
    # Generate referral URL
    from ..config import settings
    referral_url = f"{settings.FRONTEND_URL}?ref={referral_code}"
    
    return {
        "referral_code": referral_code,
        "referral_url": referral_url
    }


@router.get("/stats")
async def get_referral_stats(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, int]:
    """
    Get referral statistics for the current user
    
    Returns:
        Dictionary with total_referrals, completed_referrals, credits_earned
        
    Note: credits_earned is kept for historical/analytics purposes only.
    Credits are no longer used for access control.
    """
    total = db.query(Referral).filter(Referral.referrer_id == user.id).count()
    completed = db.query(Referral).filter(
        Referral.referrer_id == user.id,
        Referral.status == "completed"
    ).count()
    
    credits_earned = db.query(func.sum(Referral.credits_awarded)).filter(
        Referral.referrer_id == user.id
    ).scalar() or 0
    
    return {
        "total_referrals": total,
        "completed_referrals": completed,
        "credits_earned": int(credits_earned)
    }


@router.get("/code")
async def get_referral_code(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, str]:
    """
    Get existing referral code or generate a new one
    """
    existing = db.query(Referral).filter(
        Referral.referrer_id == user.id,
        Referral.status == "pending"
    ).first()
    
    if existing:
        from ..config import settings
        referral_url = f"{settings.FRONTEND_URL}?ref={existing.referral_code}"
        return {
            "referral_code": existing.referral_code,
            "referral_url": referral_url
        }
    else:
        # Generate new one
        return await generate_referral(user, db)

