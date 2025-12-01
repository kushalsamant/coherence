'use client';

import { useState, useMemo } from 'react';

export interface IfcTreeNode {
  id: number;
  name: string;
  type: string;
  children?: IfcTreeNode[];
  expressID?: number;
}

interface IfcObjectTreeProps {
  tree: IfcTreeNode | null;
  onSelectNode: (node: IfcTreeNode) => void;
  selectedNodeId?: number;
  onClose?: () => void;
}

function TreeNode({
  node,
  level = 0,
  onSelect,
  selectedId,
  expandedIds,
  onToggleExpand,
}: {
  node: IfcTreeNode;
  level?: number;
  onSelect: (node: IfcTreeNode) => void;
  selectedId?: number;
  expandedIds: Set<number>;
  onToggleExpand: (id: number) => void;
}) {
  const hasChildren = node.children && node.children.length > 0;
  const isExpanded = expandedIds.has(node.id);
  const isSelected = selectedId === node.id;

  return (
    <div>
      <div
        className={`flex items-center gap-1 px-2 py-1.5 hover:bg-gray-100 rounded cursor-pointer transition-colors ${
          isSelected ? 'bg-primary-50 border-l-2 border-primary-600' : ''
        }`}
        style={{ paddingLeft: `${level * 16 + 8}px` }}
        onClick={() => onSelect(node)}
      >
        {hasChildren ? (
          <button
            onClick={(e) => {
              e.stopPropagation();
              onToggleExpand(node.id);
            }}
            className="p-0.5 hover:bg-gray-200 rounded"
          >
            {isExpanded ? (
              <svg className="w-4 h-4 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            ) : (
              <svg className="w-4 h-4 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            )}
          </button>
        ) : (
          <div className="w-5" />
        )}
        <div className="flex-1 min-w-0">
          <div className="text-sm font-medium text-gray-900 truncate">{node.name}</div>
          <div className="text-xs text-gray-500 truncate">{node.type}</div>
        </div>
      </div>
      {hasChildren && isExpanded && (
        <div>
          {node.children!.map((child) => (
            <TreeNode
              key={child.id}
              node={child}
              level={level + 1}
              onSelect={onSelect}
              selectedId={selectedId}
              expandedIds={expandedIds}
              onToggleExpand={onToggleExpand}
            />
          ))}
        </div>
      )}
    </div>
  );
}

export default function IfcObjectTree({
  tree,
  onSelectNode,
  selectedNodeId,
  onClose,
}: IfcObjectTreeProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [expandedIds, setExpandedIds] = useState<Set<number>>(new Set());

  const toggleExpand = (id: number) => {
    const newExpanded = new Set(expandedIds);
    if (newExpanded.has(id)) {
      newExpanded.delete(id);
    } else {
      newExpanded.add(id);
    }
    setExpandedIds(newExpanded);
  };

  const filteredTree = useMemo(() => {
    if (!tree || !searchQuery.trim()) return tree;

    const filterNode = (node: IfcTreeNode): IfcTreeNode | null => {
      const matchesSearch =
        node.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        node.type.toLowerCase().includes(searchQuery.toLowerCase());

      const filteredChildren = node.children
        ? node.children.map(filterNode).filter((n): n is IfcTreeNode => n !== null)
        : [];

      if (matchesSearch || filteredChildren.length > 0) {
        return {
          ...node,
          children: filteredChildren.length > 0 ? filteredChildren : node.children,
        };
      }

      return null;
    };

    return filterNode(tree);
  }, [tree, searchQuery]);

  const expandAll = () => {
    const allIds = new Set<number>();
    const collectIds = (node: IfcTreeNode) => {
      if (node.children) {
        allIds.add(node.id);
        node.children.forEach(collectIds);
      }
    };
    if (tree) collectIds(tree);
    setExpandedIds(allIds);
  };

  const collapseAll = () => {
    setExpandedIds(new Set());
  };

  if (!tree) {
    return (
      <div className="absolute top-4 right-4 w-80 max-h-[80vh] bg-white/95 backdrop-blur-sm rounded-lg shadow-xl border border-gray-200 p-4 z-50">
        <p className="text-sm text-gray-500 text-center py-8">No object tree available</p>
      </div>
    );
  }

  return (
    <div className="absolute top-4 right-4 w-80 max-h-[80vh] bg-white/95 backdrop-blur-sm rounded-lg shadow-xl border border-gray-200 flex flex-col z-50">
      {/* Header */}
      <div className="p-4 border-b border-gray-200">
        <div className="flex items-center justify-between mb-3">
          <h3 className="font-semibold text-gray-900">Object Tree</h3>
          {onClose && (
            <button
              onClick={onClose}
              className="p-1 hover:bg-gray-100 rounded transition-colors"
              aria-label="Close panel"
            >
              <svg className="w-5 h-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          )}
        </div>

        {/* Search */}
        <div className="relative mb-2">
          <svg className="absolute left-2 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            type="text"
            placeholder="Search objects..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-8 pr-8 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
          {searchQuery && (
            <button
              onClick={() => setSearchQuery('')}
              className="absolute right-2 top-1/2 transform -translate-y-1/2 p-1 hover:bg-gray-100 rounded"
            >
              <svg className="w-4 h-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          )}
        </div>

        {/* Expand/Collapse */}
        <div className="flex gap-2">
          <button
            onClick={expandAll}
            className="text-xs px-2 py-1 text-gray-600 hover:bg-gray-100 rounded transition-colors"
          >
            Expand All
          </button>
          <button
            onClick={collapseAll}
            className="text-xs px-2 py-1 text-gray-600 hover:bg-gray-100 rounded transition-colors"
          >
            Collapse All
          </button>
        </div>
      </div>

      {/* Tree */}
      <div className="flex-1 overflow-y-auto p-2">
        {filteredTree ? (
          <TreeNode
            node={filteredTree}
            onSelect={onSelectNode}
            selectedId={selectedNodeId}
            expandedIds={expandedIds}
            onToggleExpand={toggleExpand}
          />
        ) : (
          <p className="text-sm text-gray-500 text-center py-8">No results found</p>
        )}
      </div>
    </div>
  );
}

