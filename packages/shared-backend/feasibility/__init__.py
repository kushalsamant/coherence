"""
Platform-wide business feasibility analysis
Provides unit economics, break-even analysis, and profitability projections
"""

from .feasibility_service import (
    calculate_unit_economics,
    calculate_break_even,
    calculate_profitability_projections,
    calculate_margins,
    analyze_scenarios,
)
from .cost_aggregator import (
    aggregate_platform_costs,
    allocate_shared_infrastructure_costs,
    get_project_costs,
    calculate_cost_per_user,
    calculate_revenue_per_user,
    calculate_platform_margins,
    get_cross_project_metrics,
)
from .report_generator import (
    generate_feasibility_report_json,
    format_report_summary,
)

__all__ = [
    "calculate_unit_economics",
    "calculate_break_even",
    "calculate_profitability_projections",
    "calculate_margins",
    "analyze_scenarios",
    "aggregate_platform_costs",
    "allocate_shared_infrastructure_costs",
    "get_project_costs",
    "calculate_cost_per_user",
    "calculate_revenue_per_user",
    "calculate_platform_margins",
    "get_cross_project_metrics",
    "generate_feasibility_report_json",
    "format_report_summary",
]

