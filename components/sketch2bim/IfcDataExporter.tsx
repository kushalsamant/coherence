'use client';

import { useCallback } from 'react';
import * as WebIFC from 'web-ifc';

interface IfcDataExporterProps {
  ifcApi: WebIFC.IfcAPI | null;
  modelID: number | null;
  objectTree: any;
}

interface ExportData {
  expressID: number;
  name: string;
  type: string;
  globalId?: string;
  properties: Array<{ name: string; value: string }>;
}

/**
 * Extract all IFC data for export
 */
async function extractIfcData(
  ifcApi: WebIFC.IfcAPI,
  modelID: number,
  objectTree: any
): Promise<ExportData[]> {
  const data: ExportData[] = [];
  const processedIDs = new Set<number>();

  const processNode = async (node: any) => {
    if (!node || !node.expressID || processedIDs.has(node.expressID)) return;
    
    processedIDs.add(node.expressID);
    
    try {
      const line = ifcApi.GetLine(modelID, node.expressID);
      if (!line) return;

      const exportItem: ExportData = {
        expressID: node.expressID,
        name: node.name || line.Name?.value || 'Unnamed',
        type: node.type || line.type || 'Unknown',
        properties: [],
      };

      // Get GlobalId
      if (line.GlobalId) {
        exportItem.globalId = String(line.GlobalId.value || line.GlobalId);
        exportItem.properties.push({ name: 'GlobalId', value: exportItem.globalId });
      }

      // Get property sets
      try {
        const propertySets = (ifcApi as any).GetPropertySets(modelID, node.expressID, true);
        if (propertySets) {
          for (let i = 0; i < propertySets.length; i++) {
            const ps = propertySets[i];
            if (ps && ps.Properties) {
              for (let j = 0; j < ps.Properties.length; j++) {
                const prop = ps.Properties[j];
                if (prop && prop.Name && prop.NominalValue) {
                  exportItem.properties.push({
                    name: prop.Name.value || String(prop.Name),
                    value: prop.NominalValue.value || String(prop.NominalValue),
                  });
                }
              }
            }
          }
        }
      } catch (err) {
        if (process.env.NODE_ENV === 'development') {
          console.warn('Failed to get properties for element');
        }
      }

      data.push(exportItem);
    } catch (err) {
      if (process.env.NODE_ENV === 'development') {
        console.warn('Failed to process node');
      }
    }

    // Process children recursively
    if (node.children && Array.isArray(node.children)) {
      for (const child of node.children) {
        await processNode(child);
      }
    }
  };

  if (objectTree) {
    await processNode(objectTree);
  }

  return data;
}

/**
 * Convert data to CSV format
 */
function convertToCSV(data: ExportData[]): string {
  if (data.length === 0) return '';

  // Collect all unique property names
  const allPropertyNames = new Set<string>();
  data.forEach((item) => {
    item.properties.forEach((prop) => {
      allPropertyNames.add(prop.name);
    });
  });

  const propertyNames = Array.from(allPropertyNames).sort();

  // Create header
  const headers = ['ExpressID', 'Name', 'Type', 'GlobalId', ...propertyNames];
  const csvRows = [headers.join(',')];

  // Create rows
  data.forEach((item) => {
    const row: string[] = [
      String(item.expressID),
      `"${item.name.replace(/"/g, '""')}"`,
      `"${item.type.replace(/"/g, '""')}"`,
      item.globalId ? `"${item.globalId}"` : '',
    ];

    // Add property values in the same order as headers
    propertyNames.forEach((propName) => {
      const prop = item.properties.find((p) => p.name === propName);
      row.push(prop ? `"${String(prop.value).replace(/"/g, '""')}"` : '');
    });

    csvRows.push(row.join(','));
  });

  return csvRows.join('\n');
}

/**
 * Convert data to Excel-compatible format (TSV for simplicity, can be enhanced with xlsx library)
 */
function convertToExcel(data: ExportData[]): string {
  // For now, return CSV which Excel can open
  // Can be enhanced with xlsx library for proper .xlsx format
  return convertToCSV(data);
}

/**
 * Download file
 */
function downloadFile(content: string, filename: string, mimeType: string) {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

export default function IfcDataExporter({ ifcApi, modelID, objectTree }: IfcDataExporterProps) {
  const handleExportCSV = useCallback(async () => {
    if (!ifcApi || modelID === null) {
      alert('IFC model not loaded');
      return;
    }

    try {
      const data = await extractIfcData(ifcApi, modelID, objectTree);
      const csv = convertToCSV(data);
      downloadFile(csv, 'ifc-export.csv', 'text/csv');
    } catch (err) {
      if (process.env.NODE_ENV === 'development') {
        console.error('Export failed');
      }
      alert('Failed to export data. Please try again.');
    }
  }, [ifcApi, modelID, objectTree]);

  const handleExportExcel = useCallback(async () => {
    if (!ifcApi || modelID === null) {
      alert('IFC model not loaded');
      return;
    }

    try {
      const data = await extractIfcData(ifcApi, modelID, objectTree);
      const excel = convertToExcel(data);
      // Use .csv extension for now (Excel can open it)
      // Can be changed to .xlsx when xlsx library is added
      downloadFile(excel, 'ifc-export.csv', 'text/csv');
    } catch (err) {
      if (process.env.NODE_ENV === 'development') {
        console.error('Export failed');
      }
      alert('Failed to export data. Please try again.');
    }
  }, [ifcApi, modelID, objectTree]);

  return (
    <div className="flex gap-2">
      <button
        onClick={handleExportCSV}
        className="px-3 py-1.5 rounded text-sm font-medium bg-gray-100 text-gray-700 hover:bg-gray-200 transition-colors"
        title="Export to CSV"
      >
        Export CSV
      </button>
      <button
        onClick={handleExportExcel}
        className="px-3 py-1.5 rounded text-sm font-medium bg-gray-100 text-gray-700 hover:bg-gray-200 transition-colors"
        title="Export to Excel"
      >
        Export Excel
      </button>
    </div>
  );
}

export { extractIfcData, convertToCSV, convertToExcel };

