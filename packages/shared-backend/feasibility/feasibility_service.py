"""
Platform-wide business feasibility analysis service
Calculates unit economics, break-even points, and profitability projections
"""

import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from decimal import Decimal

log = logging.getLogger(__name__)

# Pricing structure (in paise, ₹1 = 100 paise)
# Shared across all projects - using "monthly"/"yearly" standard
PRICING_TIERS = {
    "weekly": 129900,  # ₹1,299/weekly
    "monthly": 349900,  # ₹3,499/monthly
    "yearly": 2999900,  # ₹29,999/yearly
}

# Razorpay fee percentage
RAZORPAY_FEE_PERCENTAGE = 0.02  # 2%

# INR to USD conversion (approximate, should be updated regularly)
INR_TO_USD = 0.012  # ₹1 ≈ $0.012


def calculate_revenue_per_user_after_fees(tier: str) -> float:
    """
    Calculate revenue per user after Razorpay fees.
    
    Args:
        tier: Subscription tier (weekly, monthly, yearly)
        
    Returns:
        Revenue in paise (after fees)
    """
    if tier not in PRICING_TIERS:
        return 0.0
    
    price_paise = PRICING_TIERS[tier]
    revenue_after_fees = price_paise * (1 - RAZORPAY_FEE_PERCENTAGE)
    return revenue_after_fees


def calculate_unit_economics(
    project_name: str,
    cost_per_user: float,
    revenue_per_user: float,
    shared_infrastructure_cost_per_user: float = 0.0
) -> Dict:
    """
    Calculate unit economics for a project.
    
    Args:
        project_name: Name of the project (ask, sketch2bim, reframe)
        cost_per_user: Direct cost per user (in USD or paise)
        revenue_per_user: Revenue per user after fees (in paise)
        shared_infrastructure_cost_per_user: Allocated shared infrastructure cost per user
        
    Returns:
        Dictionary with unit economics metrics
    """
    # Convert revenue to USD for comparison
    revenue_usd = (revenue_per_user / 100.0) * INR_TO_USD
    
    # Total cost per user (direct + shared infrastructure)
    total_cost_per_user = cost_per_user + shared_infrastructure_cost_per_user
    
    # Gross margin
    if revenue_usd > 0:
        gross_margin = ((revenue_usd - total_cost_per_user) / revenue_usd) * 100
    else:
        gross_margin = 0.0
    
    # Contribution margin (revenue - variable costs)
    contribution_margin = revenue_usd - total_cost_per_user
    
    return {
        "project": project_name,
        "revenue_per_user_paise": revenue_per_user,
        "revenue_per_user_usd": round(revenue_usd, 2),
        "cost_per_user_usd": round(total_cost_per_user, 6),
        "contribution_margin_usd": round(contribution_margin, 2),
        "gross_margin_percent": round(gross_margin, 2),
        "break_even_users": int(total_cost_per_user / revenue_usd) if revenue_usd > 0 else 0,
    }


def calculate_break_even(
    fixed_costs: float,
    variable_cost_per_user: float,
    revenue_per_user: float,
    shared_infrastructure_costs: float = 0.0
) -> Dict:
    """
    Calculate break-even point.
    
    Args:
        fixed_costs: Fixed costs (infrastructure, etc.) in USD
        variable_cost_per_user: Variable cost per user in USD
        revenue_per_user: Revenue per user after fees (in paise, will be converted)
        shared_infrastructure_costs: Shared infrastructure costs to allocate
        
    Returns:
        Dictionary with break-even analysis
    """
    # Convert revenue to USD
    revenue_per_user_usd = (revenue_per_user / 100.0) * INR_TO_USD
    
    # Total fixed costs (including shared infrastructure)
    total_fixed_costs = fixed_costs + shared_infrastructure_costs
    
    # Contribution margin per user
    contribution_margin = revenue_per_user_usd - variable_cost_per_user
    
    # Break-even users
    if contribution_margin > 0:
        break_even_users = int(total_fixed_costs / contribution_margin)
    else:
        break_even_users = float('inf')  # Never break even
    
    # Break-even revenue
    break_even_revenue = break_even_users * revenue_per_user_usd if break_even_users != float('inf') else 0
    
    return {
        "fixed_costs_usd": round(total_fixed_costs, 2),
        "variable_cost_per_user_usd": round(variable_cost_per_user, 6),
        "revenue_per_user_usd": round(revenue_per_user_usd, 2),
        "contribution_margin_per_user_usd": round(contribution_margin, 2),
        "break_even_users": break_even_users if break_even_users != float('inf') else None,
        "break_even_revenue_usd": round(break_even_revenue, 2) if break_even_revenue > 0 else None,
        "is_feasible": contribution_margin > 0,
    }


