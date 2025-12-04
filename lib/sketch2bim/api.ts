/**
 * API client for backend communication
 */
import axios, { AxiosInstance } from 'axios';
import { getSession } from 'next-auth/react';

const API_URL = process.env.NEXT_PUBLIC_PLATFORM_API_URL || 'http://localhost:8000';

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: `${API_URL}/api/sketch2bim`,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

// Add auth token to requests
apiClient.interceptors.request.use(async (config) => {
  const session = await getSession();
  
  if (session && (session as any).accessToken) {
    config.headers.Authorization = `Bearer ${(session as any).accessToken}`;
  }
  
  return config;
});

// Types
export interface User {
  id: number;
  email: string;
  name?: string;
  credits: number;
  subscription_tier: string;
  subscription_status: string;
  subscription_expires_at?: string | null;
  subscription_auto_renew?: boolean;
  razorpay_subscription_id?: string | null;
}

export interface Job {
  id: string;
  status: 'queued' | 'processing' | 'completed' | 'failed' | 'review';
  progress: number;
  sketch_filename: string;
  project_type?: 'architecture';
  detection_confidence?: number;
  ifc_url?: string;
  dwg_url?: string;
  rvt_url?: string;
  sketchup_url?: string;  // OBJ format for SketchUp
  preview_image_url?: string;
  error_message?: string;
  legend_data?: {
    scale?: string;
    scale_ratio?: number;
    room_labels?: Record<string, string>;
    confidence?: number;
  };
  legend_detected?: boolean;
  created_at: string;
  completed_at?: string;
  expires_at?: string;
  cost_usd?: number;
  requires_review?: boolean;
  symbol_summary?: SymbolSummary | null;
}

export interface JobStatus {
  id: string;
  status: string;
  progress: number;
  message?: string;
  error?: string;
}

export interface SymbolSummary {
  total_detected: number;
  categories: Record<string, number>;
  sample_labels: string[];
  enabled: boolean;
  inference_ms?: number;
  model_path?: string;
}

export interface SymbolDetectionEntry {
  label: string;
  display_name?: string;
  category?: string;
  ifc_type?: string;
  bbox: number[];
  confidence: number;
  area_pixels?: number;
  source?: string;
}

export interface PlanData {
  rooms: any[];
  walls: any[];
  openings: any[];
  symbols?: SymbolDetectionEntry[];
  symbol_metadata?: Record<string, any>;
  confidence: number;
}

