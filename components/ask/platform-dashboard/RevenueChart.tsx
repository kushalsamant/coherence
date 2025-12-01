'use client';

import { Card } from '@kushalsamant/design-template';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface RevenueChartProps {
  data: {
    platform_revenue_paise: number;
    platform_costs: {
      total_platform_costs_usd: number;
    };
    platform_margins: {
      net_profit_usd: number;
    };
  };
}

export default function RevenueChart({ data }: RevenueChartProps) {
  const revenueUsd = (data.platform_revenue_paise / 100) * 0.012;
  const costsUsd = data.platform_costs.total_platform_costs_usd;
  const profitUsd = data.platform_margins.net_profit_usd;

  const chartData = [
    {
      name: 'Platform',
      Revenue: revenueUsd,
      Costs: costsUsd,
      Profit: profitUsd,
    },
  ];

  return (
    <Card className="p-6">
      <h2 className="text-xl font-semibold mb-4">Revenue vs Costs</h2>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip formatter={(value: number) => `$${value.toFixed(2)}`} />
          <Legend />
          <Bar dataKey="Revenue" fill="#10b981" />
          <Bar dataKey="Costs" fill="#ef4444" />
          <Bar dataKey="Profit" fill={profitUsd >= 0 ? '#3b82f6' : '#f59e0b'} />
        </BarChart>
      </ResponsiveContainer>
    </Card>
  );
}

