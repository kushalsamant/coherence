"""
Feasibility Report Generator
Generates comprehensive business feasibility reports in JSON or PDF format
"""

import logging
from typing import Dict, Optional
from datetime import datetime
from io import BytesIO

log = logging.getLogger(__name__)


def generate_feasibility_report_json(
    consolidated_data: Dict,
    unit_economics: Dict,
    break_even: Dict,
    projections: Dict,
    scenarios: Dict,
    margins: Dict,
    shared_costs: Dict,
    cross_project: Dict
) -> Dict:
    """
    Generate comprehensive feasibility report in JSON format.
    
    Args:
        consolidated_data: Platform consolidated view
        unit_economics: Unit economics data
        break_even: Break-even analysis
        projections: Profitability projections
        scenarios: Scenario analysis
        margins: Margin analysis
        shared_costs: Shared infrastructure costs
        cross_project: Cross-project metrics
        
    Returns:
        Dictionary with complete feasibility report
    """
    report = {
        "report_metadata": {
            "generated_at": datetime.utcnow().isoformat(),
            "report_type": "business_feasibility_analysis",
            "platform": "KVSHVL",
            "projects": ["ASK", "Sketch2BIM", "Reframe"],
        },
        "executive_summary": {
            "platform_revenue_usd": consolidated_data.get("platform_margins", {}).get("total_revenue_usd", 0),
            "platform_costs_usd": consolidated_data.get("platform_costs", {}).get("total_platform_costs_usd", 0),
            "net_profit_usd": consolidated_data.get("platform_margins", {}).get("net_profit_usd", 0),
            "net_margin_percent": consolidated_data.get("platform_margins", {}).get("net_margin_percent", 0),
            "is_profitable": consolidated_data.get("platform_margins", {}).get("net_profit_usd", 0) > 0,
            "total_unique_users": cross_project.get("cross_project_metrics", {}).get("total_unique_users", 0),
            "multi_project_users": cross_project.get("cross_project_metrics", {}).get("multi_project_users", 0),
        },
        "unit_economics": {
            "per_project": unit_economics.get("unit_economics", {}),
            "shared_infrastructure_allocation": unit_economics.get("shared_infrastructure_allocation", {}),
        },
        "break_even_analysis": {
            "break_even_users": break_even.get("break_even_analysis", {}).get("break_even_users"),
            "break_even_revenue_usd": break_even.get("break_even_analysis", {}).get("break_even_revenue_usd"),
            "is_feasible": break_even.get("break_even_analysis", {}).get("is_feasible", False),
            "contribution_margin_per_user_usd": break_even.get("break_even_analysis", {}).get("contribution_margin_per_user_usd", 0),
        },
        "profitability_projections": {
            "current_users": projections.get("projections", {}).get("current_users", 0),
            "scenarios": projections.get("projections", {}).get("scenarios", {}),
        },
        "scenario_analysis": {
            "base_users": scenarios.get("scenarios", {}).get("base_users", 0),
            "pessimistic": scenarios.get("scenarios", {}).get("scenarios", {}).get("pessimistic", {}),
            "realistic": scenarios.get("scenarios", {}).get("scenarios", {}).get("realistic", {}),
            "optimistic": scenarios.get("scenarios", {}).get("scenarios", {}).get("optimistic", {}),
        },
        "margin_analysis": {
            "gross_margin_percent": margins.get("margins", {}).get("gross_margin_percent", 0),
            "net_margin_percent": margins.get("margins", {}).get("net_margin_percent", 0),
            "gross_profit_usd": margins.get("margins", {}).get("gross_profit_usd", 0),
            "net_profit_usd": margins.get("margins", {}).get("net_profit_usd", 0),
        },
        "shared_infrastructure": {
            "total_shared_costs_usd": shared_costs.get("total_shared_costs_usd", 0),
            "cost_breakdown": shared_costs.get("cost_breakdown", {}),
            "allocations": shared_costs.get("allocations", {}),
        },
        "cross_project_insights": {
            "total_unique_users": cross_project.get("cross_project_metrics", {}).get("total_unique_users", 0),
            "multi_project_users": cross_project.get("cross_project_metrics", {}).get("multi_project_users", 0),
            "multi_project_user_percent": cross_project.get("cross_project_metrics", {}).get("multi_project_user_percent", 0),
            "avg_projects_per_user": cross_project.get("cross_project_metrics", {}).get("avg_projects_per_user", 0),
        },
        "cost_breakdown": {
            "platform_costs": consolidated_data.get("platform_costs", {}),
            "project_breakdown": consolidated_data.get("platform_costs", {}).get("project_breakdown", {}),
        },
        "recommendations": _generate_recommendations(
            consolidated_data,
            unit_economics,
            break_even,
            scenarios,
            margins
        ),
    }
    
    return report


