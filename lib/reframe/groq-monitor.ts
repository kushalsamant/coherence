/**
 * Groq Usage Monitoring for Reframe
 * Tracks token usage and costs, stores in Redis
 */

import { getRedisClient } from "./redis";

// Groq pricing for llama-3.1-8b-instant (Reframe model)
const GROQ_INPUT_COST_PER_MILLION = 0.05; // $0.05 per 1M input tokens
const GROQ_OUTPUT_COST_PER_MILLION = 0.08; // $0.08 per 1M output tokens

// Alert thresholds
const DAILY_COST_THRESHOLD = parseFloat(process.env.REFRAME_GROQ_DAILY_COST_THRESHOLD || process.env.GROQ_DAILY_COST_THRESHOLD || "10.0"); // $10/day
const MONTHLY_COST_THRESHOLD = parseFloat(process.env.REFRAME_GROQ_MONTHLY_COST_THRESHOLD || process.env.GROQ_MONTHLY_COST_THRESHOLD || "50.0"); // $50/month

/**
 * Calculate cost in USD for Groq API usage
 */
export function calculateGroqCost(inputTokens: number, outputTokens: number): number {
  const inputCost = (inputTokens / 1_000_000) * GROQ_INPUT_COST_PER_MILLION;
  const outputCost = (outputTokens / 1_000_000) * GROQ_OUTPUT_COST_PER_MILLION;
  return inputCost + outputCost;
}

/**
 * Track Groq API usage in Redis
 */