def calculate_profitability_projections(
    current_users: int,
    revenue_per_user: float,
    cost_per_user: float,
    fixed_costs: float,
    growth_rates: List[float],
    months: int = 12
) -> Dict:
    """
    Calculate profitability projections for different growth scenarios.
    
    Args:
        current_users: Current number of active users
        revenue_per_user: Revenue per user after fees (in paise)
        cost_per_user: Cost per user in USD
        fixed_costs: Fixed costs per month in USD
        growth_rates: List of monthly growth rates (e.g., [0.05, 0.10, 0.15] for 5%, 10%, 15%)
        months: Number of months to project
        
    Returns:
        Dictionary with profitability projections
    """
    revenue_per_user_usd = (revenue_per_user / 100.0) * INR_TO_USD
    
    projections = {}
    
    for growth_rate in growth_rates:
        scenario_name = f"{int(growth_rate * 100)}%_monthly_growth"
        monthly_data = []
        users = current_users
        cumulative_profit = 0.0
        
        for month in range(1, months + 1):
            # Calculate users for this month (with growth)
            users = int(users * (1 + growth_rate))
            
            # Monthly revenue
            monthly_revenue = users * revenue_per_user_usd
            
            # Monthly costs
            monthly_variable_costs = users * cost_per_user
            monthly_total_costs = monthly_variable_costs + fixed_costs
            
            # Monthly profit
            monthly_profit = monthly_revenue - monthly_total_costs
            cumulative_profit += monthly_profit
            
            # Margin
            margin_percent = (monthly_profit / monthly_revenue * 100) if monthly_revenue > 0 else 0
            
            monthly_data.append({
                "month": month,
                "users": users,
                "revenue_usd": round(monthly_revenue, 2),
                "costs_usd": round(monthly_total_costs, 2),
                "profit_usd": round(monthly_profit, 2),
                "margin_percent": round(margin_percent, 2),
                "cumulative_profit_usd": round(cumulative_profit, 2),
            })
        
        projections[scenario_name] = {
            "growth_rate_percent": int(growth_rate * 100),
            "final_users": users,
            "final_monthly_revenue_usd": round(users * revenue_per_user_usd, 2),
            "final_monthly_profit_usd": round(monthly_profit, 2),
            "cumulative_profit_usd": round(cumulative_profit, 2),
            "monthly_breakdown": monthly_data,
        }
    
    return {
        "current_users": current_users,
        "projection_months": months,
        "scenarios": projections,
    }


