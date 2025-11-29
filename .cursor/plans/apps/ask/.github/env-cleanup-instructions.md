# .env.local Cleanup Instructions

Your current `.env.local` has duplicate and outdated entries. Here's what to remove:

## ❌ Remove These Lines (Duplicates)

```env
# Remove first AUTH_URL (keep localhost one)
#AUTH_URL=https://reframe-ai-seven.vercel.app

# Remove live Stripe keys (keep only test)
#STRIPE_KEY_PUBLISHABLE=pk_live_2UDHQxbktN5sOx4URR3p2xBr
#STRIPE_SECRET_KEY=sk_live_ywsRrAeVNphfisdV6gICF5Mj00elbZIAEI
#STRIPE_WEBHOOK_SECRET=whsec_4xosdmXPv4pcCKqnen4O2EjXtBx7jwb5

# Remove ALL Stripe price IDs (now in config/stripe.test.json)
STRIPE_WEEKLY_PRICE_ID=...
STRIPE_MONTHLY_PRICE_ID=...
STRIPE_YEARLY_PRICE_ID=...
STRIPE_CREDIT_PACK_STARTER_PRICE_ID=...
STRIPE_CREDIT_PACK_STANDARD_PRICE_ID=...
STRIPE_CREDIT_PACK_PREMIUM_PRICE_ID=...

# Remove ALL Clerk variables (not using Clerk)
CLERK_PUBLISHABLE_KEY_PUBLIC=...
CLERK_PUBLISHABLE_KEY_SERVER=...
CLERK_SECRET_KEY=...

# Remove GitHub OAuth (not configured)
AUTH_GITHUB_ID=...
AUTH_GITHUB_SECRET=...
GITHUB_OAUTH_CLIENT_ID_PROD=...
GITHUB_OAUTH_CLIENT_SECRET_PROD=...

# Remove unused Google OAuth extras
GOOGLE_OAUTH_PROJECT_ID=...
GOOGLE_OAUTH_AUTH_URI=...
GOOGLE_OAUTH_TOKEN_URI=...
GOOGLE_OAUTH_CERT_URL=...
GOOGLE_OAUTH_REDIRECT_URL_DEV=...
GOOGLE_OAUTH_REDIRECT_URL_PROD=...
GOOGLE_OAUTH_ORIGIN_DEV=...
GOOGLE_OAUTH_ORIGIN_PROD=...

# Remove unused Redis extras
UPSTASH_REDIS_API_KEY=...
# NECTION_URL=...

# Remove OpenAI key (using Groq)
OPENAI_API_KEY=...

# Remove test publishable key (now in config)
STRIPE_KEY_PUBLISHABLE=pk_test_...
```

## ✅ Your Clean .env.local Should Look Like:

```env
# =============================================================================
# SECRETS ONLY - Public configs are in config/ directory
# =============================================================================

# Core Application
AUTH_URL=http://localhost:3000

# Session Management
AUTH_SECRET=lFGHiDWlnSC1yn1F95VgqttX0WZ2s4o+Ybsm9ELw564=

# OAuth - Google
AUTH_GOOGLE_ID=620186529337-b5o91ohmbfpbatv8gaa35ct4i0s9i2ru.apps.googleusercontent.com
AUTH_GOOGLE_SECRET=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

# Database
UPSTASH_REDIS_REST_URL=https://splendid-platypus-26441.upstash.io
UPSTASH_REDIS_REST_TOKEN=AWdJAAIncDJjZTMyOGIzZTc3ZmU0MjVhYmZmMDJiODgyYjhlY2NmZHAyMjY0NDE

# AI Services
GROQ_API_KEY=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

# Payment Processing - TEST MODE
STRIPE_SECRET_KEY=sk_test_GKqkmph47WtZ0XVtYKCfqm6C
STRIPE_WEBHOOK_SECRET=whsec_ctkLIitYUIFOQhRL2k6cZD8bfd8VhYXm

# Public Config
NEXT_PUBLIC_FREE_LIMIT=3
```

**That's only ~15 lines!** Much cleaner than the current 100+ lines.

## Optional: AUTH_GOOGLE_ID and UPSTASH_REDIS_REST_URL

These are public values and could also move to `config/app.test.json`, but keeping them in `.env.local` is fine for convenience.

---

**After cleaning .env.local, this file has been archived to `.github/` folder.**