// API functions
export const api = {
  // Auth
  async getCurrentUser(): Promise<User> {
    const { data } = await apiClient.get('/auth/me');
    return data;
  },

  // Jobs
  async uploadSketch(file: File): Promise<{ job_id: string; credits_remaining: number }> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('project_type', 'architecture');
    
    const { data } = await apiClient.post('/generate/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return data;
  },

  async batchUploadSketches(files: File[]): Promise<{
    batch_id: string;
    job_ids: string[];
    total_jobs: number;
    credits_used: number;
    credits_remaining: number;
  }> {
    const formData = new FormData();
    files.forEach(file => formData.append('files', file));
    formData.append('project_type', 'architecture');
    
    const { data } = await apiClient.post('/generate/batch-upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return data;
  },

  async getJobStatus(jobId: string): Promise<JobStatus> {
    const { data } = await apiClient.get(`/generate/status/${jobId}`);
    return data;
  },

  async getJob(jobId: string): Promise<Job> {
    const { data } = await apiClient.get(`/generate/jobs/${jobId}`);
    return data;
  },

  async getJobPlanData(jobId: string): Promise<PlanData> {
    const { data } = await apiClient.get(`/generate/jobs/${jobId}/plan-data`);
    return data;
  },

  async listJobs(limit: number = 50, offset: number = 0): Promise<Job[]> {
    const { data } = await apiClient.get('/generate/jobs', {
      params: { limit, offset },
    });
    return data;
  },

  async deleteJob(jobId: string): Promise<void> {
    await apiClient.delete(`/generate/jobs/${jobId}`);
  },

  // Payments
  async getPaymentHistory(): Promise<Array<{
    id: number;
    amount: number;
    currency: string;
    status: string;
    product_type: string;
    credits_added: number;
    created_at: string;
    completed_at?: string;
  }>> {
    const { data } = await apiClient.get('/payments/history');
    return data;
  },

  async createCheckoutSession(priceIdOrTier: string, paymentType: 'one_time' | 'subscription' = 'one_time'): Promise<{
    order_id?: string;
    subscription_id?: string;
    plan_id?: string;
    amount: number;
    currency: string;
    key_id: string;
    name: string;
    description: string;
    prefill: {
      email: string;
      name: string;
    };
    theme: {
      color: string;
    };
    success_url: string;
    cancel_url: string;
    payment_type: 'one_time' | 'subscription';
  }> {
    // Backend accepts tier names ('week', 'month', 'year') and payment type
    const { data } = await apiClient.post(`/payments/checkout?price_id=${encodeURIComponent(priceIdOrTier)}&payment_type=${paymentType}`);
    return data;
  },

  // Subscriptions
  async getSubscriptions(): Promise<{
    subscriptions: Array<any>;
    error?: string;
  }> {
    const { data } = await apiClient.get('/payments/subscriptions');
    return data;
  },

  async cancelSubscription(subscriptionId: string): Promise<{
    status: string;
    subscription: any;
  }> {
    const { data } = await apiClient.post(`/payments/subscriptions/${subscriptionId}/cancel`);
    return data;
  },

  async resumeSubscription(subscriptionId: string): Promise<{
    status: string;
    subscription: any;
  }> {
    const { data } = await apiClient.post(`/payments/subscriptions/${subscriptionId}/resume`);
    return data;
  },

  // Settings
  async updateProfile(data: { name?: string }): Promise<User> {
    const { data: user } = await apiClient.patch('/auth/me', data);
    return user;
  },

  // Iterations
  async createIteration(jobId: string, data: {
    parent_iteration_id?: string;
    name?: string;
    notes?: string;
    changes_json?: any;
  }): Promise<{
    id: string;
    job_id: string;
    parent_iteration_id?: string;
    ifc_url?: string;
    ifc_filename?: string;
    changes_json?: any;
    change_summary?: string;
    name?: string;
    notes?: string;
    created_at: string;
  }> {
    const { data: iteration } = await apiClient.post(`/iterations/jobs/${jobId}/iterations`, data);
    return iteration;
  },

  async listIterations(jobId: string): Promise<Array<{
    id: string;
    job_id: string;
    parent_iteration_id?: string;
    ifc_url?: string;
    ifc_filename?: string;
    changes_json?: any;
    change_summary?: string;
    name?: string;
    notes?: string;
    created_at: string;
  }>> {
    const { data } = await apiClient.get(`/iterations/jobs/${jobId}/iterations`);
    return data;
  },

  async getIteration(iterationId: string): Promise<{
    id: string;
    job_id: string;
    parent_iteration_id?: string;
    ifc_url?: string;
    ifc_filename?: string;
    changes_json?: any;
    change_summary?: string;
    name?: string;
    notes?: string;
    created_at: string;
  }> {
    const { data } = await apiClient.get(`/iterations/iterations/${iterationId}`);
    return data;
  },

  async updateIteration(iterationId: string, data: {
    name?: string;
    notes?: string;
    changes_json?: any;
  }): Promise<{
    id: string;
    job_id: string;
    parent_iteration_id?: string;
    ifc_url?: string;
    ifc_filename?: string;
    changes_json?: any;
    change_summary?: string;
    name?: string;
    notes?: string;
    created_at: string;
  }> {
    const { data: iteration } = await apiClient.patch(`/iterations/iterations/${iterationId}`, data);
    return iteration;
  },

  async deleteIteration(iterationId: string): Promise<void> {
    await apiClient.delete(`/iterations/iterations/${iterationId}`);
  },

  // Layout Variations
  async generateVariations(jobId: string, numVariations: number = 3, constraints?: any): Promise<Array<{
    id: string;
    job_id: string;
    variation_number: number;
    plan_data?: any;
    confidence?: number;
    ifc_url?: string;
    preview_image_url?: string;
    created_at: string;
  }>> {
    const { data } = await apiClient.post(`/variations/jobs/${jobId}/variations`, {
      num_variations: numVariations,
      constraints
    });
    return data;
  },

  async listVariations(jobId: string): Promise<Array<{
    id: string;
    job_id: string;
    variation_number: number;
    plan_data?: any;
    confidence?: number;
    ifc_url?: string;
    preview_image_url?: string;
    created_at: string;
  }>> {
    const { data } = await apiClient.get(`/variations/jobs/${jobId}/variations`);
    return data;
  },

  async getVariation(variationId: string): Promise<{
    id: string;
    job_id: string;
    variation_number: number;
    plan_data?: any;
    confidence?: number;
    ifc_url?: string;
    preview_image_url?: string;
    created_at: string;
  }> {
    const { data } = await apiClient.get(`/variations/variations/${variationId}`);
    return data;
  },

  async deleteVariation(variationId: string): Promise<void> {
    await apiClient.delete(`/variations/variations/${variationId}`);
  },

  // Referrals
  async generateReferral(): Promise<{
    referral_code: string;
    referral_url: string;
  }> {
    const { data } = await apiClient.post('/referrals/generate');
    return data;
  },

  async getReferralCode(): Promise<{
    referral_code: string;
    referral_url: string;
  }> {
    const { data } = await apiClient.get('/referrals/code');
    return data;
  },

  async getReferralStats(): Promise<{
    total_referrals: number;
    completed_referrals: number;
    credits_earned: number;
  }> {
    const { data } = await apiClient.get('/referrals/stats');
    return data;
  },

  // Monitoring (admin only)
  async getMonitoringStatus(): Promise<{
    database: {
      size_mb: number;
      limit_mb: number;
      percentage_used: number;
      status: string;
    };
    redis: {
      commands_today: number;
      limit_per_day: number;
      percentage_used: number;
      status: string;
    };
    storage: {
      size_gb: number;
      cost_estimate_usd: number;
      status: string;
    };
    timestamp: string;
  }> {
    const { data } = await apiClient.get('/monitoring/status');
    return data;
  },

  async getMonitoringAlerts(): Promise<{
    alerts: Array<{
      resource: string;
      level: string;
      message: string;
      current: number;
      limit: number;
      percentage: number;
      timestamp: string;
    }>;
    count: number;
    critical_count: number;
    warning_count: number;
  }> {
    const { data } = await apiClient.get('/monitoring/alerts');
    return data;
  },

  async getMonitoringRecommendations(): Promise<{
    recommendations: Array<{
      service: string;
      priority: string;
      message: string;
      current_usage: string;
      options: string[];
    }>;
    count: number;
    high_priority_count: number;
  }> {
    const { data } = await apiClient.get('/monitoring/recommendations');
    return data;
  },
};

export default apiClient;

