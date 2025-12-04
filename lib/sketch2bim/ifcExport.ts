/**
 * IFC Data Export Utilities
 * Export IFC model data to CSV format
 * Note: Excel export removed due to security vulnerabilities in xlsx package
 */

import logger from "@/lib/logger";
import * as WebIFC from 'web-ifc';

interface IfcElement {
  expressID: number;
  type: string;
  name: string;
  globalId?: string;
  properties?: Record<string, string | number | boolean | null>;
}

/**
 * Convert IFC elements to CSV format
 */
export function exportToCSV(
  elements: IfcElement[],
  filename: string = 'ifc_export.csv'
): void {
  if (elements.length === 0) {
    alert('No elements to export');
    return;
  }

  // Get all unique property keys
  const allKeys = new Set<string>(['ExpressID', 'Type', 'Name', 'GlobalID']);
  elements.forEach((elem) => {
    if (elem.properties) {
      Object.keys(elem.properties).forEach((key) => allKeys.add(key));
    }
  });

  const headers = Array.from(allKeys);
  const rows: string[][] = [headers];

  // Add data rows
  elements.forEach((elem) => {
    const row: string[] = [];
    headers.forEach((header) => {
      switch (header) {
        case 'ExpressID':
          row.push(String(elem.expressID));
          break;
        case 'Type':
          row.push(elem.type || '');
          break;
        case 'Name':
          row.push(elem.name || '');
          break;
        case 'GlobalID':
          row.push(elem.globalId || '');
          break;
        default:
          row.push(
            elem.properties?.[header]
              ? String(elem.properties[header])
              : ''
          );
      }
    });
    rows.push(row);
  });

  // Convert to CSV string
  const csvContent = rows
    .map((row) =>
      row
        .map((cell) => {
          // Escape cells containing commas, quotes, or newlines
          if (cell.includes(',') || cell.includes('"') || cell.includes('\n')) {
            return `"${cell.replace(/"/g, '""')}"`;
          }
          return cell;
        })
        .join(',')
    )
    .join('\n');

  // Add BOM for Excel compatibility
  const BOM = '\uFEFF';
  const blob = new Blob([BOM + csvContent], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}

/**
 * Extract IFC elements from WebIFC model for export
 */
export async function extractIfcElements(
  ifcApi: WebIFC.IfcAPI,
  modelID: number
): Promise<IfcElement[]> {
  const elements: IfcElement[] = [];

  try {
    // Get all element types
    const elementTypes = [
      'IFCWALL',
      'IFCDOOR',
      'IFCWINDOW',
      'IFCSPACE',
      'IFCSLAB',
      'IFCCOLUMN',
      'IFCBEAM',
      'IFCROOF',
      'IFCSTAIR',
      'IFCFURNISHINGELEMENT',
      'IFCBUILDINGELEMENTPROXY',
    ];

    for (const elementType of elementTypes) {
      try {
        const lineIDs = ifcApi.GetLineIDsWithType(modelID, (ifcApi as WebIFC.IfcAPI & { IFC: Record<string, number> }).IFC[elementType]);
        for (let i = 0; i < lineIDs.size(); i++) {
          const expressID = lineIDs.get(i);
          try {
            const element = ifcApi.GetLine(modelID, expressID);
            
            const ifcElement: IfcElement = {
              expressID,
              type: elementType,
              name: element.Name?.value || '',
              globalId: element.GlobalId?.value || '',
              properties: {},
            };

            // Extract properties
            if (element.IsDefinedBy) {
              element.IsDefinedBy.forEach((rel: unknown) => {
                const relation = rel as {RelatingPropertyDefinition?: {HasProperties?: unknown[]}};
                if (relation.RelatingPropertyDefinition) {
                  const pset = relation.RelatingPropertyDefinition;
                  if (pset.HasProperties) {
                    pset.HasProperties.forEach((prop: unknown) => {
                      const property = prop as {Name?: {value?: string}, NominalValue?: {value?: unknown}, wrappedValue?: unknown};
                      const propName = property.Name?.value || '';
                      let propValue: unknown = null;
                      
                      if (property.NominalValue) {
                        propValue = property.NominalValue.value;
                      } else if (property.wrappedValue) {
                        propValue = property.wrappedValue;
                      }

                      if (propName && propValue !== null && (typeof propValue === 'string' || typeof propValue === 'number' || typeof propValue === 'boolean')) {
                        ifcElement.properties![propName] = propValue;
                      }
                    });
                  }
                }
              });
            }

            elements.push(ifcElement);
          } catch (err) {
            // Skip elements that can't be read
            if (process.env.NODE_ENV === 'development') {
              logger.warn(`Failed to read element ${expressID}`);
            }
          }
        }
      } catch (err) {
        // Skip element types that aren't available
        if (process.env.NODE_ENV === 'development') {
          logger.warn(`Element type ${elementType} not available`);
        }
      }
    }
  } catch (error) {
    if (process.env.NODE_ENV === 'development') {
      logger.error('Failed to extract IFC elements');
    }
  }

  return elements;
}

