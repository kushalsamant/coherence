"""
Platform-wide Business Feasibility Analysis API Routes
Aggregates data from ASK, Sketch2BIM, and Reframe for comprehensive analysis
"""

import logging
import os
import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Optional, List
from datetime import datetime, timedelta

from ..database import get_db
from ..auth import get_current_user, require_admin
from shared_backend.feasibility import (
    calculate_unit_economics,
    calculate_break_even,
    calculate_profitability_projections,
    calculate_margins,
    analyze_scenarios,
    aggregate_platform_costs,
    allocate_shared_infrastructure_costs,
    get_project_costs,
    calculate_cost_per_user,
    calculate_revenue_per_user,
    calculate_platform_margins,
    get_cross_project_metrics,
)
from shared_backend.feasibility.report_generator import (
    generate_feasibility_report_json,
    format_report_summary,
)

router = APIRouter()
log = logging.getLogger(__name__)


def _get_ask_costs(db: Session, days: int) -> Dict:
    """Get ASK project costs"""
    try:
        from ..services.cost_service import get_total_costs, get_payment_fees
        from ..services.groq_service import get_groq_usage_stats
        
        costs = get_total_costs(db, days=days)
        groq_stats = get_groq_usage_stats(db, days=days)
        
        return {
            "groq_costs_usd": groq_stats.get("total_cost_usd", 0.0),
            "razorpay_fees_usd": costs.get("payment_fees", {}).get("total_fees_usd", 0.0),
            "infrastructure_costs_usd": 0.0,  # To be calculated
            "other_variable_costs_usd": 0.0,
        }
    except Exception as e:
        log.error(f"Failed to get ASK costs: {e}")
        return {
            "groq_costs_usd": 0.0,
            "razorpay_fees_usd": 0.0,
            "infrastructure_costs_usd": 0.0,
            "other_variable_costs_usd": 0.0,
        }


def _get_ask_revenue(db: Session, days: int) -> float:
    """Get ASK project revenue in paise"""
    try:
        from ..models_db import Payment
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        payments = db.query(Payment).filter(
            Payment.status == "succeeded",
            Payment.created_at >= cutoff_date
        ).all()
        
        total_revenue = sum(p.amount or 0 for p in payments)
        return total_revenue
    except Exception as e:
        log.error(f"Failed to get ASK revenue: {e}")
        return 0.0


def _get_ask_users(db: Session) -> List[str]:
    """Get ASK active user emails/IDs"""
    try:
        from ..models_db import User
        
        users = db.query(User).filter(
            User.is_active == True,
            User.subscription_status == "active"
        ).all()
        
        return [user.email for user in users if user.email]
    except Exception as e:
        log.error(f"Failed to get ASK users: {e}")
        return []


