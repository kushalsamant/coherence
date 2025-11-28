#!/usr/bin/env node

import Stripe from 'stripe';
import { createInterface } from 'readline';
import { writeFileSync, readFileSync, existsSync } from 'fs';
import { join, resolve } from 'path';
import { config as loadEnv } from 'dotenv';

function loadAppEnvFile() {
  const appEnvPath = resolve(process.cwd(), '../ask.env.production');
  if (existsSync(appEnvPath)) {
    loadEnv({ path: appEnvPath, override: false });
    console.log('✅ Loaded ask.env.production file\n');
  }
}

// Load .env.local file
function loadEnvFile() {
  const envPath = join(process.cwd(), '.env.local');
  if (existsSync(envPath)) {
    const envContent = readFileSync(envPath, 'utf-8');
    envContent.split('\n').forEach((line) => {
      const trimmedLine = line.trim();
      if (trimmedLine && !trimmedLine.startsWith('#')) {
        const match = trimmedLine.match(/^([^=]+)=(.*)$/);
        if (match) {
          const key = match[1].trim();
          let value = match[2].trim();
          // Remove quotes if present
          value = value.replace(/^["']|["']$/g, '');
          process.env[key] = value;
        }
      }
    });
    console.log('✅ Loaded .env.local file\n');
  }
}

const rl = createInterface({
  input: process.stdin,
  output: process.stdout,
});

const question = (query: string): Promise<string> =>
  new Promise((resolve) => rl.question(query, resolve));

async function main() {
  console.log('\n🚀 Reframe Setup Script\n');
  console.log('This script will help you configure your application.\n');

  // Load environment variables from .env.local
  loadAppEnvFile();
  loadEnvFile();

  // Check for flags
  const forceCreate = process.argv.includes('--force');
  const inrOnly = process.argv.includes('--inr-only');

  // Check for Stripe API key
  const stripeKey = process.env.STRIPE_SECRET_KEY;
  if (!stripeKey) {
    console.error('❌ STRIPE_SECRET_KEY not found in environment variables.');
    console.log('   Please add it to your .env.local file and try again.\n');
    process.exit(1);
  }

  const stripe = new Stripe(stripeKey, { apiVersion: '2025-10-29.clover' });

  console.log('✅ Stripe API key found\n');
  console.log('📦 Creating Stripe products and prices...\n');

  try {
    // Check if products already exist
    const existingProducts = await stripe.products.list({ limit: 100 });
    const reframeProducts = existingProducts.data.filter((p) =>
      p.name.includes('Reframe') || p.name.includes('Humanizer')
    );

    if (reframeProducts.length > 0 && !forceCreate) {
      console.log('⚠️  Found existing Reframe products:');
      reframeProducts.forEach((p) => {
        console.log(`   - ${p.name} (${p.id})`);
      });
      const answer = await question(
        '\nDo you want to create new products anyway? (y/N): '
      );
      if (answer.toLowerCase() !== 'y') {
        console.log('\n✅ Using existing products. Fetching price IDs...\n');
        
        // Fetch prices for existing products
        for (const product of reframeProducts) {
          const prices = await stripe.prices.list({ product: product.id });
          if (prices.data.length > 0) {
            console.log(`\n${product.name}:`);
            prices.data.forEach((price) => {
              const interval = price.recurring?.interval || 'one-time';
              const amount = (price.unit_amount || 0) / 100;
              console.log(`   Price ID: ${price.id}`);
              console.log(`   Amount: $${amount}/${interval}`);
            });
          }
        }
        rl.close();
        return;
      }
    }
    
    if (forceCreate) {
      console.log('🔥 --force flag detected, creating new products...\n');
    }

    // Handle --inr-only flag: Create only INR products, use existing USD products
    if (inrOnly) {
      console.log('💱 --inr-only flag detected, will use existing USD products and create INR only...\n');
      
      // Find existing USD products
      const weeklyUSD = reframeProducts.find(p => p.name === 'Reframe - Weekly Pro');
      const monthlyUSD = reframeProducts.find(p => p.name === 'Reframe - Monthly Pro');
      const yearlyUSD = reframeProducts.find(p => p.name === 'Reframe - Yearly Pro');
      const starterUSD = reframeProducts.find(p => p.name === 'Reframe - Starter Pack');
      const standardUSD = reframeProducts.find(p => p.name === 'Reframe - Standard Pack');
      const premiumUSD = reframeProducts.find(p => p.name === 'Reframe - Premium Pack');
      
      if (!weeklyUSD || !monthlyUSD || !yearlyUSD || !starterUSD || !standardUSD || !premiumUSD) {
        console.error('❌ Not all USD products found. Missing:');
        if (!weeklyUSD) console.error('   - Weekly Pro');
        if (!monthlyUSD) console.error('   - Monthly Pro');
        if (!yearlyUSD) console.error('   - Yearly Pro');
        if (!starterUSD) console.error('   - Starter Pack');
        if (!standardUSD) console.error('   - Standard Pack');
        if (!premiumUSD) console.error('   - Premium Pack');
        console.log('\nRun without --inr-only flag to create all products.\n');
        rl.close();
        return;
      }
      
      // Fetch USD price IDs
      console.log('✅ Found existing USD products. Fetching price IDs...\n');
      const weeklyPricesUSD = await stripe.prices.list({ product: weeklyUSD.id });
      const monthlyPricesUSD = await stripe.prices.list({ product: monthlyUSD.id });
      const yearlyPricesUSD = await stripe.prices.list({ product: yearlyUSD.id });
      const starterPricesUSD = await stripe.prices.list({ product: starterUSD.id });
      const standardPricesUSD = await stripe.prices.list({ product: standardUSD.id });
      const premiumPricesUSD = await stripe.prices.list({ product: premiumUSD.id });
      
      const weeklyPrice = weeklyPricesUSD.data[0];
      const monthlyPrice = monthlyPricesUSD.data[0];
      const yearlyPrice = yearlyPricesUSD.data[0];
      const starterPackPrice = starterPricesUSD.data[0];
      const standardPackPrice = standardPricesUSD.data[0];
      const premiumPackPrice = premiumPricesUSD.data[0];
      
      console.log('✅ USD Price IDs retrieved:');
      console.log(`   Weekly: ${weeklyPrice.id}`);
      console.log(`   Monthly: ${monthlyPrice.id}`);
      console.log(`   Yearly: ${yearlyPrice.id}`);
      console.log(`   Starter Pack: ${starterPackPrice.id}`);
      console.log(`   Standard Pack: ${standardPackPrice.id}`);
      console.log(`   Premium Pack: ${premiumPackPrice.id}\n`);
      
      console.log('📦 Creating INR products only...\n');
      
      // Skip to INR product creation (jump ahead in the script)
      // We'll create INR products here and skip USD creation
      
      // Weekly Pro (INR)
      const weeklyProductINR = await stripe.products.create({
        name: 'Reframe - Weekly Pro (INR)',
        description: '50 Requests Per Week with All Character Limits and Premium Tones Unlocked',
        active: true,
        statement_descriptor: 'REFRAME WEEKLY',
        tax_code: 'txcd_10000000',
        metadata: {
          currency: 'INR',
          region: 'India',
          plan_type: 'subscription',
          interval: 'week'
        }
      });

      const weeklyPriceINR = await stripe.prices.create({
        product: weeklyProductINR.id,
        unit_amount: 24900, // ₹249
        currency: 'inr',
        recurring: { interval: 'week', interval_count: 1, usage_type: 'licensed' },
        nickname: 'Weekly Pro (INR)',
        tax_behavior: 'inclusive',
        billing_scheme: 'per_unit',
        metadata: { currency: 'INR', region: 'India', plan: 'weekly' }
      });

      console.log('✅ Weekly Pro (INR) created');
      console.log(`   Product ID: ${weeklyProductINR.id}`);
      console.log(`   Price ID: ${weeklyPriceINR.id}\n`);

      // Monthly Pro (INR)
      const monthlyProductINR = await stripe.products.create({
        name: 'Reframe - Monthly Pro (INR)',
        description: 'Unlimited Requests with All Character Limits and Premium Tones Unlocked',
        active: true,
        statement_descriptor: 'REFRAME MONTHLY',
        tax_code: 'txcd_10000000',
        metadata: {
          currency: 'INR',
          region: 'India',
          plan_type: 'subscription',
          interval: 'month'
        }
      });

      const monthlyPriceINR = await stripe.prices.create({
        product: monthlyProductINR.id,
        unit_amount: 79900, // ₹799
        currency: 'inr',
        recurring: { interval: 'month', interval_count: 1, usage_type: 'licensed' },
        nickname: 'Monthly Pro (INR)',
        tax_behavior: 'inclusive',
        billing_scheme: 'per_unit',
        metadata: { currency: 'INR', region: 'India', plan: 'monthly' }
      });

      console.log('✅ Monthly Pro (INR) created');
      console.log(`   Product ID: ${monthlyProductINR.id}`);
      console.log(`   Price ID: ${monthlyPriceINR.id}\n`);

      // Yearly Pro (INR)
      const yearlyProductINR = await stripe.products.create({
        name: 'Reframe - Yearly Pro (INR)',
        description: 'Unlimited Requests with All Character Limits and Premium Tones Unlocked - Save 17%',
        active: true,
        statement_descriptor: 'REFRAME YEARLY',
        tax_code: 'txcd_10000000',
        metadata: {
          currency: 'INR',
          region: 'India',
          plan_type: 'subscription',
          interval: 'year',
          discount: '17%'
        }
      });

      const yearlyPriceINR = await stripe.prices.create({
        product: yearlyProductINR.id,
        unit_amount: 799900, // ₹7,999
        currency: 'inr',
        recurring: { interval: 'year', interval_count: 1, usage_type: 'licensed' },
        nickname: 'Yearly Pro (INR)',
        tax_behavior: 'inclusive',
        billing_scheme: 'per_unit',
        metadata: { currency: 'INR', region: 'India', plan: 'yearly' }
      });

      console.log('✅ Yearly Pro (INR) created');
      console.log(`   Product ID: ${yearlyProductINR.id}`);
      console.log(`   Price ID: ${yearlyPriceINR.id}\n`);

      // Starter Pack (INR)
      const starterPackProductINR = await stripe.products.create({
        name: 'Reframe - Starter Pack (INR)',
        description: '10 One-Time Credits - Perfect for 1-2 Documents - All Tones and Character Limits Unlocked',
        active: true,
        statement_descriptor: 'REFRAME CREDITS',
        tax_code: 'txcd_10000000',
        metadata: {
          currency: 'INR',
          region: 'India',
          plan_type: 'credits',
          credits: 10,
          pack: 'starter'
        }
      });

      const starterPackPriceINR = await stripe.prices.create({
        product: starterPackProductINR.id,
        unit_amount: 29900, // ₹299
        currency: 'inr',
        nickname: 'Starter Pack - 10 Credits (INR)',
        tax_behavior: 'inclusive',
        billing_scheme: 'per_unit',
        metadata: { currency: 'INR', region: 'India', credits: 10, pack: 'starter' }
      });

      console.log('✅ Starter Pack (INR) created');
      console.log(`   Product ID: ${starterPackProductINR.id}`);
      console.log(`   Price ID: ${starterPackPriceINR.id}\n`);

      // Standard Pack (INR)
      const standardPackProductINR = await stripe.products.create({
        name: 'Reframe - Standard Pack (INR)',
        description: '30 One-Time Credits - Best for Occasional Use - All Tones and Character Limits Unlocked',
        active: true,
        statement_descriptor: 'REFRAME CREDITS',
        tax_code: 'txcd_10000000',
        metadata: {
          currency: 'INR',
          region: 'India',
          plan_type: 'credits',
          credits: 30,
          pack: 'standard'
        }
      });

      const standardPackPriceINR = await stripe.prices.create({
        product: standardPackProductINR.id,
        unit_amount: 79900, // ₹799
        currency: 'inr',
        nickname: 'Standard Pack - 30 Credits (INR)',
        tax_behavior: 'inclusive',
        billing_scheme: 'per_unit',
        metadata: { currency: 'INR', region: 'India', credits: 30, pack: 'standard' }
      });

      console.log('✅ Standard Pack (INR) created');
      console.log(`   Product ID: ${standardPackProductINR.id}`);
      console.log(`   Price ID: ${standardPackPriceINR.id}\n`);

      // Premium Pack (INR)
      const premiumPackProductINR = await stripe.products.create({
        name: 'Reframe - Premium Pack (INR)',
        description: '100 One-Time Credits - Bulk One-Time Projects - All Tones and Character Limits Unlocked',
        active: true,
        statement_descriptor: 'REFRAME CREDITS',
        tax_code: 'txcd_10000000',
        metadata: {
          currency: 'INR',
          region: 'India',
          plan_type: 'credits',
          credits: 100,
          pack: 'premium'
        }
      });

      const premiumPackPriceINR = await stripe.prices.create({
        product: premiumPackProductINR.id,
        unit_amount: 199900, // ₹1,999
        currency: 'inr',
        nickname: 'Premium Pack - 100 Credits (INR)',
        tax_behavior: 'inclusive',
        billing_scheme: 'per_unit',
        metadata: { currency: 'INR', region: 'India', credits: 100, pack: 'premium' }
      });

      console.log('✅ Premium Pack (INR) created');
      console.log(`   Product ID: ${premiumPackProductINR.id}`);
      console.log(`   Price ID: ${premiumPackPriceINR.id}\n`);
      
      // Update config file with existing USD + new INR
      const isProduction = stripeKey.startsWith('sk_live_');
      const configFileName = isProduction ? 'stripe.production.json' : 'stripe.test.json';
      const configPath = join(process.cwd(), 'config', configFileName);
      const config = JSON.parse(readFileSync(configPath, 'utf-8'));
      
      config.prices.usd = {
        weekly: weeklyPrice.id,
        monthly: monthlyPrice.id,
        yearly: yearlyPrice.id,
        credit_starter: starterPackPrice.id,
        credit_standard: standardPackPrice.id,
        credit_premium: premiumPackPrice.id
      };
      
      config.prices.inr = {
        weekly: weeklyPriceINR.id,
        monthly: monthlyPriceINR.id,
        yearly: yearlyPriceINR.id,
        credit_starter: starterPackPriceINR.id,
        credit_standard: standardPackPriceINR.id,
        credit_premium: premiumPackPriceINR.id
      };
      
      writeFileSync(configPath, JSON.stringify(config, null, 2));
      console.log(`✅ Updated config/${configFileName} with existing USD + new INR price IDs\n`);
      
      console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
      console.log('✅ INR-Only Setup Complete!\n');
      console.log('USD Price IDs (existing):');
      console.log(`   Weekly: ${weeklyPrice.id}`);
      console.log(`   Monthly: ${monthlyPrice.id}`);
      console.log(`   Yearly: ${yearlyPrice.id}`);
      console.log(`   Starter Pack: ${starterPackPrice.id}`);
      console.log(`   Standard Pack: ${standardPackPrice.id}`);
      console.log(`   Premium Pack: ${premiumPackPrice.id}\n`);
      console.log('INR Price IDs (newly created):');
      console.log(`   Weekly: ${weeklyPriceINR.id}`);
      console.log(`   Monthly: ${monthlyPriceINR.id}`);
      console.log(`   Yearly: ${yearlyPriceINR.id}`);
      console.log(`   Starter Pack: ${starterPackPriceINR.id}`);
      console.log(`   Standard Pack: ${standardPackPriceINR.id}`);
      console.log(`   Premium Pack: ${premiumPackPriceINR.id}\n`);
      console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
      
      rl.close();
      return;
    }

    // Create Weekly Pro
    const weeklyProduct = await stripe.products.create({
      name: 'Reframe - Weekly Pro',
      description: '50 requests per week with all character limits unlocked',
    });

    const weeklyPrice = await stripe.prices.create({
      product: weeklyProduct.id,
      unit_amount: 299, // $2.99
      currency: 'usd',
      recurring: { interval: 'week' },
    });

    console.log('✅ Weekly Pro created');
    console.log(`   Product ID: ${weeklyProduct.id}`);
    console.log(`   Price ID: ${weeklyPrice.id}\n`);

    // Create Monthly Pro
    const monthlyProduct = await stripe.products.create({
      name: 'Reframe - Monthly Pro',
      description: 'Unlimited requests with all character limits unlocked',
    });

    const monthlyPrice = await stripe.prices.create({
      product: monthlyProduct.id,
      unit_amount: 999, // $9.99
      currency: 'usd',
      recurring: { interval: 'month' },
    });

    console.log('✅ Monthly Pro created');
    console.log(`   Product ID: ${monthlyProduct.id}`);
    console.log(`   Price ID: ${monthlyPrice.id}\n`);

    // Create Yearly Pro
    const yearlyProduct = await stripe.products.create({
      name: 'Reframe - Yearly Pro',
      description:
        'Unlimited requests with all character limits unlocked (Save 17%!)',
    });

    const yearlyPrice = await stripe.prices.create({
      product: yearlyProduct.id,
      unit_amount: 9900, // $99
      currency: 'usd',
      recurring: { interval: 'year' },
    });

    console.log('✅ Yearly Pro created');
    console.log(`   Product ID: ${yearlyProduct.id}`);
    console.log(`   Price ID: ${yearlyPrice.id}\n`);

    // Create Credit Packs
    console.log('📦 Creating credit packs...\n');

    // Starter Pack - $3.99 for 10 credits
    const starterPackProduct = await stripe.products.create({
      name: 'Reframe - Starter Pack',
      description: '10 one-time credits - Perfect for 1-2 documents',
    });

    const starterPackPrice = await stripe.prices.create({
      product: starterPackProduct.id,
      unit_amount: 399, // $3.99
      currency: 'usd',
    });

    console.log('✅ Starter Pack created');
    console.log(`   Product ID: ${starterPackProduct.id}`);
    console.log(`   Price ID: ${starterPackPrice.id}\n`);

    // Standard Pack - $9.99 for 30 credits
    const standardPackProduct = await stripe.products.create({
      name: 'Reframe - Standard Pack',
      description: '30 one-time credits - Best for occasional use',
    });

    const standardPackPrice = await stripe.prices.create({
      product: standardPackProduct.id,
      unit_amount: 999, // $9.99
      currency: 'usd',
    });

    console.log('✅ Standard Pack created');
    console.log(`   Product ID: ${standardPackProduct.id}`);
    console.log(`   Price ID: ${standardPackPrice.id}\n`);

    // Premium Pack - $24.99 for 100 credits
    const premiumPackProduct = await stripe.products.create({
      name: 'Reframe - Premium Pack',
      description: '100 one-time credits - Bulk one-time projects',
    });

    const premiumPackPrice = await stripe.prices.create({
      product: premiumPackProduct.id,
      unit_amount: 2499, // $24.99
      currency: 'usd',
    });

    console.log('✅ Premium Pack created');
    console.log(`   Product ID: ${premiumPackProduct.id}`);
    console.log(`   Price ID: ${premiumPackPrice.id}\n`);

    // Create INR Products
    console.log('📦 Creating INR products for Indian customers...\n');

    // Weekly Pro (INR)
    const weeklyProductINR = await stripe.products.create({
      name: 'Reframe - Weekly Pro (INR)',
      description: '50 Requests Per Week with All Character Limits and Premium Tones Unlocked',
      active: true,
      statement_descriptor: 'REFRAME WEEKLY',
      tax_code: 'txcd_10000000',
      metadata: {
        currency: 'INR',
        region: 'India',
        plan_type: 'subscription',
        interval: 'week'
      }
    });

    const weeklyPriceINR = await stripe.prices.create({
      product: weeklyProductINR.id,
      unit_amount: 24900, // ₹249
      currency: 'inr',
      recurring: { interval: 'week', interval_count: 1, usage_type: 'licensed' },
      nickname: 'Weekly Pro (INR)',
      tax_behavior: 'inclusive',
      billing_scheme: 'per_unit',
      metadata: { currency: 'INR', region: 'India', plan: 'weekly' }
    });

    console.log('✅ Weekly Pro (INR) created');
    console.log(`   Product ID: ${weeklyProductINR.id}`);
    console.log(`   Price ID: ${weeklyPriceINR.id}\n`);

    // Monthly Pro (INR)
    const monthlyProductINR = await stripe.products.create({
      name: 'Reframe - Monthly Pro (INR)',
      description: 'Unlimited Requests with All Character Limits and Premium Tones Unlocked',
      active: true,
      statement_descriptor: 'REFRAME MONTHLY',
      tax_code: 'txcd_10000000',
      metadata: {
        currency: 'INR',
        region: 'India',
        plan_type: 'subscription',
        interval: 'month'
      }
    });

    const monthlyPriceINR = await stripe.prices.create({
      product: monthlyProductINR.id,
      unit_amount: 79900, // ₹799
      currency: 'inr',
      recurring: { interval: 'month', interval_count: 1, usage_type: 'licensed' },
      nickname: 'Monthly Pro (INR)',
      tax_behavior: 'inclusive',
      billing_scheme: 'per_unit',
      metadata: { currency: 'INR', region: 'India', plan: 'monthly' }
    });

    console.log('✅ Monthly Pro (INR) created');
    console.log(`   Product ID: ${monthlyProductINR.id}`);
    console.log(`   Price ID: ${monthlyPriceINR.id}\n`);

    // Yearly Pro (INR)
    const yearlyProductINR = await stripe.products.create({
      name: 'Reframe - Yearly Pro (INR)',
      description: 'Unlimited Requests with All Character Limits and Premium Tones Unlocked - Save 17%',
      active: true,
      statement_descriptor: 'REFRAME YEARLY',
      tax_code: 'txcd_10000000',
      metadata: {
        currency: 'INR',
        region: 'India',
        plan_type: 'subscription',
        interval: 'year',
        discount: '17%'
      }
    });

    const yearlyPriceINR = await stripe.prices.create({
      product: yearlyProductINR.id,
      unit_amount: 799900, // ₹7,999
      currency: 'inr',
      recurring: { interval: 'year', interval_count: 1, usage_type: 'licensed' },
      nickname: 'Yearly Pro (INR)',
      tax_behavior: 'inclusive',
      billing_scheme: 'per_unit',
      metadata: { currency: 'INR', region: 'India', plan: 'yearly' }
    });

    console.log('✅ Yearly Pro (INR) created');
    console.log(`   Product ID: ${yearlyProductINR.id}`);
    console.log(`   Price ID: ${yearlyPriceINR.id}\n`);

    // Starter Pack (INR)
    const starterPackProductINR = await stripe.products.create({
      name: 'Reframe - Starter Pack (INR)',
      description: '10 One-Time Credits - Perfect for 1-2 Documents - All Tones and Character Limits Unlocked',
      active: true,
      statement_descriptor: 'REFRAME CREDITS',
      tax_code: 'txcd_10000000',
      metadata: {
        currency: 'INR',
        region: 'India',
        plan_type: 'credits',
        credits: 10,
        pack: 'starter'
      }
    });

    const starterPackPriceINR = await stripe.prices.create({
      product: starterPackProductINR.id,
      unit_amount: 29900, // ₹299
      currency: 'inr',
      nickname: 'Starter Pack - 10 Credits (INR)',
      tax_behavior: 'inclusive',
      billing_scheme: 'per_unit',
      metadata: { currency: 'INR', region: 'India', credits: 10, pack: 'starter' }
    });

    console.log('✅ Starter Pack (INR) created');
    console.log(`   Product ID: ${starterPackProductINR.id}`);
    console.log(`   Price ID: ${starterPackPriceINR.id}\n`);

    // Standard Pack (INR)
    const standardPackProductINR = await stripe.products.create({
      name: 'Reframe - Standard Pack (INR)',
      description: '30 One-Time Credits - Best for Occasional Use - All Tones and Character Limits Unlocked',
      active: true,
      statement_descriptor: 'REFRAME CREDITS',
      tax_code: 'txcd_10000000',
      metadata: {
        currency: 'INR',
        region: 'India',
        plan_type: 'credits',
        credits: 30,
        pack: 'standard'
      }
    });

    const standardPackPriceINR = await stripe.prices.create({
      product: standardPackProductINR.id,
      unit_amount: 79900, // ₹799
      currency: 'inr',
      nickname: 'Standard Pack - 30 Credits (INR)',
      tax_behavior: 'inclusive',
      billing_scheme: 'per_unit',
      metadata: { currency: 'INR', region: 'India', credits: 30, pack: 'standard' }
    });

    console.log('✅ Standard Pack (INR) created');
    console.log(`   Product ID: ${standardPackProductINR.id}`);
    console.log(`   Price ID: ${standardPackPriceINR.id}\n`);

    // Premium Pack (INR)
    const premiumPackProductINR = await stripe.products.create({
      name: 'Reframe - Premium Pack (INR)',
      description: '100 One-Time Credits - Bulk One-Time Projects - All Tones and Character Limits Unlocked',
      active: true,
      statement_descriptor: 'REFRAME CREDITS',
      tax_code: 'txcd_10000000',
      metadata: {
        currency: 'INR',
        region: 'India',
        plan_type: 'credits',
        credits: 100,
        pack: 'premium'
      }
    });

    const premiumPackPriceINR = await stripe.prices.create({
      product: premiumPackProductINR.id,
      unit_amount: 199900, // ₹1,999
      currency: 'inr',
      nickname: 'Premium Pack - 100 Credits (INR)',
      tax_behavior: 'inclusive',
      billing_scheme: 'per_unit',
      metadata: { currency: 'INR', region: 'India', credits: 100, pack: 'premium' }
    });

    console.log('✅ Premium Pack (INR) created');
    console.log(`   Product ID: ${premiumPackProductINR.id}`);
    console.log(`   Price ID: ${premiumPackPriceINR.id}\n`);

    // Update appropriate config file based on Stripe key mode
    const isProduction = stripeKey.startsWith('sk_live_');
    const configFileName = isProduction ? 'stripe.production.json' : 'stripe.test.json';
    const configPath = join(process.cwd(), 'config', configFileName);
    const config = JSON.parse(readFileSync(configPath, 'utf-8'));
    
    config.prices.usd = {
      weekly: weeklyPrice.id,
      monthly: monthlyPrice.id,
      yearly: yearlyPrice.id,
      credit_starter: starterPackPrice.id,
      credit_standard: standardPackPrice.id,
      credit_premium: premiumPackPrice.id
    };
    
    config.prices.inr = {
      weekly: weeklyPriceINR.id,
      monthly: monthlyPriceINR.id,
      yearly: yearlyPriceINR.id,
      credit_starter: starterPackPriceINR.id,
      credit_standard: standardPackPriceINR.id,
      credit_premium: premiumPackPriceINR.id
    };
    
    writeFileSync(configPath, JSON.stringify(config, null, 2));
    console.log(`✅ Updated config/${configFileName} with all price IDs\n`);

    // Output environment variables
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    console.log('📋 config/stripe.json has been updated with all price IDs\n');
    console.log('✅ USD Price IDs:');
    console.log(`   Weekly: ${weeklyPrice.id}`);
    console.log(`   Monthly: ${monthlyPrice.id}`);
    console.log(`   Yearly: ${yearlyPrice.id}`);
    console.log(`   Starter Pack: ${starterPackPrice.id}`);
    console.log(`   Standard Pack: ${standardPackPrice.id}`);
    console.log(`   Premium Pack: ${premiumPackPrice.id}\n`);
    console.log('✅ INR Price IDs:');
    console.log(`   Weekly: ${weeklyPriceINR.id}`);
    console.log(`   Monthly: ${monthlyPriceINR.id}`);
    console.log(`   Yearly: ${yearlyPriceINR.id}`);
    console.log(`   Starter Pack: ${starterPackPriceINR.id}`);
    console.log(`   Standard Pack: ${standardPackPriceINR.id}`);
    console.log(`   Premium Pack: ${premiumPackPriceINR.id}\n`);
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

    // Export to JSON file
    const configData = {
      generated_at: new Date().toISOString(),
      stripe_mode: stripeKey.startsWith('sk_test_') ? 'test' : 'live',
      subscriptions: {
        weekly: {
          product_id: weeklyProduct.id,
          price_id: weeklyPrice.id,
          amount: '$2.99/week',
        },
        monthly: {
          product_id: monthlyProduct.id,
          price_id: monthlyPrice.id,
          amount: '$9.99/month',
        },
        yearly: {
          product_id: yearlyProduct.id,
          price_id: yearlyPrice.id,
          amount: '$99/year',
        },
      },
      credit_packs: {
        starter: {
          product_id: starterPackProduct.id,
          price_id: starterPackPrice.id,
          amount: '$3.99',
          credits: 10,
        },
        standard: {
          product_id: standardPackProduct.id,
          price_id: standardPackPrice.id,
          amount: '$9.99',
          credits: 30,
        },
        premium: {
          product_id: premiumPackProduct.id,
          price_id: premiumPackPrice.id,
          amount: '$24.99',
          credits: 100,
        },
      },
      env_variables: {
        STRIPE_WEEKLY_PRICE_ID: weeklyPrice.id,
        STRIPE_MONTHLY_PRICE_ID: monthlyPrice.id,
        STRIPE_YEARLY_PRICE_ID: yearlyPrice.id,
        STRIPE_CREDIT_PACK_STARTER_PRICE_ID: starterPackPrice.id,
        STRIPE_CREDIT_PACK_STANDARD_PRICE_ID: standardPackPrice.id,
        STRIPE_CREDIT_PACK_PREMIUM_PRICE_ID: premiumPackPrice.id,
      },
    };

    const jsonPath = join(process.cwd(), 'stripe-test-config.json');
    writeFileSync(jsonPath, JSON.stringify(configData, null, 2));
    console.log(`✅ Configuration saved to stripe-test-config.json\n`);

    // Export to Markdown file
    const markdownContent = `# Stripe Test Configuration

Generated: ${new Date().toLocaleString()}
Mode: **${stripeKey.startsWith('sk_test_') ? 'TEST' : 'LIVE'}**

## Subscription Products

### Weekly Pro - $2.99/week
- Product ID: \`${weeklyProduct.id}\`
- Price ID: \`${weeklyPrice.id}\`
- Description: 50 requests per week with all character limits unlocked

### Monthly Pro - $9.99/month
- Product ID: \`${monthlyProduct.id}\`
- Price ID: \`${monthlyPrice.id}\`
- Description: Unlimited requests with all character limits unlocked

### Yearly Pro - $99/year
- Product ID: \`${yearlyProduct.id}\`
- Price ID: \`${yearlyPrice.id}\`
- Description: Unlimited requests with all character limits unlocked (Save 17%!)

## Credit Pack Products

### Starter Pack - $3.99 (10 credits)
- Product ID: \`${starterPackProduct.id}\`
- Price ID: \`${starterPackPrice.id}\`
- Description: Perfect for 1-2 documents

### Standard Pack - $9.99 (30 credits)
- Product ID: \`${standardPackProduct.id}\`
- Price ID: \`${standardPackPrice.id}\`
- Description: Best for occasional use

### Premium Pack - $24.99 (100 credits)
- Product ID: \`${premiumPackProduct.id}\`
- Price ID: \`${premiumPackPrice.id}\`
- Description: Bulk one-time projects

## Environment Variables

Copy these to your \`.env.local\` file:

\`\`\`env
# Subscriptions
STRIPE_WEEKLY_PRICE_ID=${weeklyPrice.id}
STRIPE_MONTHLY_PRICE_ID=${monthlyPrice.id}
STRIPE_YEARLY_PRICE_ID=${yearlyPrice.id}

# Credit Packs
STRIPE_CREDIT_PACK_STARTER_PRICE_ID=${starterPackPrice.id}
STRIPE_CREDIT_PACK_STANDARD_PRICE_ID=${standardPackPrice.id}
STRIPE_CREDIT_PACK_PREMIUM_PRICE_ID=${premiumPackPrice.id}
\`\`\`

## Testing

Use these test cards in Stripe test mode:
- **Success**: \`4242 4242 4242 4242\`
- **Decline**: \`4000 0000 0000 0002\`
- **Expired Date**: Any future date
- **CVV**: Any 3 digits

## Dashboard Links

- View Products: https://dashboard.stripe.com/${stripeKey.startsWith('sk_test_') ? 'test/' : ''}products
- View Prices: https://dashboard.stripe.com/${stripeKey.startsWith('sk_test_') ? 'test/' : ''}prices
`;

    const mdPath = join(process.cwd(), 'stripe-test-config.md');
    writeFileSync(mdPath, markdownContent);
    console.log(`✅ Documentation saved to stripe-test-config.md\n`);

    // Check other environment variables
    console.log('🔍 Checking environment configuration...\n');

    const requiredVars = [
      'AUTH_SECRET',
      'ASK_GOOGLE_SECRET',
      'GROQ_API_KEY',
      'UPSTASH_REDIS_REST_TOKEN',
      'STRIPE_WEBHOOK_SECRET',
    ];

    const missing = requiredVars.filter((v) => !process.env[v]);

    if (missing.length === 0) {
      console.log('✅ All required environment variables are set!\n');
    } else {
      console.log('⚠️  Missing environment variables:\n');
      missing.forEach((v) => console.log(`   - ${v}`));
      console.log('');

      if (missing.includes('UPSTASH_REDIS_REST_URL') || missing.includes('UPSTASH_REDIS_REST_TOKEN')) {
        console.log('📝 Upstash Redis Setup (2 minutes):\n');
        console.log('   1. Go to https://console.upstash.com');
        console.log('   2. Create a new Redis database');
        console.log('   3. Copy REST URL → UPSTASH_REDIS_REST_URL');
        console.log('   4. Copy REST Token → UPSTASH_REDIS_REST_TOKEN\n');
      }
    }

    console.log('✨ Setup complete! Run `npm run dev` to start the application.\n');
  } catch (error: any) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  } finally {
    rl.close();
  }
}

main();

