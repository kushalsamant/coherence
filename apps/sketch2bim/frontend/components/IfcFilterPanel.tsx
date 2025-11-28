'use client';

import { useState, useCallback } from 'react';

export interface FilterOptions {
  types: Set<string>;
  systems: Set<string>;
  customAttributes: Map<string, string>;
}

interface IfcFilterPanelProps {
  onFilterChange: (filters: FilterOptions) => void;
  availableTypes: string[];
  onClose: () => void;
}

export default function IfcFilterPanel({
  onFilterChange,
  availableTypes,
  onClose,
}: IfcFilterPanelProps) {
  const [selectedTypes, setSelectedTypes] = useState<Set<string>>(new Set());
  const [selectedSystems, setSelectedSystems] = useState<Set<string>>(new Set());
  const [searchTerm, setSearchTerm] = useState('');

  // Common IFC types
  const commonTypes = [
    'IfcWall',
    'IfcDoor',
    'IfcWindow',
    'IfcSlab',
    'IfcRoof',
    'IfcBeam',
    'IfcColumn',
    'IfcStair',
    'IfcRailing',
    'IfcSpace',
    'IfcBuildingElementProxy',
  ];

  // System categories
  const systemCategories = ['Architectural', 'Structural', 'MEP', 'Other'];

  const allTypes = [...new Set([...commonTypes, ...availableTypes])].sort();

  const toggleType = useCallback(
    (type: string) => {
      const newTypes = new Set(selectedTypes);
      if (newTypes.has(type)) {
        newTypes.delete(type);
      } else {
        newTypes.add(type);
      }
      setSelectedTypes(newTypes);
      onFilterChange({
        types: newTypes,
        systems: selectedSystems,
        customAttributes: new Map(),
      });
    },
    [selectedTypes, selectedSystems, onFilterChange]
  );

  const toggleSystem = useCallback(
    (system: string) => {
      const newSystems = new Set(selectedSystems);
      if (newSystems.has(system)) {
        newSystems.delete(system);
      } else {
        newSystems.add(system);
      }
      setSelectedSystems(newSystems);
      onFilterChange({
        types: selectedTypes,
        systems: newSystems,
        customAttributes: new Map(),
      });
    },
    [selectedTypes, selectedSystems, onFilterChange]
  );

  const clearFilters = useCallback(() => {
    setSelectedTypes(new Set());
    setSelectedSystems(new Set());
    setSearchTerm('');
    onFilterChange({
      types: new Set(),
      systems: new Set(),
      customAttributes: new Map(),
    });
  }, [onFilterChange]);

  const filteredTypes = allTypes.filter((type) =>
    type.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="absolute top-2 left-2 sm:top-4 sm:left-4 bg-white rounded-lg shadow-lg p-2 sm:p-4 w-[calc(100vw-1rem)] sm:w-80 max-h-[80vh] overflow-y-auto z-50">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-800">Filter Model</h3>
        <button
          onClick={onClose}
          className="text-gray-500 hover:text-gray-700 transition-colors"
          title="Close"
        >
          <svg
            className="w-5 h-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>

      {/* Search */}
      <div className="mb-4">
        <input
          type="text"
          placeholder="Search types..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
        />
      </div>

      {/* System Filters */}
      <div className="mb-4">
        <h4 className="text-sm font-semibold text-gray-700 mb-2">System</h4>
        <div className="flex flex-wrap gap-2">
          {systemCategories.map((system) => (
            <button
              key={system}
              onClick={() => toggleSystem(system)}
              className={`px-3 py-1 rounded text-sm transition-colors ${
                selectedSystems.has(system)
                  ? 'bg-primary-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {system}
            </button>
          ))}
        </div>
      </div>

      {/* Type Filters */}
      <div className="mb-4">
        <div className="flex items-center justify-between mb-2">
          <h4 className="text-sm font-semibold text-gray-700">Element Types</h4>
          <button
            onClick={clearFilters}
            className="text-xs text-primary-600 hover:text-primary-700"
          >
            Clear All
          </button>
        </div>
        <div className="max-h-64 overflow-y-auto border border-gray-200 rounded-md p-2">
          {filteredTypes.length > 0 ? (
            filteredTypes.map((type) => (
              <label
                key={type}
                className="flex items-center space-x-2 py-1 hover:bg-gray-50 cursor-pointer"
              >
                <input
                  type="checkbox"
                  checked={selectedTypes.has(type)}
                  onChange={() => toggleType(type)}
                  className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                />
                <span className="text-sm text-gray-700">{type}</span>
              </label>
            ))
          ) : (
            <div className="text-sm text-gray-500 py-2">No types found</div>
          )}
        </div>
      </div>

      {/* Active Filters Summary */}
      {(selectedTypes.size > 0 || selectedSystems.size > 0) && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <div className="text-xs text-gray-600 mb-2">
            Active Filters: {selectedTypes.size + selectedSystems.size}
          </div>
        </div>
      )}
    </div>
  );
}

