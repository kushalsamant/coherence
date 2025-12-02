"""
Platform-wide cost aggregation service
Aggregates costs across ASK, Sketch2BIM, and Reframe projects
"""

import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

log = logging.getLogger(__name__)

# Project names
PROJECTS = ["ask", "sketch2bim", "reframe"]

# Shared infrastructure cost estimates (monthly, in USD)
# These should be updated based on actual infrastructure bills
SHARED_INFRASTRUCTURE_COSTS = {
    "upstash_postgres": 25.0,  # Database hosting (Upstash Postgres - estimated)
    "upstash_redis": 10.0,  # Redis/caching (estimated)
    "shared_backend_maintenance": 5.0,  # Development/maintenance overhead
    "monitoring_logging": 5.0,  # Monitoring and logging services
}

# Total shared infrastructure cost
TOTAL_SHARED_COST = sum(SHARED_INFRASTRUCTURE_COSTS.values())


def allocate_shared_infrastructure_costs(
    allocation_method: str = "equal",
    project_revenues: Optional[Dict[str, float]] = None,
    project_users: Optional[Dict[str, int]] = None
) -> Dict[str, float]:
    """
    Allocate shared infrastructure costs across projects.
    
    Args:
        allocation_method: Method to use ("equal", "revenue", "users")
        project_revenues: Dictionary of project revenues (in paise) for revenue-based allocation
        project_users: Dictionary of project user counts for user-based allocation
        
    Returns:
        Dictionary mapping project names to allocated costs (in USD)
    """
    if allocation_method == "equal":
        # Equal allocation across all projects
        cost_per_project = TOTAL_SHARED_COST / len(PROJECTS)
        return {project: cost_per_project for project in PROJECTS}
    
    elif allocation_method == "revenue" and project_revenues:
        # Allocate based on revenue share
        total_revenue = sum(project_revenues.values())
        if total_revenue == 0:
            # Fallback to equal allocation
            cost_per_project = TOTAL_SHARED_COST / len(PROJECTS)
            return {project: cost_per_project for project in PROJECTS}
        
        allocations = {}
        for project in PROJECTS:
            revenue = project_revenues.get(project, 0)
            revenue_share = revenue / total_revenue
            allocations[project] = TOTAL_SHARED_COST * revenue_share
        
        return allocations
    
    elif allocation_method == "users" and project_users:
        # Allocate based on user count
        total_users = sum(project_users.values())
        if total_users == 0:
            # Fallback to equal allocation
            cost_per_project = TOTAL_SHARED_COST / len(PROJECTS)
            return {project: cost_per_project for project in PROJECTS}
        
        allocations = {}
        for project in PROJECTS:
            users = project_users.get(project, 0)
            user_share = users / total_users if total_users > 0 else 0
            allocations[project] = TOTAL_SHARED_COST * user_share
        
        return allocations
    
    else:
        # Default to equal allocation
        cost_per_project = TOTAL_SHARED_COST / len(PROJECTS)
        return {project: cost_per_project for project in PROJECTS}


