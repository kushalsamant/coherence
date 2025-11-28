"""
Razorpay payment routes
Webhooks and subscription management
"""
from fastapi import APIRouter, Depends, HTTPException, Header, Request
from sqlalchemy.orm import Session
import razorpay
import json
from datetime import datetime
import os
import logging

from ..database import get_db
from ..models_db import User, Payment
from ..config import settings
from shared_backend.subscription.utils import calculate_expiry, ensure_subscription_status, is_paid_tier
from ..auth import get_current_user

router = APIRouter()
log = logging.getLogger(__name__)

# Configure Razorpay
razorpay_client = None
key_id = settings.razorpay_key_id
key_secret = settings.razorpay_key_secret
if key_id and key_secret:
    razorpay_client = razorpay.Client(auth=(key_id, key_secret))


def verify_razorpay_webhook_signature(payload: str, signature: str) -> bool:
    """
    Verify Razorpay webhook signature
    """
    if not settings.RAZORPAY_WEBHOOK_SECRET or not razorpay_client:
        return False
    
    try:
        razorpay_client.utility.verify_webhook_signature(
            payload,
            signature,
            settings.RAZORPAY_WEBHOOK_SECRET
        )
        return True
    except Exception as e:
        log.error(f"Webhook signature verification failed: {e}")
        return False


