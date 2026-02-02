'use client';

import { Card } from '@kushalsamant/design-template';

interface PlatformOverviewCardsProps {
  data: {
    platform_revenue_paise: number;
    platform_costs: {
      total_platform_costs_usd: number;
    };
    platform_margins: {
      net_profit_usd: number;
      net_margin_percent: number;
    };
  };
}

export default function PlatformOverviewCards({ data }: PlatformOverviewCardsProps) {
  const revenueUsd = (data.platform_revenue_paise / 100) * 0.012; // Convert paise to USD
  const costsUsd = data.platform_costs.total_platform_costs_usd;
  const profitUsd = data.platform_margins.net_profit_usd;
  const marginPercent = data.platform_margins.net_margin_percent;

  const cards = [
    {
      title: 'Total Revenue',
      value: `$${revenueUsd.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`,
      subtitle: `₹${(data.platform_revenue_paise / 100).toLocaleString('en-IN')}`,
      color: 'text-green-600',
    },
    {
      title: 'Total Costs',
      value: `$${costsUsd.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`,
      subtitle: 'All projects combined',
      color: 'text-red-600',
    },
    {
      title: 'Net Profit',
      value: `$${profitUsd.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`,
      subtitle: profitUsd >= 0 ? 'Profitable' : 'Loss',
      color: profitUsd >= 0 ? 'text-green-600' : 'text-red-600',
    },
    {
      title: 'Net Margin',
      value: `${marginPercent.toFixed(2)}%`,
      subtitle: marginPercent >= 0 ? 'Positive margin' : 'Negative margin',
      color: marginPercent >= 0 ? 'text-green-600' : 'text-red-600',
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map((card, index) => (
        <Card key={index} className="p-6">
          <h3 className="text-sm font-medium text-muted-foreground mb-1">{card.title}</h3>
          <p className={`text-2xl font-bold ${card.color} mb-1`}>{card.value}</p>
          <p className="text-xs text-muted-foreground">{card.subtitle}</p>
        </Card>
      ))}
    </div>
  );
}


