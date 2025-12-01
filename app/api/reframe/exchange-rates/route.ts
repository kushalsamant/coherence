import { NextResponse } from "next/server";
import { getRedisClient } from "@/lib/reframe/redis";

export const dynamic = 'force-dynamic';

// Fallback rates (used if API fails)
const FALLBACK_RATES = {
  USD: 0.012,   // 1 INR = 0.012 USD (approx $83 per USD)
  EUR: 0.011,   // 1 INR = 0.011 EUR (approx €90 per EUR)
  GBP: 0.0095,  // 1 INR = 0.0095 GBP (approx £105 per GBP)
};

const CACHE_KEY = "exchange_rates:inr";
const CACHE_TTL = 60 * 60 * 24; // 24 hours in seconds

export async function GET() {
  try {
    const redis = getRedisClient();

    // Try to get cached rates from Redis
    try {
      const cached = await redis.get(CACHE_KEY);
      if (cached) {
        console.log("📊 Exchange rates from cache");
        return NextResponse.json(JSON.parse(cached as string));
      }
    } catch (cacheError) {
      console.warn("⚠️ Redis cache read failed, fetching fresh rates:", cacheError);
    }

    // Fetch live rates from exchangerate-api.com (INR as base)
    console.log("🌐 Fetching live exchange rates from API...");
    const response = await fetch("https://api.exchangerate-api.com/v4/latest/INR", {
      next: { revalidate: 86400 }, // Cache in Next.js for 24 hours
    });

    if (!response.ok) {
      throw new Error(`Exchange rate API returned ${response.status}`);
    }

    const data = await response.json();
    
    const rates = {
      USD: data.rates.USD || FALLBACK_RATES.USD,
      EUR: data.rates.EUR || FALLBACK_RATES.EUR,
      GBP: data.rates.GBP || FALLBACK_RATES.GBP,
      source: "live",
      lastUpdated: new Date().toISOString(),
    };

    // Cache in Redis for 24 hours
    try {
      await redis.set(CACHE_KEY, JSON.stringify(rates), { ex: CACHE_TTL });
      console.log("✅ Exchange rates cached in Redis for 24 hours");
    } catch (cacheError) {
      console.warn("⚠️ Redis cache write failed:", cacheError);
    }

    return NextResponse.json(rates);
  } catch (error) {
    console.error("❌ Error fetching exchange rates, using fallback:", error);
    
    // Return fallback rates if API fails
    return NextResponse.json({
      USD: FALLBACK_RATES.USD,
      EUR: FALLBACK_RATES.EUR,
      GBP: FALLBACK_RATES.GBP,
      source: "fallback",
      lastUpdated: new Date().toISOString(),
    });
  }
}