def _get_project_data(project_name: str, days: int) -> Dict:
    """
    Get project data (costs, revenue, users) from other projects.
    Makes HTTP calls to Sketch2BIM and Reframe backend APIs.
    """
    try:
        # Get backend URLs from environment
        # Use unified platform API URL with path prefixes
        platform_api_url = os.getenv("PLATFORM_API_URL", os.getenv("NEXT_PUBLIC_PLATFORM_API_URL", "http://localhost:8000"))
        
        if project_name == "sketch2bim":
            backend_url = f"{platform_api_url}/api/sketch2bim"
        elif project_name == "reframe":
            backend_url = f"{platform_api_url}/api/reframe"
        else:
            log.warning(f"Unknown project: {project_name}")
            return {
                "groq_costs_usd": 0.0,
                "razorpay_fees_usd": 0.0,
                "infrastructure_costs_usd": 0.0,
                "other_variable_costs_usd": 0.0,
                "revenue_paise": 0.0,
                "users": [],
            }
        
        # Make API calls with timeout
        timeout = httpx.Timeout(10.0, connect=5.0)
        
        with httpx.Client(timeout=timeout) as client:
            # Get cost metrics (if available)
            costs_data = {}
            try:
                if project_name == "sketch2bim":
                    # Sketch2BIM has /api/v1/admin/costs endpoint
                    response = client.get(
                        f"{backend_url}/api/v1/admin/costs",
                        params={"days": days},
                        headers={"Accept": "application/json"}
                    )
                    if response.status_code == 200:
                        costs_data = response.json()
                elif project_name == "reframe":
                    # Reframe may not have cost endpoint yet - return empty for now
                    costs_data = {}
            except Exception as e:
                log.warning(f"Failed to fetch costs from {project_name}: {e}")
                costs_data = {}
            
            # Extract cost data
            groq_costs = costs_data.get("total_cost", 0.0) if costs_data else 0.0
            razorpay_fees = 0.0  # Would need separate endpoint for payment fees
            infrastructure_costs = 0.0  # Would need separate calculation
            other_variable_costs = 0.0
            
            # Get revenue and user data (would need separate endpoints)
            # For now, return what we can get from costs endpoint
            revenue_paise = 0.0
            users = []
            
            return {
                "groq_costs_usd": float(groq_costs),
                "razorpay_fees_usd": float(razorpay_fees),
                "infrastructure_costs_usd": float(infrastructure_costs),
                "other_variable_costs_usd": float(other_variable_costs),
                "revenue_paise": float(revenue_paise),
                "users": users,
            }
            
    except Exception as e:
        log.error(f"Error fetching data from {project_name}: {e}")
        # Return empty data on error
        return {
            "groq_costs_usd": 0.0,
            "razorpay_fees_usd": 0.0,
            "infrastructure_costs_usd": 0.0,
            "other_variable_costs_usd": 0.0,
            "revenue_paise": 0.0,
            "users": [],
        }


@router.get("/platform/unit-economics")
async def get_platform_unit_economics(
    project: Optional[str] = Query(None, description="Filter by project (ask, sketch2bim, reframe)"),
    days: int = Query(30, description="Number of days to analyze"),
    db: Session = Depends(get_db),
    user = Depends(require_admin())
) -> Dict:
    """
    Get unit economics for platform or specific project.
    
    Returns:
        Dictionary with unit economics breakdown
    """
    try:
        # Get ASK data
        ask_costs = _get_ask_costs(db, days)
        ask_revenue = _get_ask_revenue(db, days)
        ask_users = _get_ask_users(db)
        
        # Get other project data (placeholder for now)
        sketch2bim_data = _get_project_data("sketch2bim", days)
        reframe_data = _get_project_data("reframe", days)
        
        # Aggregate project costs
        project_costs = {
            "ask": ask_costs,
            "sketch2bim": {
                "groq_costs_usd": sketch2bim_data["groq_costs_usd"],
                "razorpay_fees_usd": sketch2bim_data["razorpay_fees_usd"],
                "infrastructure_costs_usd": sketch2bim_data["infrastructure_costs_usd"],
                "other_variable_costs_usd": sketch2bim_data["other_variable_costs_usd"],
            },
            "reframe": {
                "groq_costs_usd": reframe_data["groq_costs_usd"],
                "razorpay_fees_usd": reframe_data["razorpay_fees_usd"],
                "infrastructure_costs_usd": reframe_data["infrastructure_costs_usd"],
                "other_variable_costs_usd": reframe_data["other_variable_costs_usd"],
            },
        }
        
        # Allocate shared infrastructure costs
        project_revenues = {
            "ask": ask_revenue,
            "sketch2bim": sketch2bim_data["revenue_paise"],
            "reframe": reframe_data["revenue_paise"],
        }
        project_user_counts = {
            "ask": len(ask_users),
            "sketch2bim": len(sketch2bim_data["users"]),
            "reframe": len(reframe_data["users"]),
        }
        
        shared_costs = allocate_shared_infrastructure_costs(
            allocation_method="revenue",
            project_revenues=project_revenues,
            project_users=project_user_counts
        )
        
        # Calculate unit economics per project
        unit_economics = {}
        
        for proj_name in ["ask", "sketch2bim", "reframe"]:
            if project and project != proj_name:
                continue
            
            costs = project_costs[proj_name]
            total_costs = (
                costs["groq_costs_usd"] +
                costs["razorpay_fees_usd"] +
                costs["infrastructure_costs_usd"] +
                costs["other_variable_costs_usd"]
            )
            
            users = project_user_counts[proj_name]
            revenue = project_revenues[proj_name]
            
            if users > 0:
                cost_per_user = total_costs / users
                # Calculate average revenue per user (assuming equal distribution)
                # In reality, would need tier breakdown
                from shared_backend.feasibility.feasibility_service import PRICING_TIERS, calculate_revenue_per_user_after_fees
                avg_revenue_per_user = calculate_revenue_per_user_after_fees("monthly")  # Default to monthly tier
                
                unit_econ = calculate_unit_economics(
                    project_name=proj_name,
                    cost_per_user=cost_per_user,
                    revenue_per_user=avg_revenue_per_user,
                    shared_infrastructure_cost_per_user=shared_costs.get(proj_name, 0.0) / users if users > 0 else 0.0
                )
                unit_economics[proj_name] = unit_econ
        
        return {
            "period_days": days,
            "unit_economics": unit_economics,
            "shared_infrastructure_allocation": shared_costs,
        }
        
    except Exception as e:
        log.error(f"Failed to get unit economics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve unit economics: {str(e)}")


