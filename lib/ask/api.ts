/**
 * API Client for ASK Research Tool
 * TypeScript functions to call FastAPI endpoints
 */

import logger from "@/lib/logger";

const API_BASE_URL = process.env.NEXT_PUBLIC_PLATFORM_API_URL || 'http://localhost:8000';

// Type definitions matching backend models
export interface QAPair {
  id: number;
  question_number: number;
  theme: string;
  question: string;
  style: string | null;
  answer: string;
  keywords: string | null;
  is_used: boolean;
  created_timestamp: string | null;
  question_image: string | null;
  answer_image: string | null;
  question_image_url: string | null;
  answer_image_url: string | null;
  answer_image_urls: string[];
}

export interface QAPairListResponse {
  items: QAPair[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface Theme {
  name: string;
  count: number;
}

export interface ThemeListResponse {
  themes: Theme[];
  total: number;
}

export interface Stats {
  total_qa_pairs: number;
  total_themes: number;
  themes: Theme[];
  total_questions: number;
  total_answers: number;
}

export interface GenerateRequest {
  theme?: string;
  count?: number;
}

export interface GenerateResponse {
  success: boolean;
  message: string;
  qa_pairs?: QAPair[];
  error?: string;
}

// API Client functions
async function fetchAPI<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
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

// Q&A Pairs endpoints
export async function getQAPairs(
  theme?: string,
  page: number = 1,
  pageSize: number = 20
): Promise<QAPairListResponse> {
  const params = new URLSearchParams({
    page: page.toString(),
    page_size: pageSize.toString(),
  });
  
  if (theme) {
    params.append('theme', theme);
  }
  
  return fetchAPI<QAPairListResponse>(`/api/ask/qa-pairs?${params.toString()}`);
}

export async function getQAPair(questionNumber: number): Promise<QAPair> {
  return fetchAPI<QAPair>(`/api/ask/qa-pairs/${questionNumber}`);
}

// Themes endpoints
export async function getThemes(): Promise<ThemeListResponse> {
  return fetchAPI<ThemeListResponse>('/api/ask/themes');
}

// Stats endpoint
export async function getStats(): Promise<Stats> {
  return fetchAPI<Stats>('/api/ask/stats');
}

// Generation State
export interface GenerationState {
  session_id: string;
  keywords: string;
  last_question: string | null;
  last_answer: string | null;
  qa_chain: Array<{ question: string; answer: string }>;
}

// New Generation Endpoints
export interface GenerateStartRequest {
  keywords: string;
  session_id?: string;
}

export interface GenerateStartResponse {
  success: boolean;
  message: string;
  session_id: string;
  question: string | null;
  state: GenerationState | null;
  error?: string;
}

export interface GenerateNextRequest {
  session_id: string;
  keywords?: string;
}

export interface GenerateNextResponse {
  success: boolean;
  message: string;
  question: string | null;
  answer: string | null;
  state: GenerationState | null;
  error?: string;
}

export interface UpdateKeywordsRequest {
  session_id: string;
  keywords: string;
}

export interface UpdateKeywordsResponse {
  success: boolean;
  message: string;
  state: GenerationState | null;
  error?: string;
}

// Start generation with keywords
export async function startGeneration(request: GenerateStartRequest): Promise<GenerateStartResponse> {
  return fetchAPI<GenerateStartResponse>('/api/ask/generate/start', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

// Generate next Q&A in chain
export async function generateNext(request: GenerateNextRequest): Promise<GenerateNextResponse> {
  return fetchAPI<GenerateNextResponse>('/api/ask/generate/next', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

// Update keywords
export async function updateKeywords(request: UpdateKeywordsRequest): Promise<UpdateKeywordsResponse> {
  return fetchAPI<UpdateKeywordsResponse>('/api/ask/generate/update-keywords', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

// Legacy Generate endpoint (for backward compatibility)
export async function generateContent(request: GenerateRequest): Promise<GenerateResponse> {
  return fetchAPI<GenerateResponse>('/api/ask/generate', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

// Payment interfaces
export interface Payment {
  id: number;
  amount: number;
  currency: string;
  status: string;
  product_type: string;
  credits_added: number;
  created_at: string;
  completed_at?: string;
}

export interface CheckoutSession {
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
}

// Payment API functions
export async function getPaymentHistory(): Promise<Payment[]> {
  return fetchAPI<Payment[]>('/api/ask/payments/history', {
    headers: {
      // Add auth token here when auth is implemented
    },
  });
}

export async function createCheckoutSession(
  priceIdOrTier: string,
  paymentType: 'one_time' | 'subscription' = 'one_time'
): Promise<CheckoutSession> {
  return fetchAPI<CheckoutSession>(
    `/api/ask/payments/checkout?price_id=${encodeURIComponent(priceIdOrTier)}&payment_type=${paymentType}`,
    {
      method: 'POST',
      headers: {
        // Add auth token here when auth is implemented
      },
    }
  );
}

interface Subscription {
  id: string;
  plan_id: string;
  status: string;
  current_start: number;
  current_end: number;
  charge_at: number;
}

export async function getSubscriptions(): Promise<{
  subscriptions: Subscription[];
  error?: string;
}> {
  return fetchAPI<{ subscriptions: Subscription[]; error?: string }>('/api/ask/payments/subscriptions', {
    headers: {
      // Add auth token here when auth is implemented
    },
  });
}

export async function cancelSubscription(subscriptionId: string): Promise<{
  status: string;
  subscription: Subscription;
}> {
  return fetchAPI<{ status: string; subscription: Subscription }>(
    `/api/ask/payments/subscriptions/${subscriptionId}/cancel`,
    {
      method: 'POST',
      headers: {
        // Add auth token here when auth is implemented
      },
    }
  );
}

export async function resumeSubscription(subscriptionId: string): Promise<{
  status: string;
  subscription: Subscription;
}> {
  return fetchAPI<{ status: string; subscription: Subscription }>(
    `/api/ask/payments/subscriptions/${subscriptionId}/resume`,
    {
      method: 'POST',
      headers: {
        // Add auth token here when auth is implemented
      },
    }
  );
}

