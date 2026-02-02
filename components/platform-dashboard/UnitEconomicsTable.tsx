'use client';

import { Card } from '@kushalsamant/design-template';

interface UnitEconomicsTableProps {
  data: {
    unit_economics: Record<
      string,
      {
        project: string;
        revenue_per_user_usd: number;
        cost_per_user_usd: number;
        contribution_margin_usd: number;
        gross_margin_percent: number;
      }
    >;
  };
}

export default function UnitEconomicsTable({ data }: UnitEconomicsTableProps) {
  const unitEcon = data.unit_economics;

  return (
    <Card className="p-6">
      <h2 className="text-xl font-semibold mb-4">Unit Economics</h2>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b">
              <th className="text-left p-2">Project</th>
              <th className="text-right p-2">Revenue/User (USD)</th>
              <th className="text-right p-2">Cost/User (USD)</th>
              <th className="text-right p-2">Contribution Margin (USD)</th>
              <th className="text-right p-2">Gross Margin %</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(unitEcon).map(([project, metrics]) => (
              <tr key={project} className="border-b">
                <td className="p-2 capitalize font-medium">{project}</td>
                <td className="p-2 text-right">${metrics.revenue_per_user_usd.toFixed(2)}</td>
                <td className="p-2 text-right">${metrics.cost_per_user_usd.toFixed(6)}</td>
                <td
                  className={`p-2 text-right ${
                    metrics.contribution_margin_usd >= 0 ? 'text-green-600' : 'text-red-600'
                  }`}
                >
                  ${metrics.contribution_margin_usd.toFixed(2)}
                </td>
                <td
                  className={`p-2 text-right ${
                    metrics.gross_margin_percent >= 0 ? 'text-green-600' : 'text-red-600'
                  }`}
                >
                  {metrics.gross_margin_percent.toFixed(2)}%
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  );
}


