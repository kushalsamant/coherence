'use client';

import { useState, useEffect } from 'react';
import { useSession } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import { Card } from '@kushalsamant/design-template';
import { getPlatformConsolidated, getPlatformUnitEconomics, getPlatformScenarios, checkAdminAccess } from '@/lib/platform-api';
import PlatformOverviewCards from '@/components/platform-dashboard/PlatformOverviewCards';
import ProjectBreakdownCards from '@/components/platform-dashboard/ProjectBreakdownCards';
import CostBreakdownChart from '@/components/platform-dashboard/CostBreakdownChart';
import RevenueChart from '@/components/platform-dashboard/RevenueChart';
import ProfitabilityChart from '@/components/platform-dashboard/ProfitabilityChart';
import UnitEconomicsTable from '@/components/platform-dashboard/UnitEconomicsTable';
import BreakEvenAnalysis from '@/components/platform-dashboard/BreakEvenAnalysis';
import ScenarioComparison from '@/components/platform-dashboard/ScenarioComparison';
import SharedCostsChart from '@/components/platform-dashboard/SharedCostsChart';
import ProjectComparisonChart from '@/components/platform-dashboard/ProjectComparisonChart';

export default function PlatformDashboard() {
  const { data: session, status } = useSession();
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isAdmin, setIsAdmin] = useState<boolean | null>(null);
  const [days, setDays] = useState(30);
  const [project, setProject] = useState<string | null>(null);
  
  // Data state
  const [consolidated, setConsolidated] = useState<any>(null);
  const [unitEconomics, setUnitEconomics] = useState<any>(null);
  const [scenarios, setScenarios] = useState<any>(null);

  // Check authentication and admin access
  useEffect(() => {
    const checkAccess = async () => {
      if (status === 'unauthenticated') {
        router.push('/sign-in');
        return;
      }
      
      if (status === 'authenticated' && session) {
        try {
          const adminCheck = await checkAdminAccess();
          setIsAdmin(adminCheck.is_admin);
          
          if (!adminCheck.is_admin) {
            setError('Access denied. Admin privileges required to view this dashboard.');
            setLoading(false);
            return;
          }
        } catch (err: any) {
          console.error('Failed to check admin access:', err);
          if (err.message?.includes('403') || err.message?.includes('Admin')) {
            setIsAdmin(false);
            setError('Access denied. Admin privileges required to view this dashboard.');
            setLoading(false);
            return;
          }
          setError('Failed to verify admin access. Please try again.');
          setLoading(false);
          return;
        }
      }
    };

    checkAccess();
  }, [status, session, router]);

  // Fetch data
  useEffect(() => {
    if (status !== 'authenticated' || isAdmin !== true) return;

    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);

        const [consolidatedData, unitEconData, scenariosData] = await Promise.all([
          getPlatformConsolidated(days),
          getPlatformUnitEconomics(project || undefined, days),
          getPlatformScenarios(project || undefined),
        ]);

        setConsolidated(consolidatedData);
        setUnitEconomics(unitEconData);
        setScenarios(scenariosData);
      } catch (err: any) {
        console.error('Failed to fetch dashboard data:', err);
        setError(err.message || 'Failed to load dashboard data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [days, project, status, isAdmin]);

  if (status === 'loading' || loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
            <p className="text-muted-foreground">Loading dashboard...</p>
          </div>
        </div>
      </div>
    );
  }

  if (status === 'unauthenticated') {
    return null; // Will redirect
  }

  if (isAdmin === false || (error && error.includes('Access denied'))) {
    return (
      <div className="container mx-auto px-4 py-8">
        <Card className="p-6">
          <div className="text-center">
            <h2 className="text-2xl font-bold text-destructive mb-4">Access Denied</h2>
            <p className="text-muted-foreground mb-4">
              You do not have admin privileges to access this dashboard.
            </p>
            <button
              onClick={() => router.push('/')}
              className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90"
            >
              Go to Home
            </button>
          </div>
        </Card>
      </div>
    );
  }

  if (error && !error.includes('Access denied')) {
    return (
      <div className="container mx-auto px-4 py-8">
        <Card className="p-6">
          <div className="text-center">
            <h2 className="text-2xl font-bold text-destructive mb-4">Error Loading Dashboard</h2>
            <p className="text-muted-foreground mb-4">{error}</p>
            <button
              onClick={() => window.location.reload()}
              className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90"
            >
              Retry
            </button>
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Platform Dashboard</h1>
        <p className="text-muted-foreground">
          Comprehensive business feasibility analysis for KVSHVL Platform
        </p>
      </div>

      {/* Controls */}
      <div className="mb-6 flex flex-wrap gap-4 items-center">
        <div className="flex items-center gap-2">
          <label htmlFor="days" className="text-sm font-medium">
            Period:
          </label>
          <select
            id="days"
            value={days}
            onChange={(e) => setDays(Number(e.target.value))}
            className="px-3 py-2 border rounded-md bg-background"
          >
            <option value={7}>Last 7 days</option>
            <option value={30}>Last 30 days</option>
            <option value={90}>Last 90 days</option>
            <option value={365}>Last year</option>
          </select>
        </div>

        <div className="flex items-center gap-2">
          <label htmlFor="project" className="text-sm font-medium">
            Project:
          </label>
          <select
            id="project"
            value={project || 'all'}
            onChange={(e) => setProject(e.target.value === 'all' ? null : e.target.value)}
            className="px-3 py-2 border rounded-md bg-background"
          >
            <option value="all">All Projects</option>
            <option value="ask">ASK</option>
            <option value="sketch2bim">Sketch2BIM</option>
            <option value="reframe">Reframe</option>
          </select>
        </div>
      </div>

      {/* Overview Cards */}
      {consolidated && (
        <PlatformOverviewCards data={consolidated} />
      )}

      {/* Project Breakdown */}
      {consolidated && (
        <div className="mt-6">
          <ProjectBreakdownCards data={consolidated} />
        </div>
      )}

      {/* Charts Row 1 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        {consolidated && (
          <>
            <CostBreakdownChart data={consolidated.platform_costs} />
            <RevenueChart data={consolidated} />
          </>
        )}
      </div>

      {/* Unit Economics */}
      {unitEconomics && (
        <div className="mt-6">
          <UnitEconomicsTable data={unitEconomics} />
        </div>
      )}

      {/* Break-Even Analysis */}
      <div className="mt-6">
        <BreakEvenAnalysis project={project || 'platform'} days={days} />
      </div>

      {/* Profitability Projections */}
      {consolidated && (
        <div className="mt-6">
          <ProfitabilityChart project={project || 'platform'} days={days} />
        </div>
      )}

      {/* Scenario Comparison */}
      {scenarios && (
        <div className="mt-6">
          <ScenarioComparison data={scenarios} />
        </div>
      )}

      {/* Shared Infrastructure Costs */}
      <div className="mt-6">
        <SharedCostsChart />
      </div>

      {/* Project Comparison */}
      {consolidated && (
        <div className="mt-6">
          <ProjectComparisonChart data={consolidated} />
        </div>
      )}
    </div>
  );
}

