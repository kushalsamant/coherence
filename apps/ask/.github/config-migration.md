# Configuration Migration Guide

## Overview

We've moved public configuration (Stripe price IDs, publishable keys, app URLs) from environment variables to JSON config files for better organization and version control.

## What Changed

### Before (Environment Variables)
```env
# .env.local
STRIPE_WEEKLY_PRICE_ID=price_xxx
STRIPE_MONTHLY_PRICE_ID=price_xxx
STRIPE_YEARLY_PRICE_ID=price_xxx
STRIPE_CREDIT_PACK_STARTER_PRICE_ID=price_xxx
STRIPE_CREDIT_PACK_STANDARD_PRICE_ID=price_xxx
STRIPE_CREDIT_PACK_PREMIUM_PRICE_ID=price_xxx
STRIPE_KEY_PUBLISHABLE=pk_test_xxx
AUTH_URL=http://localhost:3000
AUTH_GOOGLE_ID=xxx
UPSTASH_REDIS_REST_URL=https://xxx
NEXT_PUBLIC_FREE_LIMIT=0
```

### After (JSON Configs + Env Secrets)
```
config/
  ├── stripe.test.json       # Test mode prices (USD + INR)
  ├── stripe.production.json # Production prices (USD + INR)
  ├── app.test.json          # Public app configuration
  └── app.production.json    # Production app configuration

.env.local                   # Secrets only
```

## Benefits

1. **✅ Better Organization** - Public configs separated from secrets
2. **✅ Version Control** - Config files tracked in git, easy to review changes
3. **✅ Type Safety** - JSON imports are type-safe in TypeScript
4. **✅ Easier Updates** - Change prices without touching .env.local
5. **✅ Team Friendly** - No .env.local merge conflicts
6. **✅ Dual Currency** - Support for both USD and INR pricing

## Migration Steps

### Step 1: Clean Up .env.local

**Remove these lines (now in config files):**
```env
STRIPE_WEEKLY_PRICE_ID=...
STRIPE_MONTHLY_PRICE_ID=...
STRIPE_YEARLY_PRICE_ID=...
STRIPE_CREDIT_PACK_STARTER_PRICE_ID=...
STRIPE_CREDIT_PACK_STANDARD_PRICE_ID=...
STRIPE_CREDIT_PACK_PREMIUM_PRICE_ID=...
STRIPE_KEY_PUBLISHABLE=...
AUTH_GOOGLE_ID=...
UPSTASH_REDIS_REST_URL=...
NEXT_PUBLIC_FREE_LIMIT=...
```

**Keep only secrets:**
```env
# .env.local (secrets only)
AUTH_SECRET=...
AUTH_GOOGLE_SECRET=...
UPSTASH_REDIS_REST_TOKEN=...
GROQ_API_KEY=...
STRIPE_SECRET_KEY=...
STRIPE_WEBHOOK_SECRET=...
AUTH_URL=http://localhost:3000  # Optional: can move to config/app.json
```

### Step 2: Verify Config Files

Ensure these files exist and are populated:

**config/stripe.test.json:**
- USD price IDs (6 products)
- INR price IDs (6 products)
- Publishable key
- Display prices with amounts and symbols

**config/app.test.json:**
- auth_url
- google_client_id
- redis_url
- free_limit

### Step 3: Update Code (if needed)

If you have custom code referencing old env vars, update imports:

```typescript
// ❌ Old
const priceId = process.env.STRIPE_WEEKLY_PRICE_ID;

// ✅ New
import { getStripePrices } from '@/lib/stripe-config';
const prices = getStripePrices('usd');
const priceId = prices.weekly;
```

## Dual Currency Support

### How It Works

**Indian users automatically see INR pricing:**
- ₹249/week (primary, bold)
- ($2.99) (secondary, muted)

**International users automatically see USD pricing:**
- $2.99/week (primary, bold)
- (₹249) (secondary, muted)

**Location detection:**
- Server-side: Uses IP headers from Cloudflare/Vercel
- Client-side: Uses browser timezone + IP API fallback
- **Default:** INR (Indian market focus)

**Stripe routing:**
- Indian users → INR price IDs
- International users → USD price IDs

### Testing Different Currencies

**To test as Indian user:**
- Default behavior (INR is default)

**To test as International user:**
- Use VPN to non-Indian country
- Or modify `lib/location-server.ts` to return 'usd' for testing

## FAQ

**Q: Are price IDs secure?**  
A: Yes! Price IDs are public identifiers visible in browser network requests. They're safe to commit to git.

**Q: What about publishable keys?**  
A: Publishable keys are meant to be public (hence the name). Safe in config files.

**Q: Can I still use .env.local for everything?**  
A: Yes, but configs in JSON are better organized and easier to manage.

**Q: Do I need to restart the dev server?**  
A: Only if you change `.env.local` secrets. JSON config changes are picked up automatically.

## Support

If you encounter issues:
1. Check that `config/stripe.test.json` has both USD and INR price IDs
2. Verify `.env.local` has all secrets
3. Run `npm run setup --force` to regenerate products if needed
4. Check browser console for location detection logs

