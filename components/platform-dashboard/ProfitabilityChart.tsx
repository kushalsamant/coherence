'use client';

import { useState, useEffect } from 'react';
import { Card } from '@kushalsamant/design-template';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { getPlatformProjections } from '@/lib/platform-api';
import { logger } from '@/lib/logger';

interface ProfitabilityChartProps {
  project: string;
  days: number;
}

export default function ProfitabilityChart({ project, days }: ProfitabilityChartProps) {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const result = await getPlatformProjections(project === 'platform' ? undefined : project, 12);
        setData(result.projections);
      } catch (err) {
        logger.error('Failed to fetch projections:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [project, days]);

  if (loading || !data) {
    return (
      <Card className="p-6">
        <div className="text-center py-8">Loading profitability projections...</div>
      </Card>
    );
  }

  // Get first scenario's monthly breakdown for chart
  const firstScenario = Object.values(data.scenarios)[0] as any;
  const chartData = firstScenario?.monthly_breakdown || [];

  return (
    <Card className="p-6">
      <h2 className="text-xl font-semibold mb-4">Profitability Projections (12 Months)</h2>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip formatter={(value: number) => `$${value.toFixed(2)}`} />
          <Legend />
          <Line type="monotone" dataKey="revenue_usd" stroke="#10b981" name="Revenue" />
          <Line type="monotone" dataKey="costs_usd" stroke="#ef4444" name="Costs" />
          <Line type="monotone" dataKey="profit_usd" stroke="#3b82f6" name="Profit" />
        </LineChart>
      </ResponsiveContainer>
    </Card>
  );
}


