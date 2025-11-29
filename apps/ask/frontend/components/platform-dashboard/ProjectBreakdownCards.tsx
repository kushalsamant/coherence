'use client';

import { Card } from '@kushalsamant/design-template';

interface ProjectBreakdownCardsProps {
  data: {
    platform_costs: {
      project_breakdown: Record<string, {
        total_costs_usd: number;
        groq_costs_usd: number;
        razorpay_fees_usd: number;
      }>;
    };
  };
}

export default function ProjectBreakdownCards({ data }: ProjectBreakdownCardsProps) {
  const projects = ['ask', 'sketch2bim', 'reframe'];
  const breakdown = data.platform_costs.project_breakdown;

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Project Breakdown</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {projects.map((project) => {
          const projectData = breakdown[project] || {};
          const totalCosts = projectData?.total_costs_usd || 0;
          const groqCosts = projectData?.groq_costs_usd || 0;
          const razorpayFees = projectData?.razorpay_fees_usd || 0;

          return (
            <Card key={project} className="p-6">
              <h3 className="text-lg font-semibold mb-4 capitalize">{project}</h3>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">Total Costs:</span>
                  <span className="text-sm font-medium">
                    ${totalCosts.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">Groq API:</span>
                  <span className="text-sm">
                    ${groqCosts.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 6 })}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">Razorpay Fees:</span>
                  <span className="text-sm">
                    ${razorpayFees.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                  </span>
                </div>
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
}

