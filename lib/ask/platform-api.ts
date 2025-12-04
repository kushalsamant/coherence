/**
 * Platform-wide API Client for KVSHVL Platform Feasibility Analysis
 * Fetches data from all projects (ASK, Sketch2BIM, Reframe)
 */

import logger from "@/lib/logger";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Type definitions
export interface UnitEconomics {
  project: string;
  revenue_per_user_paise: number;
  revenue_per_user_usd: number;
  cost_per_user_usd: number;
  contribution_margin_usd: number;
  gross_margin_percent: number;
  break_even_users: number;
}

export interface BreakEvenAnalysis {
  fixed_costs_usd: number;
  variable_cost_per_user_usd: number;
  revenue_per_user_usd: number;
  contribution_margin_per_user_usd: number;
  break_even_users: number | null;
  break_even_revenue_usd: number | null;
  is_feasible: boolean;
}

export interface ProfitabilityProjection {
  month: number;
  users: number;
  revenue_usd: number;
  costs_usd: number;
  profit_usd: number;
  margin_percent: number;
  cumulative_profit_usd: number;
}

export interface Scenario {
  description: string;
  users: number;
  monthly_revenue_usd: number;
  monthly_costs_usd: number;
  monthly_profit_usd: number;
  gross_margin_percent: number;
  net_margin_percent: number;
  annual_revenue_usd: number;
  annual_costs_usd: number;
  annual_profit_usd: number;
  is_profitable: boolean;
}

export interface MarginAnalysis {
  total_revenue_usd: number;
  variable_costs_usd: number;
  fixed_costs_usd: number;
  shared_infrastructure_costs_usd: number;
  total_costs_usd: number;
  gross_profit_usd: number;
  gross_margin_percent: number;
  net_profit_usd: number;
  net_margin_percent: number;
}

export interface SharedCosts {
  allocation_method: string;
  total_shared_costs_usd: number;
  cost_breakdown: Record<string, number>;
  allocations: Record<string, number>;
}

export interface CrossProjectMetrics {
  total_unique_users: number;
  single_project_users: number;
  multi_project_users: number;
  multi_project_user_percent: number;
  avg_projects_per_user: number;
  platform_revenue_per_multi_user_paise: number;
  user_distribution: Record<string, number>;
}

export interface ConsolidatedPlatformView {
  period_days: number;
  platform_costs: {
    total_platform_costs_usd: number;
    total_groq_costs_usd: number;
    total_razorpay_fees_usd: number;
    total_infrastructure_costs_usd: number;
    project_breakdown: Record<string, unknown>;
  };
  platform_revenue_paise: number;
  platform_margins: MarginAnalysis;
  cross_project_metrics: CrossProjectMetrics;
  timestamp: string;
}

// API Client helper
async function fetchAPI<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  
  try {
    // Get auth token from session if available
    const token = typeof window !== 'undefined' 
      ? localStorage.getItem('auth_token') 
      : null;
    
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
        ...options?.headers,
      },
      credentials: 'include', // Include cookies for auth
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: response.statusText }));
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    // Error already thrown, no need to log again
    throw error;
  }
}

// Platform Feasibility API Functions

export async function getPlatformUnitEconomics(
  project?: string,
  days: number = 30
): Promise<{
  period_days: number;
  unit_economics: Record<string, UnitEconomics>;
  shared_infrastructure_allocation: Record<string, number>;
}> {
  const params = new URLSearchParams({ days: days.toString() });
  if (project) {
    params.append('project', project);
  }
  return fetchAPI(`/api/feasibility/platform/unit-economics?${params.toString()}`);
}

export async function getPlatformBreakEven(
  project?: string,
  days: number = 30
): Promise<{
  project: string;
  period_days: number;
  break_even_analysis: BreakEvenAnalysis;
}> {
  const params = new URLSearchParams({ days: days.toString() });
  if (project) {
    params.append('project', project);
  }
  return fetchAPI(`/api/feasibility/platform/break-even?${params.toString()}`);
}

export async function getPlatformProjections(
  project?: string,
  months: number = 12
): Promise<{
  project: string;
  projections: {
    current_users: number;
    projection_months: number;
    scenarios: Record<string, {
      growth_rate_percent: number;
      final_users: number;
      final_monthly_revenue_usd: number;
      final_monthly_profit_usd: number;
      cumulative_profit_usd: number;
      monthly_breakdown: ProfitabilityProjection[];
    }>;
  };
}> {
  const params = new URLSearchParams({ months: months.toString() });
  if (project) {
    params.append('project', project);
  }
  return fetchAPI(`/api/feasibility/platform/projections?${params.toString()}`);
}

export async function getPlatformScenarios(
  project?: string
): Promise<{
  project: string;
  scenarios: {
    base_users: number;
    scenarios: {
      pessimistic: Scenario;
      realistic: Scenario;
      optimistic: Scenario;
    };
  };
}> {
  const params = new URLSearchParams();
  if (project) {
    params.append('project', project);
  }
  return fetchAPI(`/api/feasibility/platform/scenarios?${params.toString()}`);
}

export async function getPlatformMargins(
  project?: string,
  days: number = 30
): Promise<{
  project: string;
  period_days: number;
  margins: MarginAnalysis;
}> {
  const params = new URLSearchParams({ days: days.toString() });
  if (project) {
    params.append('project', project);
  }
  return fetchAPI(`/api/feasibility/platform/margins?${params.toString()}`);
}

export async function getSharedCosts(
  allocationMethod: string = 'equal'
): Promise<SharedCosts> {
  return fetchAPI(`/api/feasibility/platform/shared-costs?allocation_method=${allocationMethod}`);
}

export async function getPlatformConsolidated(
  days: number = 30
): Promise<ConsolidatedPlatformView> {
  return fetchAPI(`/api/feasibility/platform/consolidated?days=${days}`);
}

export async function getCrossProjectMetrics(
  days: number = 30
): Promise<{
  period_days: number;
  cross_project_metrics: CrossProjectMetrics;
}> {
  return fetchAPI(`/api/feasibility/platform/cross-project?days=${days}`);
}

// Cost and Usage API Functions (from existing monitoring endpoints)

export async function getCosts(days: number = 30): Promise<unknown> {
  return fetchAPI(`/api/monitoring/costs?days=${days}`);
}

export async function getUsage(days: number = 30): Promise<unknown> {
  return fetchAPI(`/api/monitoring/usage?days=${days}`);
}

export async function getSummary(): Promise<unknown> {
  return fetchAPI('/api/monitoring/summary');
}

export async function getAlerts(): Promise<{
  alerts: Array<{
    level: string;
    message: string;
    current_value?: number;
    threshold?: number;
    details?: Record<string, unknown>;
    timestamp: string;
  }>;
  count: number;
  critical_count: number;
  warning_count: number;
}> {
  return fetchAPI('/api/monitoring/alerts');
}

// Admin check
export async function checkAdminAccess(): Promise<{ is_admin: boolean; email?: string }> {
  try {
    // Try to access an admin-only endpoint to check access
    await fetchAPI('/api/feasibility/platform/consolidated?days=1');
    return { is_admin: true };
  } catch (error) {
    if (error instanceof Error && (error.message?.includes('403') || error.message?.includes('Admin access'))) {
      return { is_admin: false };
    }
    // Re-throw other errors
    throw error;
  }
}