@router.get("/platform/break-even")
async def get_platform_break_even(
    project: Optional[str] = Query(None, description="Filter by project"),
    days: int = Query(30, description="Number of days to analyze"),
    db: Session = Depends(get_db),
    user = Depends(require_admin())
) -> Dict:
    """
    Get break-even analysis for platform or specific project.
    """
    try:
        # Get project data
        ask_costs = _get_ask_costs(db, days)
        ask_revenue = _get_ask_revenue(db, days)
        
        # Calculate break-even for ASK (example)
        from shared_backend.feasibility.feasibility_service import calculate_revenue_per_user_after_fees
        
        # Calculate fixed costs from shared infrastructure
        shared_costs = allocate_shared_infrastructure_costs(allocation_method="equal")
        fixed_costs = shared_costs.get("ask", 0.0) + 10.0  # Base infrastructure + app-specific
        
        # Variable cost per user (average)
        ask_users = _get_ask_users(db)
        total_variable_costs = (
            ask_costs["groq_costs_usd"] +
            ask_costs["razorpay_fees_usd"] +
            ask_costs["other_variable_costs_usd"]
        )
        variable_cost_per_user = total_variable_costs / len(ask_users) if ask_users else 0.0
        
        # Revenue per user (month tier as default)
        revenue_per_user = calculate_revenue_per_user_after_fees("monthly")
        
        # Shared infrastructure costs
        shared_costs = allocate_shared_infrastructure_costs(
            allocation_method="equal"
        )
        shared_cost_ask = shared_costs.get("ask", 0.0)
        
        break_even = calculate_break_even(
            fixed_costs=fixed_costs,
            variable_cost_per_user=variable_cost_per_user,
            revenue_per_user=revenue_per_user,
            shared_infrastructure_costs=shared_cost_ask
        )
        
        return {
            "project": project or "platform",
            "period_days": days,
            "break_even_analysis": break_even,
        }
        
    except Exception as e:
        log.error(f"Failed to get break-even analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve break-even analysis: {str(e)}")


