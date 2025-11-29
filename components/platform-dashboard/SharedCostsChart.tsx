'use client';

import { useState, useEffect } from 'react';
import { Card } from '@kushalsamant/design-template';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { getSharedCosts } from '@/lib/platform-api';

export default function SharedCostsChart() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [allocationMethod, setAllocationMethod] = useState('equal');

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const result = await getSharedCosts(allocationMethod);
        setData(result);
      } catch (err) {
        console.error('Failed to fetch shared costs:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [allocationMethod]);

  if (loading || !data) {
    return (
      <Card className="p-6">
        <div className="text-center py-8">Loading shared costs...</div>
      </Card>
    );
  }

  const chartData = [
    {
      name: 'ASK',
      cost: data.allocations.ask || 0,
    },
    {
      name: 'Sketch2BIM',
      cost: data.allocations.sketch2bim || 0,
    },
    {
      name: 'Reframe',
      cost: data.allocations.reframe || 0,
    },
  ];

  const breakdownData = Object.entries(data.cost_breakdown || {}).map(([key, value]) => ({
    name: key.replace('_', ' ').replace(/\b\w/g, (l) => l.toUpperCase()),
    cost: value as number,
  }));

  return (
    <Card className="p-6">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-xl font-semibold">Shared Infrastructure Costs</h2>
        <select
          value={allocationMethod}
          onChange={(e) => setAllocationMethod(e.target.value)}
          className="px-3 py-2 border rounded-md bg-background text-sm"
        >
          <option value="equal">Equal Allocation</option>
          <option value="revenue">Revenue-Based</option>
          <option value="users">User-Based</option>
        </select>
      </div>

      <div className="mb-4">
        <p className="text-sm text-muted-foreground mb-2">
          Total Shared Costs: ${data.total_shared_costs_usd.toFixed(2)}/month
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div>
          <h3 className="text-sm font-medium mb-2">Cost Allocation by Project</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip formatter={(value: number) => `$${value.toFixed(2)}`} />
              <Bar dataKey="cost" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div>
          <h3 className="text-sm font-medium mb-2">Cost Breakdown by Service</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={breakdownData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={80} />
              <YAxis />
              <Tooltip formatter={(value: number) => `$${value.toFixed(2)}`} />
              <Bar dataKey="cost" fill="#10b981" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </Card>
  );
}