def _generate_recommendations(
    consolidated_data: Dict,
    unit_economics: Dict,
    break_even: Dict,
    scenarios: Dict,
    margins: Dict
) -> Dict:
    """
    Generate recommendations based on feasibility analysis.
    
    Args:
        consolidated_data: Platform consolidated view
        unit_economics: Unit economics data
        break_even: Break-even analysis
        scenarios: Scenario analysis
        margins: Margin analysis
        
    Returns:
        Dictionary with recommendations
    """
    recommendations = {
        "pricing": [],
        "cost_optimization": [],
        "growth": [],
        "risk_mitigation": [],
    }
    
    # Check profitability
    net_profit = consolidated_data.get("platform_margins", {}).get("net_profit_usd", 0)
    net_margin = consolidated_data.get("platform_margins", {}).get("net_margin_percent", 0)
    
    if net_profit < 0:
        recommendations["pricing"].append(
            "Platform is currently unprofitable. Consider: 1) Increasing prices, 2) Reducing costs, or 3) Increasing user base"
        )
    
    if net_margin < 10:
        recommendations["pricing"].append(
            f"Net margin ({net_margin:.2f}%) is below healthy threshold (10%). Consider optimizing pricing or costs."
        )
    
    # Check unit economics
    unit_econ = unit_economics.get("unit_economics", {})
    for project, metrics in unit_econ.items():
        if metrics.get("contribution_margin_usd", 0) < 0:
            recommendations["cost_optimization"].append(
                f"{project.upper()}: Negative contribution margin. Costs exceed revenue per user. Urgent cost reduction needed."
            )
        elif metrics.get("gross_margin_percent", 0) < 20:
            recommendations["cost_optimization"].append(
                f"{project.upper()}: Low gross margin ({metrics.get('gross_margin_percent', 0):.2f}%). Consider cost optimization."
            )
    
    # Check break-even
    break_even_users = break_even.get("break_even_analysis", {}).get("break_even_users")
    if break_even_users and break_even_users > 1000:
        recommendations["growth"].append(
            f"Break-even requires {break_even_users} users. Focus on aggressive user acquisition."
        )
    
    # Check scenarios
    realistic_scenario = scenarios.get("scenarios", {}).get("scenarios", {}).get("realistic", {})
    if realistic_scenario.get("is_profitable", False):
        recommendations["growth"].append(
            "Realistic scenario shows profitability. Focus on achieving realistic growth targets."
        )
    else:
        recommendations["risk_mitigation"].append(
            "Even realistic scenario is not profitable. Consider pivoting business model or reducing costs significantly."
        )
    
    # Cross-project insights
    cross_project_users = consolidated_data.get("cross_project_metrics", {}).get("multi_project_users", 0)
    if cross_project_users > 0:
        recommendations["growth"].append(
            f"{cross_project_users} users have multiple subscriptions. Leverage cross-project upselling."
        )
    
    return recommendations


