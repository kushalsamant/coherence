'use client';

import { Card } from '@kushalsamant/design-template';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface ProjectComparisonChartProps {
  data: {
    platform_costs: {
      project_breakdown: Record<string, {
        total_costs_usd: number;
        groq_costs_usd: number;
        razorpay_fees_usd: number;
        infrastructure_costs_usd: number;
      }>;
    };
    platform_revenue_paise: number;
  };
}

export default function ProjectComparisonChart({ data }: ProjectComparisonChartProps) {
  const projects = ['ask', 'sketch2bim', 'reframe'];
  const breakdown = data.platform_costs.project_breakdown;
  
  // Calculate revenue per project (assuming equal distribution for now)
  // In production, this should come from actual project revenue data
  const revenuePerProject = data.platform_revenue_paise / 3;
  const revenuePerProjectUsd = (revenuePerProject / 100) * 0.012;

  const chartData = projects.map((project) => {
    const projectData = breakdown[project] || {};
    const costs = projectData.total_costs_usd || 0;
    const profit = revenuePerProjectUsd - costs;

    return {
      name: project.toUpperCase(),
      Revenue: revenuePerProjectUsd,
      Costs: costs,
      Profit: profit,
    };
  });

  return (
    <Card className="p-6">
      <h2 className="text-xl font-semibold mb-4">Project Comparison</h2>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip formatter={(value: number) => `$${value.toFixed(2)}`} />
          <Legend />
          <Bar dataKey="Revenue" fill="#10b981" />
          <Bar dataKey="Costs" fill="#ef4444" />
          <Bar dataKey="Profit" fill="#3b82f6" />
        </BarChart>
      </ResponsiveContainer>
      
      <div className="mt-4 grid grid-cols-3 gap-4 text-sm">
        {chartData.map((project) => (
          <div key={project.name} className="text-center">
            <p className="font-medium mb-1">{project.name}</p>
            <p className="text-muted-foreground">
              Margin: {((project.Profit / project.Revenue) * 100).toFixed(1)}%
            </p>
          </div>
        ))}
      </div>
    </Card>
  );
}

