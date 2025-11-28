'use client';

export interface IfcProperty {
  name: string;
  value: any;
  type?: string;
}

interface IfcPropertyPanelProps {
  properties: IfcProperty[];
  selectedObjectName?: string;
  onClose: () => void;
}

export default function IfcPropertyPanel({
  properties,
  selectedObjectName,
  onClose,
}: IfcPropertyPanelProps) {
  const formatValue = (value: any): string => {
    if (value === null || value === undefined) return 'N/A';
    if (typeof value === 'object') {
      if (Array.isArray(value)) {
        return `[${value.length} items]`;
      }
      return JSON.stringify(value, null, 2);
    }
    return String(value);
  };

  return (
    <div className="absolute top-4 left-4 w-80 max-h-[80vh] bg-white/95 backdrop-blur-sm rounded-lg shadow-xl border border-gray-200 flex flex-col z-50">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200">
        <div>
          <h3 className="font-semibold text-gray-900">Properties</h3>
          {selectedObjectName && (
            <p className="text-sm text-gray-600 mt-1 truncate">{selectedObjectName}</p>
          )}
        </div>
        <button
          onClick={onClose}
          className="p-1 hover:bg-gray-100 rounded transition-colors"
          aria-label="Close panel"
        >
          <svg className="w-5 h-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      {/* Properties List */}
      <div className="flex-1 overflow-y-auto p-4">
        {properties.length === 0 ? (
          <p className="text-sm text-gray-500 text-center py-8">No properties available</p>
        ) : (
          <div className="space-y-3">
            {properties.map((prop, index) => (
              <div key={index} className="border-b border-gray-100 pb-3 last:border-0">
                <div className="flex items-start justify-between gap-2">
                  <div className="flex-1 min-w-0">
                    <div className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">
                      {prop.name}
                    </div>
                    <div className="text-sm text-gray-900 break-words">
                      {typeof prop.value === 'object' && !Array.isArray(prop.value) ? (
                        <pre className="text-xs bg-gray-50 p-2 rounded overflow-x-auto">
                          {formatValue(prop.value)}
                        </pre>
                      ) : (
                        formatValue(prop.value)
                      )}
                    </div>
                    {prop.type && (
                      <div className="text-xs text-gray-400 mt-1">{prop.type}</div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