@router.get("/platform/projections")
async def get_platform_projections(
    project: Optional[str] = Query(None, description="Filter by project"),
    months: int = Query(12, description="Number of months to project"),
    db: Session = Depends(get_db),
    user = Depends(require_admin())
) -> Dict:
    """
    Get profitability projections for platform or specific project.
    """
    try:
        ask_users = _get_ask_users(db)
        current_users = len(ask_users)
        
        from shared_backend.feasibility.feasibility_service import (
            calculate_revenue_per_user_after_fees,
            calculate_profitability_projections
        )
        
        revenue_per_user = calculate_revenue_per_user_after_fees("monthly")
        
        # Estimate cost per user
        ask_costs = _get_ask_costs(db, days=30)
        total_costs = (
            ask_costs["groq_costs_usd"] +
            ask_costs["razorpay_fees_usd"] +
            ask_costs["infrastructure_costs_usd"]
        )
        cost_per_user = total_costs / current_users if current_users > 0 else 0.0
        
        # Calculate fixed costs from shared infrastructure
        shared_costs = allocate_shared_infrastructure_costs(allocation_method="equal")
        fixed_costs = shared_costs.get("ask", 0.0) + 10.0  # Base infrastructure + app-specific
        
        # Growth scenarios: 5%, 10%, 15% monthly growth
        growth_rates = [0.05, 0.10, 0.15]
        
        projections = calculate_profitability_projections(
            current_users=current_users,
            revenue_per_user=revenue_per_user,
            cost_per_user=cost_per_user,
            fixed_costs=fixed_costs,
            growth_rates=growth_rates,
            months=months
        )
        
        return {
            "project": project or "ask",
            "projections": projections,
        }
        
    except Exception as e:
        log.error(f"Failed to get projections: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve projections: {str(e)}")


@router.get("/platform/scenarios")
async def get_platform_scenarios(
    project: Optional[str] = Query(None, description="Filter by project"),
    db: Session = Depends(get_db),
    user = Depends(require_admin())
) -> Dict:
    """
    Get scenario analysis (pessimistic, realistic, optimistic).
    """
    try:
        ask_users = _get_ask_users(db)
        base_users = len(ask_users)
        
        from shared_backend.feasibility.feasibility_service import (
            calculate_revenue_per_user_after_fees,
            analyze_scenarios
        )
        
        revenue_per_user = calculate_revenue_per_user_after_fees("monthly")
        
        # Estimate costs
        ask_costs = _get_ask_costs(db, days=30)
        total_costs = (
            ask_costs["groq_costs_usd"] +
            ask_costs["razorpay_fees_usd"] +
            ask_costs["infrastructure_costs_usd"]
        )
        cost_per_user = total_costs / base_users if base_users > 0 else 0.0
        
        # Calculate fixed costs from shared infrastructure
        shared_costs = allocate_shared_infrastructure_costs(allocation_method="equal")
        fixed_costs = shared_costs.get("ask", 0.0) + 10.0  # Base infrastructure + app-specific
        
        shared_costs = allocate_shared_infrastructure_costs(allocation_method="equal")
        shared_cost_ask = shared_costs.get("ask", 0.0)
        
        scenarios = analyze_scenarios(
            base_users=base_users,
            revenue_per_user=revenue_per_user,
            cost_per_user=cost_per_user,
            fixed_costs=fixed_costs,
            shared_infrastructure_costs=shared_cost_ask
        )
        
        return {
            "project": project or "ask",
            "scenarios": scenarios,
        }
        
    except Exception as e:
        log.error(f"Failed to get scenarios: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve scenarios: {str(e)}")


@router.get("/platform/margins")
async def get_platform_margins(
    project: Optional[str] = Query(None, description="Filter by project"),
    days: int = Query(30, description="Number of days to analyze"),
    db: Session = Depends(get_db),
    user = Depends(require_admin())
) -> Dict:
    """
    Get margin analysis for platform or specific project.
    """
    try:
        ask_revenue = _get_ask_revenue(db, days)
        ask_costs = _get_ask_costs(db, days)
        
        variable_costs = (
            ask_costs["groq_costs_usd"] +
            ask_costs["razorpay_fees_usd"] +
            ask_costs["other_variable_costs_usd"]
        )
        
        fixed_costs = ask_costs["infrastructure_costs_usd"]
        
        shared_costs = allocate_shared_infrastructure_costs(allocation_method="equal")
        shared_cost_ask = shared_costs.get("ask", 0.0)
        
        margins = calculate_margins(
            total_revenue=ask_revenue,
            variable_costs=variable_costs,
            fixed_costs=fixed_costs,
            shared_infrastructure_costs=shared_cost_ask
        )
        
        return {
            "project": project or "ask",
            "period_days": days,
            "margins": margins,
        }
        
    except Exception as e:
        log.error(f"Failed to get margins: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve margins: {str(e)}")


