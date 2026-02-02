'use client';

import { Card } from '@kushalsamant/design-template';

interface ScenarioComparisonProps {
  data: {
    scenarios: {
      pessimistic: any;
      realistic: any;
      optimistic: any;
    };
  };
}

export default function ScenarioComparison({ data }: ScenarioComparisonProps) {
  const scenarios = data.scenarios;
  const scenarioList = [
    { key: 'pessimistic', label: 'Pessimistic', color: 'text-red-600' },
    { key: 'realistic', label: 'Realistic', color: 'text-blue-600' },
    { key: 'optimistic', label: 'Optimistic', color: 'text-green-600' },
  ];

  return (
    <Card className="p-6">
      <h2 className="text-xl font-semibold mb-4">Scenario Analysis</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {scenarioList.map(({ key, label, color }) => {
          const scenario = scenarios[key as keyof typeof scenarios];
          if (!scenario) return null;

          return (
            <div key={key} className="border rounded-lg p-4">
              <h3 className={`text-lg font-semibold mb-3 ${color}`}>{label}</h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Users:</span>
                  <span className="font-medium">{scenario.users.toLocaleString()}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Monthly Revenue:</span>
                  <span className="font-medium">
                    ${scenario.monthly_revenue_usd.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Monthly Costs:</span>
                  <span className="font-medium">
                    ${scenario.monthly_costs_usd.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Monthly Profit:</span>
                  <span
                    className={`font-medium ${
                      scenario.monthly_profit_usd >= 0 ? 'text-green-600' : 'text-red-600'
                    }`}
                  >
                    ${scenario.monthly_profit_usd.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Net Margin:</span>
                  <span
                    className={`font-medium ${
                      scenario.net_margin_percent >= 0 ? 'text-green-600' : 'text-red-600'
                    }`}
                  >
                    {scenario.net_margin_percent.toFixed(2)}%
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Annual Profit:</span>
                  <span
                    className={`font-medium ${
                      scenario.annual_profit_usd >= 0 ? 'text-green-600' : 'text-red-600'
                    }`}
                  >
                    ${scenario.annual_profit_usd.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                  </span>
                </div>
                <div className="pt-2 border-t">
                  <span
                    className={`text-xs font-medium ${
                      scenario.is_profitable ? 'text-green-600' : 'text-red-600'
                    }`}
                  >
                    {scenario.is_profitable ? '✓ Profitable' : '✗ Not Profitable'}
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </Card>
  );
}


