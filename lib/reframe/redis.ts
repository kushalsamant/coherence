import { Redis } from "@upstash/redis";

/**
 * Upstash Redis client for usage tracking and rate limiting
 * Uses REST API pattern (more reliable for serverless)
 * 
 * IMPORTANT: Uses lazy initialization to avoid build-time errors.
 * The client is only created when getRedisClient() is actually called at runtime.
 */
let redisInstance: Redis | null = null;

/**
 * Get the Redis client instance (lazy initialization)
 * Only creates the client when first called, not during module import
 */
export function getRedisClient(): Redis {
  if (!redisInstance) {
    redisInstance = new Redis({
      url: process.env.REFRAME_UPSTASH_REDIS_REST_URL || process.env.UPSTASH_REDIS_REST_URL!,
      token: process.env.REFRAME_UPSTASH_REDIS_REST_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN!,
    });
  }
  return redisInstance;
}