def aggregate_platform_costs(
    project_costs: Dict[str, Dict],
    days: int = 30
) -> Dict:
    """
    Aggregate costs across all projects.
    
    Args:
        project_costs: Dictionary mapping project names to cost dictionaries
                      Each cost dict should have: groq_costs, razorpay_fees, infrastructure_costs
        days: Number of days the costs cover
        
    Returns:
        Dictionary with aggregated platform costs
    """
    total_groq_costs = 0.0
    total_razorpay_fees = 0.0
    total_infrastructure_costs = 0.0
    total_variable_costs = 0.0
    
    project_breakdown = {}
    
    for project in PROJECTS:
        costs = project_costs.get(project, {})
        
        groq_cost = costs.get("groq_costs_usd", 0.0)
        razorpay_fee = costs.get("razorpay_fees_usd", 0.0)
        infrastructure_cost = costs.get("infrastructure_costs_usd", 0.0)
        other_variable = costs.get("other_variable_costs_usd", 0.0)
        
        project_total = groq_cost + razorpay_fee + infrastructure_cost + other_variable
        
        project_breakdown[project] = {
            "groq_costs_usd": round(groq_cost, 6),
            "razorpay_fees_usd": round(razorpay_fee, 2),
            "infrastructure_costs_usd": round(infrastructure_cost, 2),
            "other_variable_costs_usd": round(other_variable, 2),
            "total_costs_usd": round(project_total, 2),
        }
        
        total_groq_costs += groq_cost
        total_razorpay_fees += razorpay_fee
        total_infrastructure_costs += infrastructure_cost
        total_variable_costs += other_variable
    
    total_platform_costs = total_groq_costs + total_razorpay_fees + total_infrastructure_costs + total_variable_costs
    
    return {
        "period_days": days,
        "total_groq_costs_usd": round(total_groq_costs, 6),
        "total_razorpay_fees_usd": round(total_razorpay_fees, 2),
        "total_infrastructure_costs_usd": round(total_infrastructure_costs, 2),
        "total_other_variable_costs_usd": round(total_variable_costs, 2),
        "total_platform_costs_usd": round(total_platform_costs, 2),
        "daily_average_costs_usd": round(total_platform_costs / days, 2) if days > 0 else 0.0,
        "project_breakdown": project_breakdown,
    }


def get_project_costs(
    project_name: str,
    project_costs_data: Dict[str, Dict],
    days: int = 30
) -> Dict:
    """
    Get costs for a specific project.
    
    Args:
        project_name: Name of the project (ask, sketch2bim, reframe)
        project_costs_data: Dictionary mapping project names to cost dictionaries
        days: Number of days the costs cover
        
    Returns:
        Dictionary with project-specific costs
    """
    costs = project_costs_data.get(project_name, {})
    
    return {
        "project": project_name,
        "period_days": days,
        "groq_costs_usd": round(costs.get("groq_costs_usd", 0.0), 6),
        "razorpay_fees_usd": round(costs.get("razorpay_fees_usd", 0.0), 2),
        "infrastructure_costs_usd": round(costs.get("infrastructure_costs_usd", 0.0), 2),
        "other_variable_costs_usd": round(costs.get("other_variable_costs_usd", 0.0), 2),
        "total_costs_usd": round(
            costs.get("groq_costs_usd", 0.0) +
            costs.get("razorpay_fees_usd", 0.0) +
            costs.get("infrastructure_costs_usd", 0.0) +
            costs.get("other_variable_costs_usd", 0.0),
            2
        ),
        "daily_average_costs_usd": round(
            (costs.get("groq_costs_usd", 0.0) +
             costs.get("razorpay_fees_usd", 0.0) +
             costs.get("infrastructure_costs_usd", 0.0) +
             costs.get("other_variable_costs_usd", 0.0)) / days,
            2
        ) if days > 0 else 0.0,
    }


def calculate_cost_per_user(
    project_name: str,
    total_costs: float,
    active_users: int,
    days: int = 30
) -> Dict:
    """
    Calculate cost per user for a project.
    
    Args:
        project_name: Name of the project
        total_costs: Total costs for the period (in USD)
        active_users: Number of active users
        days: Number of days in the period
        
    Returns:
        Dictionary with cost per user metrics
    """
    if active_users == 0:
        return {
            "project": project_name,
            "period_days": days,
            "total_costs_usd": round(total_costs, 2),
            "active_users": 0,
            "cost_per_user_usd": 0.0,
            "cost_per_user_per_day_usd": 0.0,
        }
    
    cost_per_user = total_costs / active_users
    cost_per_user_per_day = cost_per_user / days if days > 0 else 0
    
    return {
        "project": project_name,
        "period_days": days,
        "total_costs_usd": round(total_costs, 2),
        "active_users": active_users,
        "cost_per_user_usd": round(cost_per_user, 6),
        "cost_per_user_per_day_usd": round(cost_per_user_per_day, 8),
    }