export async function trackGroqUsage(
  inputTokens: number,
  outputTokens: number,
  requestType: string = "reframe"
): Promise<void> {
  try {
    const redis = getRedisClient();
    const now = new Date();
    const dateKey = now.toISOString().split('T')[0]; // YYYY-MM-DD
    const monthKey = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`; // YYYY-MM
    
    const totalTokens = inputTokens + outputTokens;
    const cost = calculateGroqCost(inputTokens, outputTokens);
    
    // Track daily usage
    const dailyKey = `groq:usage:daily:${dateKey}`;
    await redis.incrby(`${dailyKey}:requests`, 1);
    await redis.incrby(`${dailyKey}:input_tokens`, inputTokens);
    await redis.incrby(`${dailyKey}:output_tokens`, outputTokens);
    await redis.incrbyfloat(`${dailyKey}:cost`, cost);
    
    // Track monthly usage
    const monthlyKey = `groq:usage:monthly:${monthKey}`;
    await redis.incrby(`${monthlyKey}:requests`, 1);
    await redis.incrby(`${monthlyKey}:input_tokens`, inputTokens);
    await redis.incrby(`${monthlyKey}:output_tokens`, outputTokens);
    await redis.incrbyfloat(`${monthlyKey}:cost`, cost);
    
    // Set expiration (30 days for daily, 90 days for monthly)
    await redis.expire(dailyKey, 30 * 24 * 60 * 60);
    await redis.expire(monthlyKey, 90 * 24 * 60 * 60);
    
    // Store individual request for detailed tracking
    const requestKey = `groq:request:${Date.now()}:${Math.random().toString(36).substr(2, 9)}`;
    await redis.hset(requestKey, {
      input_tokens: String(inputTokens),
      output_tokens: String(outputTokens),
      total_tokens: String(totalTokens),
      cost: String(cost),
      request_type: requestType,
      timestamp: now.toISOString()
    });
    await redis.expire(requestKey, 30 * 24 * 60 * 60); // 30 days
    
    // Check for alerts
    await checkAndAlert(redis, dateKey, monthKey);
  } catch (error) {
    console.error("Failed to track Groq usage:", error);
    // Don't throw - tracking failure shouldn't break the request
  }
}

/**
 * Get daily usage statistics
 */
export async function getDailyUsage(date?: string): Promise<{
  date: string;
  requests: number;
  inputTokens: number;
  outputTokens: number;
  totalTokens: number;
  cost: number;
}> {
  try {
    const redis = getRedisClient();
    const dateKey = date || new Date().toISOString().split('T')[0];
    const dailyKey = `groq:usage:daily:${dateKey}`;
    
    const requests = parseInt((await redis.get(`${dailyKey}:requests`)) || "0", 10);
    const inputTokens = parseInt((await redis.get(`${dailyKey}:input_tokens`)) || "0", 10);
    const outputTokens = parseInt((await redis.get(`${dailyKey}:output_tokens`)) || "0", 10);
    const cost = parseFloat((await redis.get(`${dailyKey}:cost`)) || "0");
    
    return {
      date: dateKey,
      requests,
      inputTokens,
      outputTokens,
      totalTokens: inputTokens + outputTokens,
      cost: Math.round(cost * 1000000) / 1000000 // Round to 6 decimal places
    };
  } catch (error) {
    console.error("Failed to get daily usage:", error);
    return {
      date: date || new Date().toISOString().split('T')[0],
      requests: 0,
      inputTokens: 0,
      outputTokens: 0,
      totalTokens: 0,
      cost: 0
    };
  }
}

/**
 * Get monthly usage statistics
 */
export async function getMonthlyUsage(year?: number, month?: number): Promise<{
  year: number;
  month: number;
  requests: number;
  inputTokens: number;
  outputTokens: number;
  totalTokens: number;
  cost: number;
}> {
  try {
    const redis = getRedisClient();
    const now = new Date();
    const yearNum = year || now.getFullYear();
    const monthNum = month || now.getMonth() + 1;
    const monthKey = `${yearNum}-${String(monthNum).padStart(2, '0')}`;
    const monthlyKey = `groq:usage:monthly:${monthKey}`;
    
    const requests = parseInt((await redis.get(`${monthlyKey}:requests`)) || "0", 10);
    const inputTokens = parseInt((await redis.get(`${monthlyKey}:input_tokens`)) || "0", 10);
    const outputTokens = parseInt((await redis.get(`${monthlyKey}:output_tokens`)) || "0", 10);
    const cost = parseFloat((await redis.get(`${monthlyKey}:cost`)) || "0");
    
    return {
      year: yearNum,
      month: monthNum,
      requests,
      inputTokens,
      outputTokens,
      totalTokens: inputTokens + outputTokens,
      cost: Math.round(cost * 1000000) / 1000000
    };
  } catch (error) {
    console.error("Failed to get monthly usage:", error);
    const now = new Date();
    return {
      year: year || now.getFullYear(),
      month: month || now.getMonth() + 1,
      requests: 0,
      inputTokens: 0,
      outputTokens: 0,
      totalTokens: 0,
      cost: 0
    };
  }
}

/**
 * Check usage and send alerts if thresholds exceeded
 */
async function checkAndAlert(redis: any, dateKey: string, monthKey: string): Promise<void> {
  try {
    const dailyKey = `groq:usage:daily:${dateKey}`;
    const monthlyKey = `groq:usage:monthly:${monthKey}`;
    
    const dailyCost = parseFloat((await redis.get(`${dailyKey}:cost`)) || "0");
    const monthlyCost = parseFloat((await redis.get(`${monthlyKey}:cost`)) || "0");
    
    // Check daily threshold
    if (dailyCost > DAILY_COST_THRESHOLD) {
      const alertKey = `groq:alert:daily:${dateKey}`;
      const alreadyAlerted = await redis.get(alertKey);
      
      if (!alreadyAlerted) {
        console.warn(`[GROQ ALERT] Daily cost ($${dailyCost.toFixed(2)}) exceeds threshold ($${DAILY_COST_THRESHOLD})`);
        await redis.set(alertKey, "1", { EX: 24 * 60 * 60 }); // Alert once per day
      }
    }
    
    // Check monthly threshold
    if (monthlyCost > MONTHLY_COST_THRESHOLD) {
      const alertKey = `groq:alert:monthly:${monthKey}`;
      const alreadyAlerted = await redis.get(alertKey);
      
      if (!alreadyAlerted) {
        console.warn(`[GROQ ALERT] Monthly cost ($${monthlyCost.toFixed(2)}) exceeds threshold ($${MONTHLY_COST_THRESHOLD})`);
        await redis.set(alertKey, "1", { EX: 30 * 24 * 60 * 60 }); // Alert once per month
      }
    }
  } catch (error) {
    console.error("Failed to check alerts:", error);
  }
}

/**
 * Get usage statistics for the last N days
 */
export async function getUsageStats(days: number = 30): Promise<{
  periodDays: number;
  totalRequests: number;
  totalInputTokens: number;
  totalOutputTokens: number;
  totalTokens: number;
  totalCost: number;
  dailyBreakdown: Array<{
    date: string;
    requests: number;
    cost: number;
  }>;
}> {
  try {
    const redis = getRedisClient();
    const now = new Date();
    const dailyBreakdown: Array<{ date: string; requests: number; cost: number }> = [];
    let totalRequests = 0;
    let totalInputTokens = 0;
    let totalOutputTokens = 0;
    let totalCost = 0;
    
    // Get usage for each day in the period
    for (let i = 0; i < days; i++) {
      const date = new Date(now);
      date.setDate(date.getDate() - i);
      const dateKey = date.toISOString().split('T')[0];
      
      const daily = await getDailyUsage(dateKey);
      dailyBreakdown.push({
        date: dateKey,
        requests: daily.requests,
        cost: daily.cost
      });
      
      totalRequests += daily.requests;
      totalInputTokens += daily.inputTokens;
      totalOutputTokens += daily.outputTokens;
      totalCost += daily.cost;
    }
    
    return {
      periodDays: days,
      totalRequests,
      totalInputTokens,
      totalOutputTokens,
      totalTokens: totalInputTokens + totalOutputTokens,
      totalCost: Math.round(totalCost * 1000000) / 1000000,
      dailyBreakdown: dailyBreakdown.reverse() // Oldest to newest
    };
  } catch (error) {
    console.error("Failed to get usage stats:", error);
    return {
      periodDays: days,
      totalRequests: 0,
      totalInputTokens: 0,
      totalOutputTokens: 0,
      totalTokens: 0,
      totalCost: 0,
      dailyBreakdown: []
    };
  }
}

