"""
Admin routes
Statistics and management
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from ..database import get_db
from ..auth import is_admin
from ..models import User, Job, Payment
from ..schemas import AdminStats
from sqlalchemy import func, and_
from fastapi import HTTPException

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats", response_model=AdminStats)
def get_admin_stats(
    admin: User = Depends(is_admin),
    db: Session = Depends(get_db)
):
    """
    Get platform statistics
    """
    total_users = db.query(func.count(User.id)).scalar()
    total_jobs = db.query(func.count(Job.id)).scalar()
    
    total_completed = db.query(func.count(Job.id)).filter(
        Job.status == "completed"
    ).scalar()
    
    total_failed = db.query(func.count(Job.id)).filter(
        Job.status == "failed"
    ).scalar()
    
    # Credits used today
    today = datetime.utcnow().date()
    jobs_today = db.query(func.count(Job.id)).filter(
        func.date(Job.created_at) == today
    ).scalar()
    
    # Revenue today (sum of payments)
    revenue_today = db.query(func.sum(Payment.amount)).filter(
        func.date(Payment.created_at) == today,
        Payment.status == "succeeded"
    ).scalar() or 0
    
    revenue_today_rupees = revenue_today / 100  # Convert paise to rupees
    
    # Cost metrics
    total_cost = db.query(func.sum(Job.cost_usd)).filter(
        Job.cost_usd > 0
    ).scalar() or 0.0
    
    cost_today = db.query(func.sum(Job.cost_usd)).filter(
        func.date(Job.created_at) == today,
        Job.cost_usd > 0
    ).scalar() or 0.0
    
    # Jobs requiring review
    jobs_requiring_review = db.query(func.count(Job.id)).filter(
        Job.status == "review"
    ).scalar()
    
    return AdminStats(
        total_users=total_users,
        total_jobs=total_jobs,
        total_completed=total_completed,
        total_failed=total_failed,
        credits_used_today=jobs_today,
        revenue_today=revenue_today_rupees,
        total_cost=total_cost,
        cost_today=cost_today,
        jobs_requiring_review=jobs_requiring_review
    )


@router.get("/users")
def list_all_users(
    admin: User = Depends(is_admin),
    db: Session = Depends(get_db),
    limit: int = 100,
    offset: int = 0
):
    """
    List all users (admin only)
    """
    users = db.query(User).order_by(
        User.created_at.desc()
    ).limit(limit).offset(offset).all()
    
    return users


@router.get("/jobs")
def list_all_jobs(
    admin: User = Depends(is_admin),
    db: Session = Depends(get_db),
    limit: int = 100,
    offset: int = 0,
    status: str = None
):
    """
    List all jobs (admin only)
    """
    query = db.query(Job)
    
    if status:
        query = query.filter(Job.status == status)
    
    jobs = query.order_by(Job.created_at.desc()).limit(limit).offset(offset).all()
    
    return jobs


@router.get("/jobs/review")
def list_review_jobs(
    admin: User = Depends(is_admin),
    db: Session = Depends(get_db),
    limit: int = 50
):
    """
    List jobs requiring review (admin only)
    """
    jobs = db.query(Job).filter(
        Job.status == "review"
    ).order_by(Job.created_at.asc()).limit(limit).all()
    
    return jobs


@router.get("/costs")
def get_cost_metrics(
    admin: User = Depends(is_admin),
    db: Session = Depends(get_db),
    days: int = 30
):
    """
    Get cost metrics for the last N days (admin only)
    """
    from datetime import datetime, timedelta
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Total cost
    total_cost = db.query(func.sum(Job.cost_usd)).filter(
        Job.cost_usd > 0,
        Job.created_at >= start_date
    ).scalar() or 0.0
    
    # Cost per day
    daily_costs = db.query(
        func.date(Job.created_at).label('date'),
        func.sum(Job.cost_usd).label('cost')
    ).filter(
        Job.cost_usd > 0,
        Job.created_at >= start_date
    ).group_by(func.date(Job.created_at)).all()
    
    # Average cost per job
    avg_cost = db.query(func.avg(Job.cost_usd)).filter(
        Job.cost_usd > 0,
        Job.created_at >= start_date
    ).scalar() or 0.0
    
    # Jobs by cost range
    cost_ranges = {
        "under_0.01": db.query(func.count(Job.id)).filter(
            Job.cost_usd > 0,
            Job.cost_usd < 0.01,
            Job.created_at >= start_date
        ).scalar(),
        "0.01_to_0.05": db.query(func.count(Job.id)).filter(
            Job.cost_usd >= 0.01,
            Job.cost_usd < 0.05,
            Job.created_at >= start_date
        ).scalar(),
        "0.05_to_0.10": db.query(func.count(Job.id)).filter(
            Job.cost_usd >= 0.05,
            Job.cost_usd < 0.10,
            Job.created_at >= start_date
        ).scalar(),
        "over_0.10": db.query(func.count(Job.id)).filter(
            Job.cost_usd >= 0.10,
            Job.created_at >= start_date
        ).scalar(),
    }
    
    return {
        "total_cost": float(total_cost),
        "average_cost_per_job": float(avg_cost),
        "daily_costs": [
            {"date": str(row.date), "cost": float(row.cost)}
            for row in daily_costs
        ],
        "cost_ranges": cost_ranges,
        "period_days": days
    }




@router.post("/users/{user_id}/toggle-active")
def toggle_user_active(
    user_id: int,
    admin: User = Depends(is_admin),
    db: Session = Depends(get_db)
):
    """
    Toggle user active status (admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        return {"error": "User not found"}
    
    user.is_active = not user.is_active
    db.commit()
    
    return {
        "message": f"User {user_id} is now {'active' if user.is_active else 'inactive'}"
    }


@router.post("/data-export/{user_id}")
def export_user_data(
    user_id: int,
    admin: User = Depends(is_admin),
    db: Session = Depends(get_db)
):
    """
    Export all user data for GDPR compliance (admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Collect all user data
    jobs = db.query(Job).filter(Job.user_id == user_id).all()
    payments = db.query(Payment).filter(Payment.user_id == user_id).all()
    
    export_data = {
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "created_at": user.created_at.isoformat(),
            "last_login": user.last_login.isoformat() if user.last_login else None,
            "subscription_tier": user.subscription_tier,
            "credits": user.credits
        },
        "jobs": [
            {
                "id": job.id,
                "status": job.status,
                "created_at": job.created_at.isoformat(),
                "sketch_filename": job.sketch_filename,
                "detection_confidence": job.detection_confidence
            }
            for job in jobs
        ],
        "payments": [
            {
                "id": payment.id,
                "amount": payment.amount,
                "currency": payment.currency,
                "status": payment.status,
                "created_at": payment.created_at.isoformat()
            }
            for payment in payments
        ],
        "exported_at": datetime.utcnow().isoformat()
    }
    
    return export_data


@router.delete("/data-delete/{user_id}")
def delete_user_data(
    user_id: int,
    admin: User = Depends(is_admin),
    db: Session = Depends(get_db)
):
    """
    Delete all user data (GDPR right to be forgotten) (admin only)
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Delete user's jobs (files will be cleaned up by cleanup task)
    db.query(Job).filter(Job.user_id == user_id).delete()
    
    # Anonymize user (don't fully delete for audit trail)
    user.email = f"deleted_{user_id}@deleted.local"
    user.name = "Deleted User"
    user.google_id = None
    user.is_active = False
    user.credits = 0
    
    db.commit()
    
    return {"message": f"User {user_id} data deleted successfully"}

