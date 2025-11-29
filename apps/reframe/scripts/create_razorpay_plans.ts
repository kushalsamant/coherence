#!/usr/bin/env tsx

/**
 * Script to create Razorpay Plans for Reframe subscription payments
 * Run this once to create Plans in your Razorpay account
 * 
 * Usage:
 *   npx tsx scripts/create_razorpay_plans.ts
 * 
 * Or add to package.json:
 *   "scripts": {
 *     "create-razorpay-plans": "tsx scripts/create_razorpay_plans.ts"
 *   }
 */

import Razorpay from "razorpay";
import dotenv from "dotenv";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load app-specific .env.production
const appEnvPath = path.resolve(__dirname, "../../reframe.env.production");
if (fs.existsSync(appEnvPath)) {
  dotenv.config({ path: appEnvPath, override: false });
  console.log("Loaded environment from: reframe.env.production");
}

const RAZORPAY_KEY_ID = process.env.REFRAME_RAZORPAY_KEY_ID;
const RAZORPAY_KEY_SECRET = process.env.REFRAME_RAZORPAY_KEY_SECRET;

if (!RAZORPAY_KEY_ID || !RAZORPAY_KEY_SECRET) {
  console.error("Error: REFRAME_RAZORPAY_KEY_ID and REFRAME_RAZORPAY_KEY_SECRET must be set");
  console.error("They should be in: reframe.env.production");
  process.exit(1);
}

// Initialize Razorpay client
const razorpay = new Razorpay({
  key_id: RAZORPAY_KEY_ID,
  key_secret: RAZORPAY_KEY_SECRET,
});

// Plan definitions for Reframe
// Unified pricing shared across all apps (ASK, Reframe, Sketch2BIM)
// Week: ₹1,299 = 129900 paise
// Monthly: ₹3,499 = 349900 paise
// Yearly: ₹29,999 = 2999900 paise
const PLANS = [
  {
    period: "weekly" as const,
    interval: 1,
    item: {
      name: "Week Pro - Reframe",
      description: "7-day unlimited access to Reframe AI",
      amount: 129900, // ₹1,299 in paise
      currency: "INR",
    },
    notes: {
      tier: "week",
      app: "reframe",
    },
  },
  {
    period: "monthly" as const,
    interval: 1,
    item: {
      name: "Monthly Pro - Reframe",
      description: "30-day unlimited access to Reframe AI",
      amount: 349900, // ₹3,499 in paise
      currency: "INR",
    },
    notes: {
      tier: "monthly",
      app: "reframe",
    },
  },
  {
    period: "yearly" as const,
    interval: 1,
    item: {
      name: "Yearly Pro - Reframe",
      description: "365-day unlimited access to Reframe AI",
      amount: 2999900, // ₹29,999 in paise
      currency: "INR",
    },
    notes: {
      tier: "yearly",
      app: "reframe",
    },
  },
];

interface PlanData {
  period: "weekly" | "monthly" | "yearly";
  interval: number;
  item: {
    name: string;
    description: string;
    amount: number;
    currency: string;
  };
  notes: {
    tier: string;
    app: string;
  };
}

async function createPlan(planData: PlanData): Promise<any | null> {
  try {
    console.log(`\nCreating plan: ${planData.item.name}`);
    console.log(`  Period: ${planData.period}, Interval: ${planData.interval}`);
    console.log(`  Amount: ₹${planData.item.amount / 100}`);

    const plan = await razorpay.plans.create({
      period: planData.period,
      interval: planData.interval,
      item: planData.item,
      notes: planData.notes,
    });

    console.log(`✅ Created Plan: ${plan.id} - ${plan.item.name}`);
    return plan;
  } catch (error: any) {
    console.error(`❌ Failed to create plan ${planData.item.name}:`);
    if (error.statusCode) {
      console.error(`   Status: ${error.statusCode}`);
    }
    if (error.error) {
      console.error(`   Error: ${JSON.stringify(error.error, null, 2)}`);
    } else {
      console.error(`   Error: ${error.message || String(error)}`);
    }
    return null;
  }
}