@router.post("/webhook")
async def razorpay_webhook(
    request: Request,
    x_razorpay_signature: str = Header(None, alias="x-razorpay-signature"),
    db: Session = Depends(get_db)
):
    """
    Handle Razorpay webhook events
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
    
    # Map Razorpay amounts to tiers
    AMOUNT_TO_TIER = {
        settings.RAZORPAY_WEEK_AMOUNT: "week",
        settings.RAZORPAY_MONTH_AMOUNT: "month",
        settings.RAZORPAY_YEAR_AMOUNT: "year",
    }
    
    # Handle one-time payment captured
    if event_type == "payment.captured":
        payload_data = event.get("payload", {}).get("payment", {}).get("entity", {})
        payment_id = payload_data.get("id")
        order_id = payload_data.get("order_id")
        amount = payload_data.get("amount")  # in paise
        currency = payload_data.get("currency", "INR")
        email = payload_data.get("email")
        notes = payload_data.get("notes", {})
        user_id = notes.get("user_id")
        payment_type = notes.get("payment_type", "one_time")
        
        # Get user by ID from notes or by email
        user = None
        if user_id:
            try:
                user = db.query(User).filter(User.id == int(user_id)).first()
            except (ValueError, TypeError):
                pass
        
        if not user and email:
            user = db.query(User).filter(User.email == email).first()
        
        if not user:
            # Log but don't fail - payment succeeded but user not found
            return {"status": "success", "message": "User not found"}
        
        ensure_subscription_status(user, db)
        
        # Determine tier from amount (paise) - only for one-time payments
        if payment_type == "one_time":
            tier = AMOUNT_TO_TIER.get(amount)
            credits_added = 0
            product_type = tier if tier else "one_time"
            
            if tier:
                user.subscription_tier = tier
                user.subscription_status = "active"
                user.subscription_expires_at = calculate_expiry(tier)
                user.subscription_auto_renew = False  # One-time payment
            else:
                # Unknown amount - log for investigation
                log.warning(f"Unknown payment amount: {amount} for user {user.id}")
            
            # Calculate Razorpay processing fee (2% of amount)
            processing_fee = int(amount * 0.02)  # 2% fee in paise
            
            # Record payment
            payment = Payment(
                user_id=user.id,
                stripe_checkout_session_id=order_id,  # Stores Razorpay order_id
                stripe_payment_intent_id=payment_id,  # Stores Razorpay payment_id
                amount=amount,  # in paise
                currency=currency.lower() or "inr",
                status="succeeded",
                product_type=product_type,
                credits_added=credits_added,
                processing_fee=processing_fee,  # Store processing fee
                completed_at=datetime.utcnow()
            )
            
            db.add(payment)
            db.commit()
    
    # Handle subscription events
    elif event_type == "subscription.created":
        subscription_data = event.get("payload", {}).get("subscription", {}).get("entity", {})
        subscription_id = subscription_data.get("id")
        customer_id = subscription_data.get("customer_id")
        notes = subscription_data.get("notes", {})
        user_id = notes.get("user_id")
        
        # Find user
        user = None
        if user_id:
            try:
                user = db.query(User).filter(User.id == int(user_id)).first()
            except (ValueError, TypeError):
                pass
        
        if not user and customer_id:
            user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
        
        if user:
            user.razorpay_subscription_id = subscription_id
            user.subscription_auto_renew = True
            db.commit()
    
    elif event_type == "subscription.activated":
        subscription_data = event.get("payload", {}).get("subscription", {}).get("entity", {})
        subscription_id = subscription_data.get("id")
        customer_id = subscription_data.get("customer_id")
        plan_data = subscription_data.get("plan", {})
        notes = subscription_data.get("notes", {})
        user_id = notes.get("user_id")
        
        # Determine tier from plan_id
        plan_to_tier = {
            settings.RAZORPAY_PLAN_WEEK: "week",
            settings.RAZORPAY_PLAN_MONTH: "month",
            settings.RAZORPAY_PLAN_YEAR: "year",
        }
        tier = plan_to_tier.get(plan_data.get("id"))
        
        # Find user
        user = None
        if user_id:
            try:
                user = db.query(User).filter(User.id == int(user_id)).first()
            except (ValueError, TypeError):
                pass
        
        if not user and customer_id:
            user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
        
        if user and tier:
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
    
    elif event_type == "subscription.charged":
        # Subscription payment was charged (renewal)
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
                stripe_checkout_session_id=subscription_id,  # Stores Razorpay subscription_id
                stripe_payment_intent_id=payment_id,  # Stores Razorpay payment_id
                amount=amount,  # in paise
                currency="inr",
                status="succeeded",
                product_type=user.subscription_tier,
                credits_added=0,
                processing_fee=processing_fee,  # Store processing fee
                completed_at=datetime.utcnow()
            )
            db.add(payment)
            db.commit()
    
    elif event_type == "subscription.cancelled" or event_type == "subscription.paused":
        subscription_data = event.get("payload", {}).get("subscription", {}).get("entity", {})
        subscription_id = subscription_data.get("id")
        customer_id = subscription_data.get("customer_id")
        
        # Find user by subscription ID or customer ID
        user = None
        if subscription_id:
            user = db.query(User).filter(User.razorpay_subscription_id == subscription_id).first()
        
        if not user and customer_id:
            user = db.query(User).filter(User.stripe_customer_id == customer_id).first()
        
        if user:
            # Don't downgrade immediately - let them use until period ends
            user.subscription_auto_renew = False
            user.subscription_status = "cancelled"
            # Keep subscription_expires_at as is - they paid for the period
            db.commit()
    
    return {"status": "success"}


@router.post("/checkout")
async def create_checkout_session(
    price_id: str,
    payment_type: str = "one_time",  # "one_time" or "subscription"
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create Razorpay order or subscription for checkout
    
    Args:
        price_id: Tier name ('week', 'month', 'year')
        payment_type: 'one_time' for one-time payment, 'subscription' for recurring
        user: Current user
        db: Database session
    """
    if not razorpay_client:
        raise HTTPException(status_code=500, detail="Razorpay not configured")
    
    tier_key = price_id.lower()
    
    # Get base URL from settings or request
    base_url = settings.FRONTEND_URL

    cancel_url = f"{base_url}/pricing?checkout=canceled"
    
    try:
        if payment_type == "subscription":
            # Create subscription using Plan ID
            plan_map = {
                "week": settings.RAZORPAY_PLAN_WEEK,
                "month": settings.RAZORPAY_PLAN_MONTH,
                "year": settings.RAZORPAY_PLAN_YEAR,
            }
            
            plan_id = plan_map.get(tier_key)
            if not plan_id:
                raise HTTPException(
                    status_code=400,
                    detail=f"Plan not configured for tier: {tier_key}. Run scripts/create_razorpay_plans.py first."
                )
            
            # Create customer if doesn't exist
            customer_id = user.stripe_customer_id
            if not customer_id:
                customer = razorpay_client.customer.create({
                    "name": user.name or user.email.split("@")[0],
                    "email": user.email,
                    "contact": None
                })
                customer_id = customer["id"]
                user.stripe_customer_id = customer_id
                db.commit()
            
            # Create subscription
            subscription_data = {
                "plan_id": plan_id,
                "customer_notify": 1,
                "total_count": 0,  # 0 = infinite recurring
                "notes": {
                    "user_id": str(user.id),
                    "user_email": user.email,
                    "tier": tier_key
                }
            }
            
            subscription = razorpay_client.subscription.create(data=subscription_data)
            
            return {
                "subscription_id": subscription["id"],
                "plan_id": plan_id,
                "amount": subscription["plan"]["amount"],
                "currency": subscription["plan"]["currency"],
                "key_id": settings.razorpay_key_id,
                "name": "ASK: Daily Research",
                "description": f"{tier_key.title()} subscription (auto-renews)",
                "prefill": {
                    "email": user.email,
                    "name": user.name or user.email.split("@")[0]
                },
                "theme": {
                    "color": "#6366f1"
                },
                "success_url": f"{base_url}/dashboard?checkout=success",
                "cancel_url": cancel_url,
                "payment_type": "subscription"
            }
        
        else:
            # Create one-time order
            tier_map = {
                "week": settings.RAZORPAY_WEEK_AMOUNT,
                "month": settings.RAZORPAY_MONTH_AMOUNT,
                "year": settings.RAZORPAY_YEAR_AMOUNT,
            }
            
            amount = tier_map.get(tier_key)
            if not amount:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid tier. Expected one of {list(tier_map.keys())}, got: {price_id}"
                )
            
            order_data = {
                "amount": amount,  # in paise
                "currency": "INR",
                "receipt": f"order_{user.id}_{datetime.utcnow().timestamp()}",
                "notes": {
                    "user_id": str(user.id),
                    "user_email": user.email,
                    "tier": tier_key,
                    "payment_type": "one_time"
                }
            }
            
            order = razorpay_client.order.create(data=order_data)
            
            return {
                "order_id": order["id"],
                "amount": order["amount"],
                "currency": order["currency"],
                "key_id": settings.razorpay_key_id,
                "name": "ASK: Daily Research",
                "description": f"{tier_key.title()} access (one-time)",
                "prefill": {
                    "email": user.email,
                    "name": user.name or user.email.split("@")[0]
                },
                "theme": {
                    "color": "#6366f1"
                },
                "success_url": f"{base_url}/dashboard?checkout=success",
                "cancel_url": cancel_url,
                "payment_type": "one_time"
            }
    
    except razorpay.errors.BadRequestError as e:
        raise HTTPException(status_code=400, detail=f"Razorpay error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Payment error: {str(e)}")


