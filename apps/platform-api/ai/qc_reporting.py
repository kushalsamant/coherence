"""
Enhanced QC Reporting Module
Provides structured, category-based reporting with pass/fail indicators
Inspired by SortDesk Gates validation reporting
"""
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict, field
from datetime import datetime
import json
import csv
import io

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

from .ifc_qc import QCReport, QCError
from .ids_validator import IDSValidationReport, IDSValidationResult
from loguru import logger


@dataclass
class CategoryResult:
    """Result for a specific validation category"""
    category: str  # geometry, metadata, structure, naming, compliance
    passed: bool
    total_checks: int
    passed_checks: int
    failed_checks: int
    errors: List[QCError] = field(default_factory=list)
    warnings: List[QCError] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    
    @property
    def pass_rate(self) -> float:
        """Calculate pass rate as percentage"""
        if self.total_checks == 0:
            return 0.0
        return (self.passed_checks / self.total_checks) * 100.0


@dataclass
class EnhancedQCReport:
    """Enhanced QC report with structured categories"""
    job_id: str
    validation_timestamp: str
    overall_status: str  # passed, failed, warning
    overall_confidence: float  # 0-100
    pass_rate: float  # 0-100
    
    # Category breakdown
    categories: Dict[str, CategoryResult] = field(default_factory=dict)
    
    # Summary statistics
    total_checks: int = 0
    passed_checks: int = 0
    failed_checks: int = 0
    warning_checks: int = 0
    
    # File information
    file_size: int = 0
    ifc_schema_version: Optional[str] = None
    
    # IDS validation (if performed)
    ids_validation: Optional[IDSValidationReport] = None
    
    @property
    def all_categories_passed(self) -> bool:
        """Check if all categories passed"""
        return all(cat.passed for cat in self.categories.values())


