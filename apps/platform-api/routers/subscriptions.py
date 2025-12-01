"""
Unified Subscription Router
Handles platform-wide subscription management for KVSHVL Platform
Uses platform-wide Razorpay configuration and ASK database for user management
"""

from fastapi import APIRouter, HTTPException, Depends, Header, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import razorpay
import json
import os
import logging
from datetime import datetime
from typing import Optional

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import ASK database/auth/models (platform subscriptions use ASK's user table)
from api.database import get_db
from api.models_db import User, Payment
from api.auth import get_current_user
from shared_backend.subscription.utils import (
    calculate_expiry,
    ensure_subscription_status,
    is_paid_tier,
    has_active_subscription
)

router = APIRouter()
log = logging.getLogger(__name__)

# Configure Razorpay using platform-wide environment variables
PLATFORM_RAZORPAY_KEY_ID = os.getenv("PLATFORM_RAZORPAY_KEY_ID", "")
PLATFORM_RAZORPAY_KEY_SECRET = os.getenv("PLATFORM_RAZORPAY_KEY_SECRET", "")
PLATFORM_RAZORPAY_WEBHOOK_SECRET = os.getenv("PLATFORM_RAZORPAY_WEBHOOK_SECRET", "")
PLATFORM_RAZORPAY_PLAN_WEEK = os.getenv("PLATFORM_RAZORPAY_PLAN_WEEK", "")
PLATFORM_RAZORPAY_PLAN_MONTH = os.getenv("PLATFORM_RAZORPAY_PLAN_MONTH", "")
PLATFORM_RAZORPAY_PLAN_YEAR = os.getenv("PLATFORM_RAZORPAY_PLAN_YEAR", "")

# Pricing amounts in paise (₹1 = 100 paise)
# These should match the plan amounts in Razorpay
PLATFORM_RAZORPAY_WEEK_AMOUNT = int(os.getenv("PLATFORM_RAZORPAY_WEEK_AMOUNT", "129900"))
PLATFORM_RAZORPAY_MONTH_AMOUNT = int(os.getenv("PLATFORM_RAZORPAY_MONTH_AMOUNT", "349900"))
PLATFORM_RAZORPAY_YEAR_AMOUNT = int(os.getenv("PLATFORM_RAZORPAY_YEAR_AMOUNT", "2999900"))

# Frontend URL for redirects
PLATFORM_FRONTEND_URL = os.getenv("PLATFORM_FRONTEND_URL", "https://kvshvl.in")

# Initialize Razorpay client
razorpay_client = None
if PLATFORM_RAZORPAY_KEY_ID and PLATFORM_RAZORPAY_KEY_SECRET:
    razorpay_client = razorpay.Client(auth=(PLATFORM_RAZORPAY_KEY_ID, PLATFORM_RAZORPAY_KEY_SECRET))


def verify_razorpay_webhook_signature(payload: str, signature: str) -> bool:
    """
    Verify Razorpay webhook signature
    """
    if not PLATFORM_RAZORPAY_WEBHOOK_SECRET or not razorpay_client:
        return False
    
    try:
        razorpay_client.utility.verify_webhook_signature(
            payload,
            signature,
            PLATFORM_RAZORPAY_WEBHOOK_SECRET
        )
        return True
    except Exception as e:
        log.error(f"Webhook signature verification failed: {e}")
        return False


@router.get("/status")
async def get_subscription_status(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's platform-wide subscription status
    """
    # Ensure subscription status is up to date
    ensure_subscription_status(user, db)
    db.refresh(user)
    
    return {
        "tier": user.subscription_tier or "trial",
        "status": user.subscription_status or "inactive",
        "expires_at": user.subscription_expires_at.isoformat() if user.subscription_expires_at else None,
        "plan_name": user.subscription_tier,
        "auto_renew": user.subscription_auto_renew or False,
        "has_active_subscription": has_active_subscription(user)
    }


@router.post("/checkout")
async def create_checkout_session(
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create Razorpay checkout session for platform subscription
    Expects JSON body with: {"tier": "week" | "monthly" | "yearly"}
    """
    if not razorpay_client:
        raise HTTPException(status_code=500, detail="Razorpay not configured")
    
    try:
        body = await request.json()
        tier = body.get("tier", "").lower()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid request body")
    
    if tier not in ["week", "monthly", "yearly"]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid tier. Expected one of: week, monthly, yearly. Got: {tier}"
        )
    
    base_url = PLATFORM_FRONTEND_URL
    cancel_url = f"{base_url}/subscribe?checkout=canceled"
    
    try:
        # Create subscription using Plan ID
        plan_map = {
            "week": PLATFORM_RAZORPAY_PLAN_WEEK,
            "monthly": PLATFORM_RAZORPAY_PLAN_MONTH,
            "yearly": PLATFORM_RAZORPAY_PLAN_YEAR,
        }
        
        plan_id = plan_map.get(tier)
        if not plan_id:
            raise HTTPException(
                status_code=400,
                detail=f"Plan not configured for tier: {tier}. Please configure Razorpay plan IDs."
            )
        
        # Create customer if doesn't exist
        customer_id = user.razorpay_customer_id
        if not customer_id:
            customer = razorpay_client.customer.create({
                "name": user.name or user.email.split("@")[0],
                "email": user.email,
                "contact": None
            })
            customer_id = customer["id"]
            user.razorpay_customer_id = customer_id
            db.commit()
        
        # Create subscription
        subscription_data = {
            "plan_id": plan_id,
            "customer_notify": 1,
            "total_count": 0,  # 0 = infinite recurring
            "notes": {
                "user_id": str(user.id),
                "user_email": user.email,
                "tier": tier,
                "platform": "kvshvl"
            }
        }
        
        subscription = razorpay_client.subscription.create(data=subscription_data)
        
        return {
            "subscription_id": subscription["id"],
            "plan_id": plan_id,
            "amount": subscription["plan"]["amount"],
            "currency": subscription["plan"]["currency"],
            "key_id": PLATFORM_RAZORPAY_KEY_ID,
            "name": "KVSHVL Platform",
            "description": f"{tier.title()} subscription (auto-renews) - Access to all apps",
            "prefill": {
                "email": user.email,
                "name": user.name or user.email.split("@")[0]
            },
            "theme": {
                "color": "#6366f1"
            },
            "success_url": f"{base_url}/account?checkout=success",
            "cancel_url": cancel_url,
            "payment_type": "subscription"
        }
    
    except razorpay.errors.BadRequestError as e:
        raise HTTPException(status_code=400, detail=f"Razorpay error: {str(e)}")
    except Exception as e:
        log.error(f"Checkout error: {e}")
        raise HTTPException(status_code=500, detail=f"Payment error: {str(e)}")


@router.post("/cancel")
async def cancel_subscription(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cancel user's platform subscription
    Cancels at end of billing cycle (user keeps access until period ends)
    """
    if not razorpay_client:
        raise HTTPException(status_code=500, detail="Razorpay not configured")
    
    if not user.razorpay_subscription_id:
        raise HTTPException(status_code=404, detail="No active subscription found")
    
    try:
        # Cancel subscription at period end
        subscription = razorpay_client.subscription.cancel(user.razorpay_subscription_id, {
            "cancel_at_cycle_end": 1  # Cancel at end of billing cycle
        })
        
        user.subscription_auto_renew = False
        user.subscription_status = "cancelled"
        db.commit()
        
        return {
            "status": "success",
            "message": "Subscription will be cancelled at end of billing cycle",
            "subscription": subscription
        }
    except razorpay.errors.BadRequestError as e:
        raise HTTPException(status_code=400, detail=f"Razorpay error: {str(e)}")
    except Exception as e:
        log.error(f"Cancel subscription error: {e}")
        raise HTTPException(status_code=500, detail=f"Error cancelling subscription: {str(e)}")


@router.post("/resume")
async def resume_subscription(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Resume a cancelled subscription
    Only works if subscription was cancelled but hasn't ended yet
    """
    if not razorpay_client:
        raise HTTPException(status_code=500, detail="Razorpay not configured")
    
    if not user.razorpay_subscription_id:
        raise HTTPException(status_code=404, detail="No subscription found")
    
    try:
        # Fetch subscription from Razorpay
        subscription = razorpay_client.subscription.fetch(user.razorpay_subscription_id)
        
        # Check if subscription can be resumed
        if subscription.get("status") not in ["cancelled", "paused"]:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot resume subscription with status: {subscription.get('status')}"
            )
        
        # Resume subscription
        subscription = razorpay_client.subscription.resume(user.razorpay_subscription_id, {
            "resume_at": "now"  # Resume immediately
        })
        
        user.subscription_auto_renew = True
        user.subscription_status = "active"
        db.commit()
        
        return {
            "status": "success",
            "message": "Subscription resumed successfully",
            "subscription": subscription
        }
    except razorpay.errors.BadRequestError as e:
        raise HTTPException(status_code=400, detail=f"Razorpay error: {str(e)}")
    except Exception as e:
        log.error(f"Resume subscription error: {e}")
        raise HTTPException(status_code=500, detail=f"Error resuming subscription: {str(e)}")


@router.post("/webhook")
async def razorpay_webhook(
    request: Request,
    x_razorpay_signature: str = Header(None, alias="x-razorpay-signature"),
    db: Session = Depends(get_db)
):
    """
    Handle Razorpay webhook events for platform subscriptions
    Processes: subscription.created, subscription.charged, subscription.cancelled, payment.captured
    """
    payload_bytes = await request.body()
    payload_str = payload_bytes.decode('utf-8')
    
    # Verify webhook signature
    if not x_razorpay_signature:
        raise HTTPException(status_code=400, detail="Missing webhook signature")
    
    if not verify_razorpay_webhook_signature(payload_str, x_razorpay_signature):
        raise HTTPException(status_code=400, detail="Invalid webhook signature")
    
    try:
        event = json.loads(payload_str)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    
    event_type = event.get("event")
    log.info(f"Processing webhook event: {event_type}")
    
    # Map Razorpay amounts to tiers
    AMOUNT_TO_TIER = {
        PLATFORM_RAZORPAY_WEEK_AMOUNT: "week",
        PLATFORM_RAZORPAY_MONTH_AMOUNT: "monthly",
        PLATFORM_RAZORPAY_YEAR_AMOUNT: "yearly",
    }
    
    # Handle subscription.created
    if event_type == "subscription.created":
        subscription_data = event.get("payload", {}).get("subscription", {}).get("entity", {})
        subscription_id = subscription_data.get("id")
        customer_id = subscription_data.get("customer_id")
        plan_id = subscription_data.get("plan_id")
        notes = subscription_data.get("notes", {})
        user_id = notes.get("user_id")
        
        # Find user by customer_id or user_id from notes
        user = None
        if user_id:
            user = db.query(User).filter(User.id == int(user_id)).first()
        if not user and customer_id:
            user = db.query(User).filter(User.razorpay_customer_id == customer_id).first()
        
        if user:
            # Determine tier from plan_id
            tier = None
            if plan_id == PLATFORM_RAZORPAY_PLAN_WEEK:
                tier = "week"
            elif plan_id == PLATFORM_RAZORPAY_PLAN_MONTH:
                tier = "monthly"
            elif plan_id == PLATFORM_RAZORPAY_PLAN_YEAR:
                tier = "yearly"
            
            if tier:
                user.razorpay_subscription_id = subscription_id
                user.subscription_tier = tier
                user.subscription_status = "active"
                user.subscription_auto_renew = True
                # Set expiry based on current period end
                current_end = subscription_data.get("current_end")
                if current_end:
                    user.subscription_expires_at = datetime.fromtimestamp(current_end)
                else:
                    user.subscription_expires_at = calculate_expiry(tier)
                db.commit()
    
    # Handle subscription.charged (renewal)
    elif event_type == "subscription.charged":
        subscription_data = event.get("payload", {}).get("subscription", {}).get("entity", {})
        subscription_id = subscription_data.get("id")
        payment_data = event.get("payload", {}).get("payment", {}).get("entity", {})
        payment_id = payment_data.get("id")
        amount = payment_data.get("amount")
        
        user = db.query(User).filter(User.razorpay_subscription_id == subscription_id).first()
        
        if user:
            # Update expiry date
            current_end = subscription_data.get("current_end")
            if current_end:
                user.subscription_expires_at = datetime.fromtimestamp(current_end)
            
            # Calculate Razorpay processing fee (2% of amount)
            processing_fee = int(amount * 0.02)  # 2% fee in paise
            
            # Record payment
            payment = Payment(
                user_id=user.id,
                razorpay_order_id=subscription_id,  # Razorpay subscription_id
                razorpay_payment_id=payment_id,  # Razorpay payment_id
                amount=amount,  # in paise
                currency="inr",
                status="succeeded",
                product_type=user.subscription_tier,
                credits_added=0,
                processing_fee=processing_fee,
                completed_at=datetime.utcnow()
            )
            db.add(payment)
            db.commit()
    
    # Handle subscription.cancelled or subscription.paused
    elif event_type in ["subscription.cancelled", "subscription.paused"]:
        subscription_data = event.get("payload", {}).get("subscription", {}).get("entity", {})
        subscription_id = subscription_data.get("id")
        customer_id = subscription_data.get("customer_id")
        
        # Find user by subscription ID or customer ID
        user = None
        if subscription_id:
            user = db.query(User).filter(User.razorpay_subscription_id == subscription_id).first()
        if not user and customer_id:
            user = db.query(User).filter(User.razorpay_customer_id == customer_id).first()
        
        if user:
            # Don't downgrade immediately - let them use until period ends
            user.subscription_auto_renew = False
            user.subscription_status = "cancelled"
            # Keep subscription_expires_at as is - they paid for the period
            db.commit()
    
    # Handle one-time payment.captured (for backward compatibility)
    elif event_type == "payment.captured":
        payload_data = event.get("payload", {}).get("payment", {}).get("entity", {})
        payment_id = payload_data.get("id")
        order_id = payload_data.get("order_id")
        amount = payload_data.get("amount")  # in paise
        currency = payload_data.get("currency", "INR")
        email = payload_data.get("email")
        notes = payload_data.get("notes", {})
        user_id = notes.get("user_id")
        tier = notes.get("tier")
        
        # Get user by ID from notes or by email
        user = None
        if user_id:
            try:
                user = db.query(User).filter(User.id == int(user_id)).first()
            except (ValueError, TypeError):
                pass
        
        if not user and email:
            user = db.query(User).filter(User.email == email).first()
        
        if user and tier:
            # Determine tier from amount if not in notes
            if not tier:
                tier = AMOUNT_TO_TIER.get(amount)
            
            if tier:
                user.subscription_tier = tier
                user.subscription_status = "active"
                user.subscription_expires_at = calculate_expiry(tier)
                user.subscription_auto_renew = False  # One-time payment
                
                # Record payment
                payment = Payment(
                    user_id=user.id,
                    razorpay_payment_id=payment_id,
                    razorpay_order_id=order_id,
                    amount=amount,
                    currency=currency,
                    status="succeeded",
                    product_type=tier,
                    credits_added=0,
                    processing_fee=int(amount * 0.02),  # 2% fee
                    completed_at=datetime.utcnow()
                )
                db.add(payment)
                db.commit()
    
    return {"status": "success"}

