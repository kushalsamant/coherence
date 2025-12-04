import { getRedisClient } from "./redis";
import logger from "@/lib/logger";

/**
 * NextAuth Database Cleanup Utilities
 * Handles deletion of user records from NextAuth's Upstash Redis adapter
 */

const redis = getRedisClient();

/**
 * Delete all NextAuth data for a user
 * This includes user record, sessions, and OAuth accounts
 * 
 * NextAuth with UpstashRedisAdapter stores data with these key patterns:
 * - user:{userId} - User record
 * - user:email:{email} - Email to user ID mapping
 * - user:account:{provider}:{providerAccountId} - OAuth account mapping
 * - session:{sessionToken} - Session data
 * 
 * @param userId - User ID
 * @param email - User email (for cleaning up email mapping)
 */
export async function deleteUserFromDatabase(userId: string, email?: string): Promise<void> {
  try {
    // Delete main user record
    await redis.del(`user:${userId}`);

    // Delete email mapping if email provided
    if (email) {
      await redis.del(`user:email:${email}`);
    }

    // Find and delete all sessions for this user
    // NextAuth stores sessions with pattern: session:{sessionToken}
    // We need to scan for sessions that belong to this user
    const sessionKeys = await scanKeys("session:*");
    for (const key of sessionKeys) {
      const session = await redis.get(key);
      if (session && typeof session === "object" && "userId" in session) {
        const sessionObj = session as Record<string, unknown>;
        if (sessionObj.userId === userId) {
          await redis.del(key);
        }
      }
    }

    // Find and delete OAuth accounts
    // Pattern: user:account:{provider}:{providerAccountId}
    const accountKeys = await scanKeys("user:account:*");
    for (const key of accountKeys) {
      const account = await redis.get(key);
      if (account && typeof account === "object" && "userId" in account) {
        const accountObj = account as Record<string, unknown>;
        if (accountObj.userId === userId) {
          await redis.del(key);
        }
      }
    }

    logger.info(`Deleted all NextAuth data for user ${userId}`);
  } catch (error) {
    logger.error("Error deleting user from database:", error);
    throw error;
  }
}

/**
 * Helper function to scan Redis keys by pattern
 * @param pattern - Redis key pattern (e.g., "session:*")
 * @returns Array of matching keys
 */
async function scanKeys(pattern: string): Promise<string[]> {
  const keys: string[] = [];
  let cursor = 0;

  try {
    do {
      const result = await redis.scan(cursor, {
        match: pattern,
        count: 100,
      });
      
      cursor = typeof result[0] === 'string' ? parseInt(result[0], 10) : result[0];
      keys.push(...result[1]);
    } while (cursor !== 0);
  } catch (error) {
    logger.error(`Error scanning keys with pattern ${pattern}:`, error);
  }

  return keys;
}