@router.get("/subscriptions")
def get_user_subscriptions(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's active subscriptions
    """
    if not user.razorpay_subscription_id:
        return {"subscriptions": []}
    
    try:
        subscription = razorpay_client.subscription.fetch(user.razorpay_subscription_id)
        return {"subscriptions": [subscription]}
    except Exception as e:
        return {"subscriptions": [], "error": str(e)}


@router.post("/subscriptions/{subscription_id}/cancel")
async def cancel_subscription(
    subscription_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cancel a subscription
    """
    if not razorpay_client:
        raise HTTPException(status_code=500, detail="Razorpay not configured")
    
    # Verify subscription belongs to user
    if user.razorpay_subscription_id != subscription_id:
        raise HTTPException(status_code=403, detail="Subscription not found")
    
    try:
        # Cancel subscription at period end
        subscription = razorpay_client.subscription.cancel(subscription_id, {
            "cancel_at_cycle_end": 1  # Cancel at end of billing cycle
        })
        
        user.subscription_auto_renew = False
        user.subscription_status = "cancelled"
        db.commit()
        
        return {"status": "success", "subscription": subscription}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to cancel subscription: {str(e)}")


@router.post("/subscriptions/{subscription_id}/resume")
async def resume_subscription(
    subscription_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Resume a paused subscription
    """
    if not razorpay_client:
        raise HTTPException(status_code=500, detail="Razorpay not configured")
    
    # Verify subscription belongs to user
    if user.razorpay_subscription_id != subscription_id:
        raise HTTPException(status_code=403, detail="Subscription not found")
    
    try:
        subscription = razorpay_client.subscription.resume(subscription_id, {
            "resume_at": "now"
        })
        
        user.subscription_auto_renew = True
        user.subscription_status = "active"
        db.commit()
        
        return {"status": "success", "subscription": subscription}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to resume subscription: {str(e)}")


@router.get("/history")
def get_payment_history(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 50
):
    """
    Get user's payment history
    """
    payments = db.query(Payment).filter(
        Payment.user_id == user.id
    ).order_by(Payment.created_at.desc()).limit(limit).all()
    
    return payments


@router.get("/fees")
def get_payment_fees(
    days: int = 30,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get payment processing fees summary
    
    Args:
        days: Number of days to look back (default: 30)
        user: Current user (must be authenticated)
        db: Database session
        
    Returns:
        Dictionary with fee breakdown
    """
    from ..services.cost_service import get_payment_fees as get_fees
    
    try:
        fees = get_fees(db, days=days)
        return fees
    except Exception as e:
        log.error(f"Failed to get payment fees: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve payment fees")


@router.post("/add-credits")
async def add_credits_manual(
    user_id: int,
    credits: int,
    db: Session = Depends(get_db),
    # Add admin auth here
):
    """
    Manually add credits (admin only)
    DEPRECATED: Credits are no longer used for access control.
    This endpoint is kept for backward compatibility only.
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # DEPRECATED: Credits are no longer used for access control.
    # This endpoint is kept for backward compatibility only.
    # Access is now controlled by subscription status.
    user.credits += credits
    db.commit()
    
    return {"message": f"Added {credits} credits to user {user_id} (deprecated - credits no longer used for access control)"}

