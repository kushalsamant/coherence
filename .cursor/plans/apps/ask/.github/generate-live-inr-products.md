# Generate Live INR Products for Production

## Overview

This guide explains how to generate live INR products in Stripe without creating duplicate USD products.

## Current Status

**✅ Already Have (Live USD Products):**
- Weekly Pro: `price_1SPMDMJlfVCbQ3BNFAJq4wO6`
- Monthly Pro: `price_1SPMAgJlfVCbQ3BNDs3NM0jf`
- Yearly Pro: `price_1SPMEqJlfVCbQ3BNG6ZhQrKt`
- Starter Pack: `price_1SPMRbJlfVCbQ3BNxVouv2uY`
- Standard Pack: `price_1SPMSJJlfVCbQ3BNcRYLRArc`
- Premium Pack: `price_1SPMSxJlfVCbQ3BNqYcWJrRr`

**❌ Need to Create (Live INR Products):**
- 6 INR products (₹249, ₹799, ₹7,999 + credit packs)

## Steps to Generate Live INR Products

### Step 1: Switch to Live Stripe Key

**Temporarily update your `.env.local`:**

```env
# Comment out test key
#STRIPE_SECRET_KEY=sk_test_GKqkmph47WtZ0XVtYKCfqm6C

# Use live key temporarily
STRIPE_SECRET_KEY=sk_live_ywsRrAeVNphfisdV6gICF5Mj00elbZIAEI
STRIPE_WEBHOOK_SECRET=whsec_4xosdmXPv4pcCKqnen4O2EjXtBx7jwb5
```

### Step 2: Run Setup Script with --inr-only Flag

```bash
npm run setup -- --inr-only
```

**What this does:**
1. Detects existing USD products in Stripe live mode
2. Fetches their price IDs
3. Creates ONLY the 6 INR products (no duplicates)
4. Updates `config/stripe.production.json` with existing USD + new INR price IDs

### Step 3: What to Expect

**Success scenario (if cross-border is enabled):**
```
✅ Found existing USD products. Fetching price IDs...
✅ USD Price IDs retrieved:
   Weekly: price_1SPMDMJlfVCbQ3BNFAJq4wO6
   ...
📦 Creating INR products only...
✅ Weekly Pro (INR) created
   Product ID: prod_XXX
   Price ID: price_XXX
...
✅ Updated config/stripe.production.json
```

**Failure scenario (cross-border not enabled):**
```
✅ Found existing USD products...
📦 Creating INR products only...
❌ Error: As per Indian regulations, only registered Indian businesses...
```

### Step 4: If Cross-Border Error Occurs

**This is expected!** Your Stripe account needs verification.

**Do this:**
1. Visit: https://dashboard.stripe.com/settings/update
2. Complete business registration details
3. Submit for verification
4. Wait for Stripe approval (usually 1-3 business days)
5. Once approved, re-run: `npm run setup -- --inr-only`

### Step 5: Revert to Test Key

After creating INR products (or attempting to), switch back:

```env
# Switch back to test key
STRIPE_SECRET_KEY=sk_test_GKqkmph47WtZ0XVtYKCfqm6C
STRIPE_WEBHOOK_SECRET=whsec_ctkLIitYUIFOQhRL2k6cZD8bfd8VhYXm
```

## Important Notes

### INR Products Work Without Cross-Border

**You can accept INR payments from Indian customers RIGHT NOW:**
- ✅ INR from Indian users → Works
- ✅ INR from international users → Works
- ❌ USD from Indian users → Needs cross-border (but you're routing Indians to INR anyway!)

**The cross-border restriction only affects:**
- USD payments from customers in India
- Since your app routes Indian users to INR prices, this doesn't matter for your use case

### What Gets Created

**INR Products (Live Mode):**
```
1. Reframe AI - Weekly Pro (INR) - ₹249/week
2. Reframe AI - Monthly Pro (INR) - ₹799/month
3. Reframe AI - Yearly Pro (INR) - ₹7,999/year
4. Reframe AI - Starter Pack (INR) - ₹299
5. Reframe AI - Standard Pack (INR) - ₹799
6. Reframe AI - Premium Pack (INR) - ₹1,999
```

**All products include:**
- Proper capitalization
- Complete metadata (currency, region, plan_type, etc.)
- Tax behavior: inclusive (Indian GST compliance)
- Statement descriptors for credit card statements

## Verification

After creating products, verify in Stripe Dashboard:

1. Visit: https://dashboard.stripe.com/products
2. Should see 12 total products:
   - 6 USD products (existing)
   - 6 INR products (newly created)
3. Check each INR product has proper metadata

## Troubleshooting

**Error: "Not all USD products found"**
- Means your live Stripe account doesn't have the expected USD products
- Solution: Run `npm run setup -- --force` to create all products (will create duplicates)

**Error: "Cross-border transactions not enabled"**
- Expected for Indian Stripe accounts
- Solution: Enable cross-border at https://dashboard.stripe.com/settings/update
- Or: Launch with INR-only for Indian customers (works now!)

## Alternative: India-Only Launch

If you don't want to wait for cross-border approval:

1. Don't create USD products
2. Serve only Indian customers with INR pricing
3. Launch immediately!
4. Add USD later when cross-border is approved

This is valid and compliant!

