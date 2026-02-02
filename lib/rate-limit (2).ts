/**
 * Rate Limiting Utility
 * Prevents API abuse by limiting requests per IP address
 */

import { getRedisClient } from '@/lib/redis';
import logger from '@/lib/logger';

const redis = getRedisClient();

export interface RateLimitConfig {
  /**
   * Number of requests allowed within the time window
   */
  limit: number;
  /**
   * Time window in seconds
   */
  window: number;
}

export interface RateLimitResult {
  success: boolean;
  limit: number;
  remaining: number;
  reset: number;
}

/**
 * Default rate limit configurations for different types of requests
 */
export const RATE_LIMITS = {
  // API requests: 100 per minute
  api: { limit: 100, window: 60 },
  // Authentication: 5 attempts per 15 minutes
  auth: { limit: 5, window: 900 },
  // Checkout/payments: 10 per hour
  payment: { limit: 10, window: 3600 },
  // Generation requests: 20 per hour
  generation: { limit: 20, window: 3600 },
  // File uploads: 5 per minute
  upload: { limit: 5, window: 60 },
} as const;

/**
 * Check and enforce rate limit for an identifier (e.g., IP address, user ID)
 * 
 * @param identifier - Unique identifier (IP address, user ID, etc.)
 * @param config - Rate limit configuration
 * @returns Rate limit result with success status and metadata
 */
export async function checkRateLimit(
  identifier: string,
  config: RateLimitConfig = RATE_LIMITS.api
): Promise<RateLimitResult> {
  const key = `ratelimit:${identifier}`;
  const now = Date.now();
  const windowStart = now - config.window * 1000;

  try {
    // Get current count from Redis
    const current = await redis.get(key);
    const count = current ? parseInt(String(current), 10) : 0;

    // Calculate reset time (end of current window)
    const resetTime = Math.floor(now / 1000) + config.window;

    if (count >= config.limit) {
      logger.warn(`Rate limit exceeded for ${identifier}`, { count, limit: config.limit });
      return {
        success: false,
        limit: config.limit,
        remaining: 0,
        reset: resetTime,
      };
    }

    // Increment counter
    const newCount = count + 1;
    await redis.set(key, String(newCount), { ex: config.window });

    return {
      success: true,
      limit: config.limit,
      remaining: config.limit - newCount,
      reset: resetTime,
    };
  } catch (error) {
    logger.error('Rate limit check failed:', error instanceof Error ? error : new Error(String(error)));
    // Fail open in case of Redis errors to avoid blocking legitimate users
    return {
      success: true,
      limit: config.limit,
      remaining: config.limit,
      reset: Math.floor(now / 1000) + config.window,
    };
  }
}

/**
 * Get rate limit headers to include in API responses
 */
export function getRateLimitHeaders(result: RateLimitResult): Record<string, string> {
  return {
    'X-RateLimit-Limit': String(result.limit),
    'X-RateLimit-Remaining': String(result.remaining),
    'X-RateLimit-Reset': String(result.reset),
  };
}

/**
 * Extract client identifier from request (IP address)
 * Falls back to a default identifier if IP cannot be determined
 */
export function getClientIdentifier(request: Request): string {
  // Try to get real IP from headers (considering proxies/CDN)
  const forwarded = request.headers.get('x-forwarded-for');
  const realIp = request.headers.get('x-real-ip');
  const cfConnectingIp = request.headers.get('cf-connecting-ip'); // Cloudflare

  const ip = forwarded?.split(',')[0].trim() || realIp || cfConnectingIp || 'unknown';
  
  return ip;
}

/**
 * Reset rate limit for an identifier (useful for testing or admin actions)
 */
export async function resetRateLimit(identifier: string): Promise<void> {
  const key = `ratelimit:${identifier}`;
  await redis.del(key);
  logger.info(`Rate limit reset for ${identifier}`);
}