@router.get("/platform/shared-costs")
async def get_shared_costs(
    allocation_method: str = Query("equal", description="Allocation method: equal, revenue, users"),
    db: Session = Depends(get_db),
    user = Depends(require_admin())
) -> Dict:
    """
    Get shared infrastructure cost breakdown and allocation.
    """
    try:
        # Get project revenues and user counts for allocation
        ask_revenue = _get_ask_revenue(db, days=30)
        ask_users = _get_ask_users(db)
        
        project_revenues = {
            "ask": ask_revenue,
            "sketch2bim": _get_project_data("sketch2bim", days=30).get("revenue_paise", 0.0),
            "reframe": _get_project_data("reframe", days=30).get("revenue_paise", 0.0),
        }
        
        project_users = {
            "ask": len(ask_users),
            "sketch2bim": len(_get_project_data("sketch2bim", days=30).get("users", [])),
            "reframe": len(_get_project_data("reframe", days=30).get("users", [])),
        }
        
        allocations = allocate_shared_infrastructure_costs(
            allocation_method=allocation_method,
            project_revenues=project_revenues if allocation_method == "revenue" else None,
            project_users=project_users if allocation_method == "users" else None
        )
        
        from shared_backend.feasibility.cost_aggregator import SHARED_INFRASTRUCTURE_COSTS, TOTAL_SHARED_COST
        
        return {
            "allocation_method": allocation_method,
            "total_shared_costs_usd": TOTAL_SHARED_COST,
            "cost_breakdown": SHARED_INFRASTRUCTURE_COSTS,
            "allocations": allocations,
        }
        
    except Exception as e:
        log.error(f"Failed to get shared costs: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve shared costs: {str(e)}")


@router.get("/platform/consolidated")
async def get_platform_consolidated(
    days: int = Query(30, description="Number of days to analyze"),
    db: Session = Depends(get_db),
    user = Depends(require_admin())
) -> Dict:
    """
    Get consolidated platform view with all key metrics.
    """
    try:
        # Get all project data
        ask_costs = _get_ask_costs(db, days)
        ask_revenue = _get_ask_revenue(db, days)
        ask_users = _get_ask_users(db)
        
        sketch2bim_data = _get_project_data("sketch2bim", days)
        reframe_data = _get_project_data("reframe", days)
        
        # Aggregate costs
        project_costs = {
            "ask": ask_costs,
            "sketch2bim": {
                "groq_costs_usd": sketch2bim_data["groq_costs_usd"],
                "razorpay_fees_usd": sketch2bim_data["razorpay_fees_usd"],
                "infrastructure_costs_usd": sketch2bim_data["infrastructure_costs_usd"],
                "other_variable_costs_usd": sketch2bim_data["other_variable_costs_usd"],
            },
            "reframe": {
                "groq_costs_usd": reframe_data["groq_costs_usd"],
                "razorpay_fees_usd": reframe_data["razorpay_fees_usd"],
                "infrastructure_costs_usd": reframe_data["infrastructure_costs_usd"],
                "other_variable_costs_usd": reframe_data["other_variable_costs_usd"],
            },
        }
        
        aggregated = aggregate_platform_costs(project_costs, days=days)
        
        # Calculate platform revenue
        platform_revenue = ask_revenue + sketch2bim_data["revenue_paise"] + reframe_data["revenue_paise"]
        
        # Calculate platform margins
        platform_variable_costs = aggregated["total_platform_costs_usd"]
        shared_costs = allocate_shared_infrastructure_costs(allocation_method="equal")
        total_shared = sum(shared_costs.values())
        
        margins = calculate_platform_margins(
            platform_revenue=platform_revenue,
            platform_costs=platform_variable_costs,
            shared_infrastructure_costs=total_shared
        )
        
        # Cross-project metrics
        project_users_dict = {
            "ask": ask_users,
            "sketch2bim": sketch2bim_data["users"],
            "reframe": reframe_data["users"],
        }
        project_revenues_dict = {
            "ask": ask_revenue,
            "sketch2bim": sketch2bim_data["revenue_paise"],
            "reframe": reframe_data["revenue_paise"],
        }
        
        cross_project = get_cross_project_metrics(
            project_users=project_users_dict,
            project_revenues=project_revenues_dict
        )
        
        return {
            "period_days": days,
            "platform_costs": aggregated,
            "platform_revenue_paise": platform_revenue,
            "platform_margins": margins,
            "cross_project_metrics": cross_project,
            "timestamp": datetime.utcnow().isoformat(),
        }
        
    except Exception as e:
        log.error(f"Failed to get consolidated view: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve consolidated view: {str(e)}")