def calculate_revenue_per_user(
    project_name: str,
    total_revenue: float,
    active_users: int,
    days: int = 30
) -> Dict:
    """
    Calculate revenue per user for a project.
    
    Args:
        project_name: Name of the project
        total_revenue: Total revenue for the period (in paise)
        active_users: Number of active users
        days: Number of days in the period
        
    Returns:
        Dictionary with revenue per user metrics
    """
    if active_users == 0:
        return {
            "project": project_name,
            "period_days": days,
            "total_revenue_paise": total_revenue,
            "active_users": 0,
            "revenue_per_user_paise": 0.0,
            "revenue_per_user_usd": 0.0,
        }
    
    from .feasibility_service import INR_TO_USD
    
    revenue_per_user_paise = total_revenue / active_users
    revenue_per_user_usd = (revenue_per_user_paise / 100.0) * INR_TO_USD
    
    return {
        "project": project_name,
        "period_days": days,
        "total_revenue_paise": total_revenue,
        "active_users": active_users,
        "revenue_per_user_paise": round(revenue_per_user_paise, 2),
        "revenue_per_user_usd": round(revenue_per_user_usd, 2),
    }


def calculate_platform_margins(
    platform_revenue: float,
    platform_costs: float,
    shared_infrastructure_costs: float = 0.0
) -> Dict:
    """
    Calculate platform-wide margins.
    
    Args:
        platform_revenue: Total platform revenue (in paise)
        platform_costs: Total platform variable costs (in USD)
        shared_infrastructure_costs: Shared infrastructure costs (in USD)
        
    Returns:
        Dictionary with platform margin analysis
    """
    from .feasibility_service import INR_TO_USD
    
    platform_revenue_usd = (platform_revenue / 100.0) * INR_TO_USD
    total_costs = platform_costs + shared_infrastructure_costs
    
    gross_profit = platform_revenue_usd - platform_costs
    gross_margin = (gross_profit / platform_revenue_usd * 100) if platform_revenue_usd > 0 else 0
    
    net_profit = platform_revenue_usd - total_costs
    net_margin = (net_profit / platform_revenue_usd * 100) if platform_revenue_usd > 0 else 0
    
    return {
        "platform_revenue_usd": round(platform_revenue_usd, 2),
        "variable_costs_usd": round(platform_costs, 2),
        "shared_infrastructure_costs_usd": round(shared_infrastructure_costs, 2),
        "total_costs_usd": round(total_costs, 2),
        "gross_profit_usd": round(gross_profit, 2),
        "gross_margin_percent": round(gross_margin, 2),
        "net_profit_usd": round(net_profit, 2),
        "net_margin_percent": round(net_margin, 2),
    }


def get_cross_project_metrics(
    project_users: Dict[str, List[str]],
    project_revenues: Dict[str, float]
) -> Dict:
    """
    Get cross-project metrics (users with multiple subscriptions, etc.).
    
    Args:
        project_users: Dictionary mapping project names to lists of user IDs/emails
        project_revenues: Dictionary mapping project names to total revenue (in paise)
        
    Returns:
        Dictionary with cross-project metrics
    """
    # Find users with multiple subscriptions
    user_project_map = {}
    for project, users in project_users.items():
        for user in users:
            if user not in user_project_map:
                user_project_map[user] = []
            user_project_map[user].append(project)
    
    # Count users by subscription count
    single_project_users = sum(1 for projects in user_project_map.values() if len(projects) == 1)
    multi_project_users = sum(1 for projects in user_project_map.values() if len(projects) > 1)
    total_unique_users = len(user_project_map)
    
    # Calculate average projects per user
    avg_projects_per_user = sum(len(projects) for projects in user_project_map.values()) / total_unique_users if total_unique_users > 0 else 0
    
    # Calculate platform revenue per multi-project user
    total_platform_revenue = sum(project_revenues.values())
    platform_revenue_per_multi_user = total_platform_revenue / multi_project_users if multi_project_users > 0 else 0
    
    return {
        "total_unique_users": total_unique_users,
        "single_project_users": single_project_users,
        "multi_project_users": multi_project_users,
        "multi_project_user_percent": round((multi_project_users / total_unique_users * 100) if total_unique_users > 0 else 0, 2),
        "avg_projects_per_user": round(avg_projects_per_user, 2),
        "platform_revenue_per_multi_user_paise": round(platform_revenue_per_multi_user, 2),
        "user_distribution": {
            project: len(users) for project, users in project_users.items()
        },
    }

