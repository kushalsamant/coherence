'use client';

import { useState, useEffect } from 'react';
import { Card } from '@kushalsamant/design-template';
import { getPlatformBreakEven } from '@/lib/platform-api';

interface BreakEvenAnalysisProps {
  project: string;
  days: number;
}

export default function BreakEvenAnalysis({ project, days }: BreakEvenAnalysisProps) {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const result = await getPlatformBreakEven(project === 'platform' ? undefined : project, days);
        setData(result.break_even_analysis);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [project, days]);

  if (loading) {
    return (
      <Card className="p-6">
        <div className="text-center py-8">Loading break-even analysis...</div>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="p-6">
        <div className="text-center text-destructive">Error: {error}</div>
      </Card>
    );
  }

  if (!data) return null;

  return (
    <Card className="p-6">
      <h2 className="text-xl font-semibold mb-4">Break-Even Analysis</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <p className="text-sm text-muted-foreground mb-1">Fixed Costs</p>
          <p className="text-lg font-semibold">${data.fixed_costs_usd.toFixed(2)}</p>
        </div>
        <div>
          <p className="text-sm text-muted-foreground mb-1">Variable Cost per User</p>
          <p className="text-lg font-semibold">${data.variable_cost_per_user_usd.toFixed(6)}</p>
        </div>
        <div>
          <p className="text-sm text-muted-foreground mb-1">Revenue per User</p>
          <p className="text-lg font-semibold">${data.revenue_per_user_usd.toFixed(2)}</p>
        </div>
        <div>
          <p className="text-sm text-muted-foreground mb-1">Contribution Margin per User</p>
          <p
            className={`text-lg font-semibold ${
              data.contribution_margin_per_user_usd >= 0 ? 'text-green-600' : 'text-red-600'
            }`}
          >
            ${data.contribution_margin_per_user_usd.toFixed(2)}
          </p>
        </div>
        <div>
          <p className="text-sm text-muted-foreground mb-1">Break-Even Users</p>
          <p className="text-lg font-semibold">
            {data.break_even_users !== null ? data.break_even_users.toLocaleString() : 'N/A'}
          </p>
        </div>
        <div>
          <p className="text-sm text-muted-foreground mb-1">Feasible</p>
          <p
            className={`text-lg font-semibold ${
              data.is_feasible ? 'text-green-600' : 'text-red-600'
            }`}
          >
            {data.is_feasible ? 'Yes' : 'No'}
          </p>
        </div>
      </div>
    </Card>
  );
}