async function checkExistingPlans(): Promise<Record<string, string>> {
  try {
    const plans = await razorpay.plans.all();
    const existing: Record<string, string> = {};

    if (plans.items) {
      for (const plan of plans.items) {
        const itemName = plan.item?.name || "";
        if (itemName.includes("Week Pro - Reframe")) {
          existing.week = plan.id;
        } else if (itemName.includes("Monthly Pro - Reframe")) {
          existing.monthly = plan.id;
        } else if (itemName.includes("Yearly Pro - Reframe")) {
          existing.yearly = plan.id;
        }
      }
    }

    return existing;
  } catch (error: any) {
    console.error(`⚠️  Could not check existing plans: ${error.message || String(error)}`);
    return {};
  }
}

async function main() {
  console.log("Creating Razorpay Plans for Reframe subscriptions...");
  console.log("=".repeat(60));
  console.log(`Using Key ID: ${RAZORPAY_KEY_ID.substring(0, 10)}...`);
  console.log(`Mode: ${RAZORPAY_KEY_ID.includes("test") ? "TEST" : "LIVE"}`);
  console.log("=".repeat(60));

  // Check for existing plans
  console.log("\nChecking for existing plans...");
  const existingPlans = await checkExistingPlans();
  if (Object.keys(existingPlans).length > 0) {
    console.log(`Found ${Object.keys(existingPlans).length} existing plan(s):`);
    for (const [tier, planId] of Object.entries(existingPlans)) {
      console.log(`  ${tier}: ${planId}`);
    }
    console.log("\nSkipping creation of existing plans.");
  }

  const createdPlans: Record<string, string> = { ...existingPlans };

  // Create missing plans
  for (const planData of PLANS) {
    const tierKey = planData.notes.tier;
    if (existingPlans[tierKey]) {
      console.log(`\n⏭️  Skipping ${tierKey} - plan already exists: ${existingPlans[tierKey]}`);
      continue;
    }

    const plan = await createPlan(planData);
    if (plan) {
      createdPlans[tierKey] = plan.id;
    }
  }

  console.log("\n" + "=".repeat(60));
  console.log("Plan IDs (for environment variables):");
  console.log("=".repeat(60));

  if (Object.keys(createdPlans).length === 0) {
    console.error("❌ No plans created or found. Please check the errors above.");
    console.log("\nTroubleshooting:");
    console.log("1. Verify your API keys are correct in reframe.env.production");
    console.log("2. Check if your Razorpay account has subscription features enabled");
    console.log("3. Try creating plans manually in Razorpay Dashboard");
    process.exit(1);
  }

  for (const tier of ["week", "monthly", "yearly"]) {
    if (createdPlans[tier]) {
      const envVarName = tier === "week" ? "REFRAME_RAZORPAY_PLAN_WEEK" :
                        tier === "monthly" ? "REFRAME_RAZORPAY_PLAN_MONTH" : 
                        "REFRAME_RAZORPAY_PLAN_YEAR";
      console.log(`${envVarName}=${createdPlans[tier]}`);
    } else {
      const envVarName = tier === "week" ? "REFRAME_RAZORPAY_PLAN_WEEK" :
                        tier === "monthly" ? "REFRAME_RAZORPAY_PLAN_MONTH" : 
                        "REFRAME_RAZORPAY_PLAN_YEAR";
      console.log(`${envVarName}=  # MISSING - create manually`);
    }
  }

  console.log("\n" + "=".repeat(60));
  console.log("Copy these to your reframe.env.production:");
  console.log("=".repeat(60));
  for (const tier of ["week", "monthly", "yearly"]) {
    if (createdPlans[tier]) {
      const envVarName = tier === "week" ? "REFRAME_RAZORPAY_PLAN_WEEK" :
                        tier === "monthly" ? "REFRAME_RAZORPAY_PLAN_MONTH" : 
                        "REFRAME_RAZORPAY_PLAN_YEAR";
      console.log(`${envVarName}=${createdPlans[tier]}`);
    }
  }

  if (Object.keys(createdPlans).length === 3) {
    console.log("\n✅ All plans created successfully!");
  } else {
    console.log(`\n⚠️  Only ${Object.keys(createdPlans).length}/3 plans created. Please create the missing ones manually.`);
  }
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});

