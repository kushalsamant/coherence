"""
Data Export Module
Exports extracted IFC data to various formats (Excel, CSV, JSON, XML)
"""
from typing import Dict, List, Any, Optional
from pathlib import Path
import json
import csv
from loguru import logger


class DataExporter:
    """Exports extracted IFC data to various formats"""
    
    def __init__(self):
        pass
    
    def export_to_json(
        self,
        data: Dict[str, Any],
        output_path: str
    ) -> str:
        """
        Export data to JSON format
        
        Args:
            data: Data dictionary
            output_path: Path to save JSON file
            
        Returns:
            Path to generated JSON file
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Exported JSON to {output_file}")
        return str(output_file)
    
    def export_to_csv(
        self,
        data: List[Dict[str, Any]],
        output_path: str,
        headers: Optional[List[str]] = None
    ) -> str:
        """
        Export data to CSV format
        
        Args:
            data: List of dictionaries
            output_path: Path to save CSV file
            headers: Optional list of column headers
            
        Returns:
            Path to generated CSV file
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        if not data:
            logger.warning("No data to export to CSV")
            return str(output_file)
        
        # Determine headers
        if not headers:
            headers = list(data[0].keys())
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            
            for row in data:
                # Flatten nested dictionaries
                flat_row = {}
                for key, value in row.items():
                    if isinstance(value, dict):
                        flat_row[key] = json.dumps(value)
                    else:
                        flat_row[key] = value
                writer.writerow(flat_row)
        
        logger.info(f"Exported CSV to {output_file}")
        return str(output_file)
    
    def export_to_excel(
        self,
        data: Dict[str, List[Dict[str, Any]]],
        output_path: str
    ) -> str:
        """
        Export data to Excel format (multiple sheets)
        
        Args:
            data: Dictionary mapping sheet names to lists of data
            output_path: Path to save Excel file
            
        Returns:
            Path to generated Excel file
            
        Note: Requires openpyxl or xlsxwriter library
        """
        try:
            import openpyxl
            from openpyxl import Workbook
            
            wb = Workbook()
            wb.remove(wb.active)  # Remove default sheet
            
            for sheet_name, sheet_data in data.items():
                ws = wb.create_sheet(title=sheet_name[:31])  # Excel sheet name limit
                
                if not sheet_data:
                    continue
                
                # Write headers
                headers = list(sheet_data[0].keys())
                ws.append(headers)
                
                # Write data
                for row in sheet_data:
                    # Flatten nested dictionaries
                    flat_row = []
                    for header in headers:
                        value = row.get(header, '')
                        if isinstance(value, dict):
                            value = json.dumps(value)
                        flat_row.append(value)
                    ws.append(flat_row)
            
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            wb.save(output_file)
            
            logger.info(f"Exported Excel to {output_file}")
            return str(output_file)
            
        except ImportError:
            logger.warning("openpyxl not installed, falling back to CSV export")
            # Fallback: export first sheet as CSV
            if data:
                first_sheet_name = list(data.keys())[0]
                csv_path = output_path.replace('.xlsx', f'_{first_sheet_name}.csv')
                return self.export_to_csv(data[first_sheet_name], csv_path)
        except Exception as e:
            logger.error(f"Failed to export Excel: {e}")
            raise
    
    def export_to_xml(
        self,
        data: Dict[str, Any],
        output_path: str,
        root_element: str = "data"
    ) -> str:
        """
        Export data to XML format
        
        Args:
            data: Data dictionary
            output_path: Path to save XML file
            root_element: Root XML element name
            
        Returns:
            Path to generated XML file
        """
        try:
            import xml.etree.ElementTree as ET
            
            def dict_to_xml(parent, d):
                for key, value in d.items():
                    if isinstance(value, dict):
                        child = ET.SubElement(parent, key)
                        dict_to_xml(child, value)
                    elif isinstance(value, list):
                        for item in value:
                            if isinstance(item, dict):
                                child = ET.SubElement(parent, key)
                                dict_to_xml(child, item)
                            else:
                                child = ET.SubElement(parent, key)
                                child.text = str(item)
                    else:
                        child = ET.SubElement(parent, key)
                        child.text = str(value) if value is not None else ''
            
            root = ET.Element(root_element)
            dict_to_xml(root, data)
            
            tree = ET.ElementTree(root)
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            tree.write(output_file, encoding='utf-8', xml_declaration=True)
            
            logger.info(f"Exported XML to {output_file}")
            return str(output_file)
            
        except Exception as e:
            logger.error(f"Failed to export XML: {e}")
            raise

