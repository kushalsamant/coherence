/**
 * Rate Limiting Utility
 * Protects API routes from abuse using Upstash Rate Limit
 */

import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";

// Initialize Redis for rate limiting
const redis = new Redis({
  url: process.env.UPSTASH_REDIS_REST_URL || process.env.PLATFORM_UPSTASH_REDIS_REST_URL || "",
  token: process.env.UPSTASH_REDIS_REST_TOKEN || process.env.PLATFORM_UPSTASH_REDIS_REST_TOKEN || "",
});

// Create rate limiters with different limits for different endpoints

// Standard API rate limit: 10 requests per 10 seconds
export const standardRateLimit = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(10, "10 s"),
  analytics: true,
  prefix: "@ratelimit/api",
});

// Strict rate limit for expensive operations: 3 requests per minute
export const strictRateLimit = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(3, "1 m"),
  analytics: true,
  prefix: "@ratelimit/strict",
});

// Authentication endpoints: 5 attempts per minute
export const authRateLimit = new Ratelimit({
  redis,
  limiter: Ratelimit.slidingWindow(5, "1 m"),
  analytics: true,
  prefix: "@ratelimit/auth",
});

/**
 * Get client identifier from request
 * Uses IP address as identifier
 */
export function getClientIdentifier(request: Request): string {
  // Try to get IP from headers (for proxied requests)
  const forwarded = request.headers.get("x-forwarded-for");
  const realIp = request.headers.get("x-real-ip");
  
  if (forwarded) {
    return forwarded.split(',')[0].trim();
  }
  
  if (realIp) {
    return realIp;
  }
  
  // Fallback to a default identifier
  return "unknown";
}

/**
 * Apply rate limit and return appropriate response if exceeded
 */
export async function applyRateLimit(
  request: Request,
  rateLimiter: Ratelimit = standardRateLimit
): Promise<{ success: boolean; response?: Response }> {
  const identifier = getClientIdentifier(request);
  const { success, limit, reset, remaining } = await rateLimiter.limit(identifier);
  
  if (!success) {
    return {
      success: false,
      response: new Response(
        JSON.stringify({
          error: "Too many requests",
          message: "Rate limit exceeded. Please try again later.",
          reset: new Date(reset).toISOString(),
        }),
        {
          status: 429,
          headers: {
            "Content-Type": "application/json",
            "X-RateLimit-Limit": limit.toString(),
            "X-RateLimit-Remaining": remaining.toString(),
            "X-RateLimit-Reset": reset.toString(),
          },
        }
      ),
    };
  }
  
  return { success: true };
}