def generate_feasibility_report_pdf(
    report_data: Dict
) -> BytesIO:
    """
    Generate feasibility report in PDF format using reportlab.
    
    Args:
        report_data: Report data dictionary
        
    Returns:
        BytesIO object with PDF content
    """
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
    except ImportError:
        log.warning("reportlab not installed. PDF generation requires: pip install reportlab")
        log.warning("Falling back to empty PDF. Use JSON format instead.")
        return BytesIO()
    
    try:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        story.append(Paragraph("Business Feasibility Report", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Report metadata
        metadata = report_data.get("report_metadata", {})
        if metadata:
            story.append(Paragraph(f"<b>Generated:</b> {metadata.get('generated_at', 'N/A')}", styles['Normal']))
            story.append(Paragraph(f"<b>Platform:</b> {metadata.get('platform', 'N/A')}", styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
        
        # Executive Summary
        exec_summary = report_data.get("executive_summary", {})
        if exec_summary:
            story.append(Paragraph("<b>Executive Summary</b>", styles['Heading2']))
            story.append(Spacer(1, 0.1*inch))
            
            summary_data = [
                ["Metric", "Value"],
                ["Platform Revenue (USD)", f"${exec_summary.get('platform_revenue_usd', 0):,.2f}"],
                ["Platform Costs (USD)", f"${exec_summary.get('platform_costs_usd', 0):,.2f}"],
                ["Net Profit (USD)", f"${exec_summary.get('net_profit_usd', 0):,.2f}"],
                ["Net Margin (%)", f"{exec_summary.get('net_margin_percent', 0):.2f}%"],
            ]
            
            summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(summary_table)
            story.append(Spacer(1, 0.3*inch))
        
        # Unit Economics
        unit_economics = report_data.get("unit_economics", {})
        if unit_economics:
            story.append(Paragraph("<b>Unit Economics</b>", styles['Heading2']))
            story.append(Spacer(1, 0.1*inch))
            
            for project, data in unit_economics.items():
                if isinstance(data, dict):
                    story.append(Paragraph(f"<b>{project.upper()}</b>", styles['Heading3']))
                    story.append(Paragraph(f"Cost per User: ${data.get('cost_per_user_usd', 0):,.4f}", styles['Normal']))
                    story.append(Paragraph(f"Revenue per User: ${data.get('revenue_per_user_usd', 0):,.2f}", styles['Normal']))
                    story.append(Spacer(1, 0.1*inch))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
        
    except Exception as e:
        log.error(f"Error generating PDF: {e}")
        log.warning("Falling back to empty PDF. Use JSON format instead.")
        return BytesIO()


def format_report_summary(report: Dict) -> str:
    """
    Format report as human-readable summary text.
    
    Args:
        report: Feasibility report dictionary
        
    Returns:
        Formatted summary string
    """
    summary = report.get("executive_summary", {})
    
    lines = [
        "=" * 80,
        "KVSHVL PLATFORM BUSINESS FEASIBILITY REPORT",
        "=" * 80,
        "",
        f"Generated: {report.get('report_metadata', {}).get('generated_at', 'N/A')}",
        "",
        "EXECUTIVE SUMMARY",
        "-" * 80,
        f"Platform Revenue: ${summary.get('platform_revenue_usd', 0):,.2f}",
        f"Platform Costs: ${summary.get('platform_costs_usd', 0):,.2f}",
        f"Net Profit: ${summary.get('net_profit_usd', 0):,.2f}",
        f"Net Margin: {summary.get('net_margin_percent', 0):.2f}%",
        f"Status: {'PROFITABLE' if summary.get('is_profitable') else 'NOT PROFITABLE'}",
        "",
        f"Total Unique Users: {summary.get('total_unique_users', 0):,}",
        f"Multi-Project Users: {summary.get('multi_project_users', 0):,}",
        "",
    ]
    
    # Add recommendations
    recommendations = report.get("recommendations", {})
    if any(recommendations.values()):
        lines.extend([
            "RECOMMENDATIONS",
            "-" * 80,
        ])
        
        for category, items in recommendations.items():
            if items:
                lines.append(f"\n{category.upper().replace('_', ' ')}:")
                for item in items:
                    lines.append(f"  • {item}")
    
    lines.extend([
        "",
        "=" * 80,
    ])
    
    return "\n".join(lines)

