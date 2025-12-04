/**
 * Centralized Redis client for KVSHVL Platform
 * Exports redis clients for different apps
 */

export * from './reframe/redis';

// Re-export for backward compatibility
export { getRedisClient } from './reframe/redis';