@router.get("/platform/cross-project")
async def get_cross_project_metrics(
    days: int = Query(30, description="Number of days to analyze"),
    db: Session = Depends(get_db),
    user = Depends(require_admin())
) -> Dict:
    """
    Get cross-project metrics (users with multiple subscriptions, etc.).
    """
    try:
        ask_users = _get_ask_users(db)
        sketch2bim_data = _get_project_data("sketch2bim", days)
        reframe_data = _get_project_data("reframe", days)
        
        project_users = {
            "ask": ask_users,
            "sketch2bim": sketch2bim_data["users"],
            "reframe": reframe_data["users"],
        }
        
        project_revenues = {
            "ask": _get_ask_revenue(db, days),
            "sketch2bim": sketch2bim_data["revenue_paise"],
            "reframe": reframe_data["revenue_paise"],
        }
        
        metrics = get_cross_project_metrics(
            project_users=project_users,
            project_revenues=project_revenues
        )
        
        return {
            "period_days": days,
            "cross_project_metrics": metrics,
        }
        
    except Exception as e:
        log.error(f"Failed to get cross-project metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve cross-project metrics: {str(e)}")


@router.get("/platform/report")
async def generate_feasibility_report(
    project: Optional[str] = Query(None, description="Filter by project"),
    format: str = Query("json", description="Report format: json or text"),
    days: int = Query(30, description="Number of days to analyze"),
    db: Session = Depends(get_db),
    user = Depends(require_admin())
):
    """
    Generate comprehensive feasibility report.
    
    Returns:
        JSON report or formatted text summary
    """
    try:
        from fastapi.responses import JSONResponse, PlainTextResponse
        
        # Fetch all required data
        consolidated = await get_platform_consolidated(days=days, db=db, user=user)
        unit_econ = await get_platform_unit_economics(project=project, days=days, db=db, user=user)
        break_even = await get_platform_break_even(project=project, days=days, db=db, user=user)
        projections = await get_platform_projections(project=project, months=12, db=db, user=user)
        scenarios = await get_platform_scenarios(project=project, db=db, user=user)
        margins = await get_platform_margins(project=project, days=days, db=db, user=user)
        shared_costs = await get_shared_costs(allocation_method="revenue", db=db, user=user)
        cross_project = await get_cross_project_metrics(days=days, db=db, user=user)
        
        # Generate report
        report = generate_feasibility_report_json(
            consolidated_data=consolidated,
            unit_economics=unit_econ,
            break_even=break_even,
            projections=projections,
            scenarios=scenarios,
            margins=margins,
            shared_costs=shared_costs,
            cross_project=cross_project
        )
        
        if format == "text":
            summary = format_report_summary(report)
            return PlainTextResponse(content=summary, media_type="text/plain")
        else:
            return JSONResponse(content=report)
        
    except Exception as e:
        log.error(f"Failed to generate report: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")

