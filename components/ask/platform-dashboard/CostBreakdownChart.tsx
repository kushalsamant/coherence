'use client';

import { Card } from '@kushalsamant/design-template';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

interface CostBreakdownChartProps {
  data: {
    total_groq_costs_usd: number;
    total_razorpay_fees_usd: number;
    total_infrastructure_costs_usd: number;
    total_other_variable_costs_usd: number;
  };
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

export default function CostBreakdownChart({ data }: CostBreakdownChartProps) {
  const chartData = [
    { name: 'Groq API', value: data.total_groq_costs_usd },
    { name: 'Razorpay Fees', value: data.total_razorpay_fees_usd },
    { name: 'Infrastructure', value: data.total_infrastructure_costs_usd },
    { name: 'Other Variable', value: data.total_other_variable_costs_usd },
  ].filter(item => item.value > 0);

  return (
    <Card className="p-6">
      <h2 className="text-xl font-semibold mb-4">Cost Breakdown</h2>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip formatter={(value: number) => `$${value.toFixed(2)}`} />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </Card>
  );
}