class EnhancedQCReporter:
    """Enhanced QC reporting with structured categories and multiple formats"""
    
    def __init__(self):
        self.category_mapping = {
            'geometry': 'Geometry',
            'topology': 'Topology',
            'units': 'Units & Measurement',
            'standards': 'IFC Standards',
            'metadata': 'Metadata',
            'structure': 'Structure',
            'naming': 'Naming Conventions',
            'file': 'File Integrity',
            'compliance': 'Compliance',
            'material': 'Materials'
        }
    
    def create_enhanced_report(
        self,
        job_id: str,
        qc_report: QCReport,
        ids_report: Optional[IDSValidationReport] = None
    ) -> EnhancedQCReport:
        """
        Create enhanced QC report from basic QC report
        
        Args:
            job_id: Job identifier
            qc_report: Basic QC report
            ids_report: Optional IDS validation report
            
        Returns:
            EnhancedQCReport
        """
        # Categorize errors and warnings
        categories = self._categorize_issues(qc_report.errors, qc_report.warnings, qc_report.info)
        
        # Calculate statistics
        total_checks = len(qc_report.errors) + len(qc_report.warnings) + len(qc_report.info)
        passed_checks = len(qc_report.info)
        failed_checks = len([e for e in qc_report.errors if e.severity == 'critical'])
        warning_checks = len(qc_report.warnings) + len([e for e in qc_report.errors if e.severity == 'warning'])
        
        # Determine overall status
        if failed_checks == 0 and warning_checks == 0:
            overall_status = "passed"
        elif failed_checks == 0:
            overall_status = "warning"
        else:
            overall_status = "failed"
        
        # Calculate pass rate
        pass_rate = (passed_checks / total_checks * 100) if total_checks > 0 else 100.0
        
        # Generate recommendations
        recommendations = self._generate_recommendations(categories, qc_report)
        
        return EnhancedQCReport(
            job_id=job_id,
            validation_timestamp=qc_report.validation_timestamp,
            overall_status=overall_status,
            overall_confidence=qc_report.confidence_score,
            pass_rate=pass_rate,
            categories=categories,
            total_checks=total_checks,
            passed_checks=passed_checks,
            failed_checks=failed_checks,
            warning_checks=warning_checks,
            file_size=qc_report.file_size,
            ifc_schema_version=qc_report.ifc_schema_version,
            ids_validation=ids_report
        )
    
    def _categorize_issues(
        self,
        errors: List[QCError],
        warnings: List[QCError],
        info: List[QCError]
    ) -> Dict[str, CategoryResult]:
        """Categorize errors and warnings by category"""
        categories: Dict[str, CategoryResult] = {}
        
        # Initialize all categories
        for category in self.category_mapping.keys():
            categories[category] = CategoryResult(
                category=category,
                passed=True,
                total_checks=0,
                passed_checks=0,
                failed_checks=0
            )
        
        # Process errors
        for error in errors:
            category = error.category if error.category in categories else 'standards'
            if category not in categories:
                categories[category] = CategoryResult(
                    category=category,
                    passed=True,
                    total_checks=0,
                    passed_checks=0,
                    failed_checks=0
                )
            
            cat_result = categories[category]
            cat_result.total_checks += 1
            if error.severity == 'critical':
                cat_result.failed_checks += 1
                cat_result.passed = False
                cat_result.errors.append(error)
            else:
                cat_result.warning_checks += 1
                cat_result.warnings.append(error)
        
        # Process warnings
        for warning in warnings:
            category = warning.category if warning.category in categories else 'standards'
            cat_result = categories[category]
            cat_result.total_checks += 1
            cat_result.warning_checks += 1
            cat_result.warnings.append(warning)
        
        # Process info (passed checks)
        for info_item in info:
            category = info_item.category if info_item.category in categories else 'standards'
            cat_result = categories[category]
            cat_result.total_checks += 1
            cat_result.passed_checks += 1
        
        # Calculate passed status for each category
        for category in categories.values():
            if category.failed_checks > 0:
                category.passed = False
        
        # Remove empty categories
        return {k: v for k, v in categories.items() if v.total_checks > 0}
    
    def _generate_recommendations(
        self,
        categories: Dict[str, CategoryResult],
        qc_report: QCReport
    ) -> List[str]:
        """Generate actionable recommendations based on issues"""
        recommendations = []
        
        for category, result in categories.items():
            if not result.passed:
                category_name = self.category_mapping.get(category, category.title())
                
                if category == 'geometry':
                    recommendations.append(
                        f"Review {category_name}: {result.failed_checks} geometry issues found. "
                        "Check wall connections, room boundaries, and opening placements."
                    )
                elif category == 'metadata':
                    recommendations.append(
                        f"Enhance {category_name}: {result.failed_checks} metadata issues. "
                        "Add missing property sets and properties to IFC elements."
                    )
                elif category == 'structure':
                    recommendations.append(
                        f"Fix {category_name}: {result.failed_checks} structural issues. "
                        "Review IFC hierarchy and element relationships."
                    )
                elif category == 'naming':
                    recommendations.append(
                        f"Improve {category_name}: {result.failed_checks} naming convention issues. "
                        "Follow standard naming conventions for elements."
                    )
                elif category == 'compliance':
                    recommendations.append(
                        f"Address {category_name}: {result.failed_checks} compliance issues. "
                        "Review IFC schema compliance and standards adherence."
                    )
        
        if qc_report.confidence_score < 50:
            recommendations.append(
                f"Overall confidence is low ({qc_report.confidence_score:.1f}%). "
                "Consider reviewing the source sketch quality or processing parameters."
            )
        
        return recommendations
    
    def write_enhanced_report(
        self,
        enhanced_report: EnhancedQCReport,
        output_dir: str,
        formats: List[str] = ['json', 'txt', 'csv']
    ) -> Dict[str, str]:
        """
        Write enhanced report in multiple formats
        
        Args:
            enhanced_report: Enhanced QC report
            output_dir: Output directory
            formats: List of formats to generate ('json', 'txt', 'csv', 'pdf')
            
        Returns:
            Dictionary mapping format to file path
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        output_files = {}
        
        if 'json' in formats:
            json_path = output_path / f"{enhanced_report.job_id}_qc_report_enhanced.json"
            self._write_json(enhanced_report, json_path)
            output_files['json'] = str(json_path)
        
        if 'txt' in formats:
            txt_path = output_path / f"{enhanced_report.job_id}_qc_report_enhanced.txt"
            self._write_text(enhanced_report, txt_path)
            output_files['txt'] = str(txt_path)
        
        if 'csv' in formats:
            csv_path = output_path / f"{enhanced_report.job_id}_qc_report_enhanced.csv"
            self._write_csv(enhanced_report, csv_path)
            output_files['csv'] = str(csv_path)
        
        if 'pdf' in formats and REPORTLAB_AVAILABLE:
            pdf_path = output_path / f"{enhanced_report.job_id}_qc_report_enhanced.pdf"
            self._write_pdf(enhanced_report, pdf_path)
            output_files['pdf'] = str(pdf_path)
        elif 'pdf' in formats and not REPORTLAB_AVAILABLE:
            logger.warning("reportlab not available. PDF generation skipped.")
        
        return output_files
    
    def _write_json(self, report: EnhancedQCReport, path: Path):
        """Write JSON report"""
        report_dict = asdict(report)
        # Convert dataclass objects to dict
        report_dict['categories'] = {
            k: asdict(v) for k, v in report.categories.items()
        }
        if report.ids_validation:
            report_dict['ids_validation'] = asdict(report.ids_validation)
            report_dict['ids_validation']['results'] = [asdict(r) for r in report.ids_validation.results]
        
        with open(path, 'w') as f:
            json.dump(report_dict, f, indent=2)
    
    def _write_text(self, report: EnhancedQCReport, path: Path):
        """Write text report"""
        with open(path, 'w') as f:
            f.write("=" * 70 + "\n")
            f.write("ENHANCED QUALITY CONTROL REPORT\n")
            f.write("=" * 70 + "\n\n")
            
            f.write(f"Job ID: {report.job_id}\n")
            f.write(f"Validation Time: {report.validation_timestamp}\n")
            f.write(f"IFC Schema: {report.ifc_schema_version or 'Unknown'}\n")
            f.write(f"File Size: {report.file_size:,} bytes\n\n")
            
            f.write("-" * 70 + "\n")
            f.write("OVERALL STATUS\n")
            f.write("-" * 70 + "\n")
            f.write(f"Status: {report.overall_status.upper()}\n")
            f.write(f"Confidence Score: {report.overall_confidence:.1f}/100\n")
            f.write(f"Pass Rate: {report.pass_rate:.1f}%\n")
            f.write(f"Total Checks: {report.total_checks}\n")
            f.write(f"Passed: {report.passed_checks}\n")
            f.write(f"Failed: {report.failed_checks}\n")
            f.write(f"Warnings: {report.warning_checks}\n\n")
            
            f.write("-" * 70 + "\n")
            f.write("CATEGORY BREAKDOWN\n")
            f.write("-" * 70 + "\n")
            
            for category_name, result in report.categories.items():
                display_name = self.category_mapping.get(category_name, category_name.title())
                status = "PASSED" if result.passed else "FAILED"
                f.write(f"\n{display_name}: {status}\n")
                f.write(f"  Pass Rate: {result.pass_rate:.1f}% ({result.passed_checks}/{result.total_checks})\n")
                
                if result.errors:
                    f.write(f"  Errors ({len(result.errors)}):\n")
                    for error in result.errors:
                        f.write(f"    - [{error.severity.upper()}] {error.message}\n")
                        if error.suggestion:
                            f.write(f"      Suggestion: {error.suggestion}\n")
                
                if result.warnings:
                    f.write(f"  Warnings ({len(result.warnings)}):\n")
                    for warning in result.warnings:
                        f.write(f"    - [{warning.severity.upper()}] {warning.message}\n")
                        if warning.suggestion:
                            f.write(f"      Suggestion: {warning.suggestion}\n")
            
            f.write("\n" + "-" * 70 + "\n")
            f.write("RECOMMENDATIONS\n")
            f.write("-" * 70 + "\n")
            
            if report.categories:
                reporter = EnhancedQCReporter()
                recommendations = reporter._generate_recommendations(report.categories, None)
                for rec in recommendations:
                    f.write(f"- {rec}\n")
            else:
                f.write("All checks passed. No recommendations.\n")
            
            # IDS validation section
            if report.ids_validation:
                f.write("\n" + "-" * 70 + "\n")
                f.write("IDS VALIDATION\n")
                f.write("-" * 70 + "\n")
                f.write(f"Specification: {report.ids_validation.specification_name} v{report.ids_validation.specification_version}\n")
                f.write(f"Pass Rate: {report.ids_validation.pass_rate:.1f}%\n")
                f.write(f"Passed: {report.ids_validation.passed_requirements}\n")
                f.write(f"Failed: {report.ids_validation.failed_requirements}\n\n")
                
                failed_results = [r for r in report.ids_validation.results if not r.passed]
                if failed_results:
                    f.write("Failed Requirements:\n")
                    for result in failed_results[:10]:  # Limit to first 10
                        f.write(f"  - {result.requirement_name}: {result.message}\n")
    
    def _write_csv(self, report: EnhancedQCReport, path: Path):
        """Write CSV report"""
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow(['Enhanced QC Report'])
            writer.writerow(['Job ID', report.job_id])
            writer.writerow(['Validation Time', report.validation_timestamp])
            writer.writerow(['Overall Status', report.overall_status.upper()])
            writer.writerow(['Confidence Score', f"{report.overall_confidence:.1f}"])
            writer.writerow(['Pass Rate', f"{report.pass_rate:.1f}%"])
            writer.writerow([])
            
            # Category summary
            writer.writerow(['Category', 'Status', 'Pass Rate', 'Total', 'Passed', 'Failed', 'Warnings'])
            for category_name, result in report.categories.items():
                display_name = self.category_mapping.get(category_name, category_name.title())
                status = "PASSED" if result.passed else "FAILED"
                writer.writerow([
                    display_name,
                    status,
                    f"{result.pass_rate:.1f}%",
                    result.total_checks,
                    result.passed_checks,
                    result.failed_checks,
                    len(result.warnings)
                ])
            
            writer.writerow([])
            
            # Detailed issues
            writer.writerow(['Category', 'Severity', 'Type', 'Message', 'Element ID', 'Suggestion'])
            for category_name, result in report.categories.items():
                display_name = self.category_mapping.get(category_name, category_name.title())
                for error in result.errors:
                    writer.writerow([
                        display_name,
                        error.severity,
                        'Error',
                        error.message,
                        error.element_id or '',
                        error.suggestion or ''
                    ])
                for warning in result.warnings:
                    writer.writerow([
                        display_name,
                        warning.severity,
                        'Warning',
                        warning.message,
                        warning.element_id or '',
                        warning.suggestion or ''
                    ])
    
    def _write_pdf(self, report: EnhancedQCReport, path: Path):
        """Write PDF report (requires reportlab)"""
        if not REPORTLAB_AVAILABLE:
            raise ImportError("reportlab not available. Install with: pip install reportlab")
        
        doc = SimpleDocTemplate(str(path), pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30
        )
        story.append(Paragraph("Enhanced Quality Control Report", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Summary
        summary_data = [
            ['Job ID', report.job_id],
            ['Validation Time', report.validation_timestamp],
            ['Overall Status', report.overall_status.upper()],
            ['Confidence Score', f"{report.overall_confidence:.1f}/100"],
            ['Pass Rate', f"{report.pass_rate:.1f}%"],
            ['Total Checks', str(report.total_checks)],
            ['Passed', str(report.passed_checks)],
            ['Failed', str(report.failed_checks)],
            ['Warnings', str(report.warning_checks)]
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 4*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Category breakdown
        story.append(Paragraph("Category Breakdown", styles['Heading2']))
        story.append(Spacer(1, 0.2*inch))
        
        category_data = [['Category', 'Status', 'Pass Rate', 'Checks']]
        for category_name, result in report.categories.items():
            display_name = self.category_mapping.get(category_name, category_name.title())
            status = "✓ PASSED" if result.passed else "✗ FAILED"
            category_data.append([
                display_name,
                status,
                f"{result.pass_rate:.1f}%",
                f"{result.passed_checks}/{result.total_checks}"
            ])
        
        category_table = Table(category_data, colWidths=[2.5*inch, 1.5*inch, 1*inch, 1*inch])
        category_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4472c4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')])
        ]))
        story.append(category_table)
        
        doc.build(story)


def create_enhanced_qc_report(
    job_id: str,
    qc_report: QCReport,
    ids_report: Optional[IDSValidationReport] = None,
    output_dir: str = "./outputs",
    formats: List[str] = ['json', 'txt', 'csv']
) -> Dict[str, str]:
    """
    Convenience function to create and write enhanced QC report
    
    Args:
        job_id: Job identifier
        qc_report: Basic QC report
        ids_report: Optional IDS validation report
        output_dir: Output directory
        formats: List of formats to generate
        
    Returns:
        Dictionary mapping format to file path
    """
    reporter = EnhancedQCReporter()
    enhanced_report = reporter.create_enhanced_report(job_id, qc_report, ids_report)
    return reporter.write_enhanced_report(enhanced_report, output_dir, formats)