def calculate_margins(
    total_revenue: float,
    variable_costs: float,
    fixed_costs: float,
    shared_infrastructure_costs: float = 0.0
) -> Dict:
    """
    Calculate gross and net margins.
    
    Args:
        total_revenue: Total revenue (in paise, will be converted)
        variable_costs: Variable costs in USD
        fixed_costs: Fixed costs in USD
        shared_infrastructure_costs: Shared infrastructure costs in USD
        
    Returns:
        Dictionary with margin analysis
    """
    total_revenue_usd = (total_revenue / 100.0) * INR_TO_USD
    total_costs = variable_costs + fixed_costs + shared_infrastructure_costs
    
    # Gross margin (revenue - variable costs)
    gross_profit = total_revenue_usd - variable_costs
    gross_margin = (gross_profit / total_revenue_usd * 100) if total_revenue_usd > 0 else 0
    
    # Net margin (revenue - all costs)
    net_profit = total_revenue_usd - total_costs
    net_margin = (net_profit / total_revenue_usd * 100) if total_revenue_usd > 0 else 0
    
    return {
        "total_revenue_usd": round(total_revenue_usd, 2),
        "variable_costs_usd": round(variable_costs, 6),
        "fixed_costs_usd": round(fixed_costs, 2),
        "shared_infrastructure_costs_usd": round(shared_infrastructure_costs, 2),
        "total_costs_usd": round(total_costs, 2),
        "gross_profit_usd": round(gross_profit, 2),
        "gross_margin_percent": round(gross_margin, 2),
        "net_profit_usd": round(net_profit, 2),
        "net_margin_percent": round(net_margin, 2),
    }


def analyze_scenarios(
    base_users: int,
    revenue_per_user: float,
    cost_per_user: float,
    fixed_costs: float,
    shared_infrastructure_costs: float = 0.0
) -> Dict:
    """
    Analyze pessimistic, realistic, and optimistic scenarios.
    
    Args:
        base_users: Base number of users
        revenue_per_user: Revenue per user after fees (in paise)
        cost_per_user: Cost per user in USD
        fixed_costs: Fixed costs per month in USD
        shared_infrastructure_costs: Shared infrastructure costs per month in USD
        
    Returns:
        Dictionary with scenario analysis
    """
    revenue_per_user_usd = (revenue_per_user / 100.0) * INR_TO_USD
    total_fixed_costs = fixed_costs + shared_infrastructure_costs
    
    scenarios = {
        "pessimistic": {
            "user_multiplier": 0.5,  # 50% of base
            "description": "Low user growth, high costs"
        },
        "realistic": {
            "user_multiplier": 1.0,  # Base case
            "description": "Moderate growth, expected costs"
        },
        "optimistic": {
            "user_multiplier": 2.0,  # 2x base
            "description": "High growth, optimized costs"
        }
    }
    
    results = {}
    
    for scenario_name, scenario_config in scenarios.items():
        users = int(base_users * scenario_config["user_multiplier"])
        
        # Monthly revenue
        monthly_revenue = users * revenue_per_user_usd
        
        # Monthly costs
        monthly_variable_costs = users * cost_per_user
        monthly_total_costs = monthly_variable_costs + total_fixed_costs
        
        # Monthly profit
        monthly_profit = monthly_revenue - monthly_total_costs
        
        # Margins
        gross_margin = ((monthly_revenue - monthly_variable_costs) / monthly_revenue * 100) if monthly_revenue > 0 else 0
        net_margin = (monthly_profit / monthly_revenue * 100) if monthly_revenue > 0 else 0
        
        # Annual projections
        annual_revenue = monthly_revenue * 12
        annual_costs = monthly_total_costs * 12
        annual_profit = annual_revenue - annual_costs
        
        results[scenario_name] = {
            "description": scenario_config["description"],
            "users": users,
            "monthly_revenue_usd": round(monthly_revenue, 2),
            "monthly_costs_usd": round(monthly_total_costs, 2),
            "monthly_profit_usd": round(monthly_profit, 2),
            "gross_margin_percent": round(gross_margin, 2),
            "net_margin_percent": round(net_margin, 2),
            "annual_revenue_usd": round(annual_revenue, 2),
            "annual_costs_usd": round(annual_costs, 2),
            "annual_profit_usd": round(annual_profit, 2),
            "is_profitable": monthly_profit > 0,
        }
    
    return {
        "base_users": base_users,
        "scenarios": results,
    }

