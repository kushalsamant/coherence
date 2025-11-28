# Reframe

Transform AI-generated text with authentic human voices using Groq's Llama 3.1 8B model. Choose from 6 distinct tones × 9 generations (Silent Generation to Gen Beta) = 54 unique voices for any audience.

**Live:** [reframe.kvshvl.in](https://reframe.kvshvl.in)

---

## Features

- **6 Authentic Tones** - Conversational, Professional, Academic, Enthusiastic, Empathetic, Witty
- **9 Generation Targeting** - Silent Generation, Boomers, Gen X, Millennials, Gen Z, Gen Alpha, Gen Beta, Kids
- **54 Unique Voices** - 6 tones × 9 generations = tailored content for any audience
- **10,000 Words/Request** - Fixed limit, simple and generous
- **Google OAuth** - Simple sign-in, no email verification needed
- **INR Pricing** - ₹99-₹7,999 with live USD/EUR/GBP conversions
- **Flexible Payment** - Daily passes, credit packs, or subscriptions
- **Usage Tracking** - Redis-powered rate limiting
- **Cost Efficient** - Groq inference 500x cheaper than OpenAI

---

## Tech Stack

- **Frontend:** Next.js 15, React, TailwindCSS, shadcn/ui (Vercel)
- **Backend:** FastAPI (Python 3.11+, deployed on Render)
- **Auth:** NextAuth v5 (Google OAuth) with JWT validation in FastAPI
- **AI:** Groq Llama 3.1 8B Instant
- **Storage:** Upstash Redis REST API (usage tracking and user metadata)
- **Payments:** Razorpay (INR only, handled in Next.js API routes)
- **Hosting:** 
  - Frontend: Vercel
  - Backend: Render (FastAPI web service)

---

## Prerequisites

- Node.js 18+ (for frontend)
- Python 3.11+ (for backend)
- Accounts for:
  - [Google Cloud](https://console.cloud.google.com) - OAuth
  - [Groq](https://console.groq.com) - AI inference
  - [Upstash](https://console.upstash.com) - Redis
  - [Razorpay](https://dashboard.razorpay.com) - Payments
  - [Render](https://render.com) - Backend hosting

---

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Environment Variables

> **⚠️ IMPORTANT: Centralized Environment Variables**  
> All production environment variables are in `reframe.env.production` at the repository root.  
> This is the single source of truth for all production secrets across all repos (ASK, Reframe, Sketch2BIM).  
> The Next.js config automatically loads that file (when present) before applying `.env.local`, so local overrides still win.

For local development, create `.env.local` (this file is gitignored):

```env
# Auth (generate with: openssl rand -base64 32)
REFRAME_AUTH_SECRET=your-secret-here
REFRAME_GOOGLE_CLIENT_ID=your-id.apps.googleusercontent.com
REFRAME_GOOGLE_CLIENT_SECRET=your-secret

# Groq AI
REFRAME_GROQ_API_KEY=gsk_...

# Upstash Redis
REFRAME_UPSTASH_REDIS_REST_URL=https://...upstash.io
REFRAME_UPSTASH_REDIS_REST_TOKEN=...

# Razorpay
REFRAME_RAZORPAY_KEY_ID=rzp_test_...
REFRAME_RAZORPAY_KEY_SECRET=...
REFRAME_RAZORPAY_WEBHOOK_SECRET=whsec_...

# Optional
REFRAME_NEXT_PUBLIC_FREE_LIMIT=3
```

**Note:** All environment variables should use the `REFRAME_` prefix. Unprefixed versions are deprecated but still supported for backward compatibility.

### 3. Configure Razorpay

Razorpay pricing is configured in the checkout route. Plan IDs can be set up later via Razorpay dashboard or scripts.

### 4. Setup Backend (FastAPI)

The backend is a FastAPI application deployed on Render. The main reframe endpoint (`/api/reframe`) is handled by the FastAPI backend, while other endpoints (payments, webhooks) remain in Next.js API routes.

**Local Development:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Environment Variables for Backend:**
- `REFRAME_GROQ_API_KEY` / `GROQ_API_KEY` (deprecated) - Groq API key (prefixed version required)
- `REFRAME_UPSTASH_REDIS_REST_URL` / `UPSTASH_REDIS_REST_URL` (deprecated) - Upstash Redis REST URL (prefixed version required)
- `REFRAME_UPSTASH_REDIS_REST_TOKEN` / `UPSTASH_REDIS_REST_TOKEN` (deprecated) - Upstash Redis REST token (prefixed version required)
- `REFRAME_NEXTAUTH_SECRET` / `REFRAME_AUTH_SECRET` / `NEXTAUTH_SECRET` (deprecated) / `AUTH_SECRET` (deprecated) - JWT secret (same as frontend, prefixed version required)
- `REFRAME_JWT_ALGORITHM` / `JWT_ALGORITHM` (deprecated) - JWT algorithm (default: HS256, prefixed version preferred)
- `REFRAME_CORS_ORIGINS` / `CORS_ORIGINS` (deprecated) - Comma-separated allowed origins (e.g., `http://localhost:3000,https://reframe.kvshvl.in`, prefixed version required)
- `REFRAME_FREE_LIMIT` / `FREE_LIMIT` (deprecated) - Free tier request limit (default: 5, prefixed version preferred)
- `REFRAME_ENVIRONMENT` / `ENVIRONMENT` (deprecated) - Environment name (default: development, prefixed version preferred)
- `REFRAME_DEBUG` / `DEBUG` (deprecated) - Debug mode (default: false, prefixed version preferred)

**Architecture:**
- Frontend calls `/api/reframe-proxy` (Next.js API route)
- Proxy route adds JWT token from NextAuth session
- Proxy forwards request to FastAPI backend at `${REFRAME_API_URL}/api/reframe`
- FastAPI validates JWT, processes request, returns reframed text

**Deployment:**
Deploy to Render using `render.yaml`. The backend will be available at the Render URL, which should be set as `REFRAME_API_URL` or `NEXT_PUBLIC_API_URL` in Vercel environment variables.

### 5. Setup External Services

**Google OAuth:**
1. [Create OAuth credentials](https://console.cloud.google.com/apis/credentials)
2. Add redirect URI: `http://localhost:3000/api/auth/callback/google`
3. Copy Client ID and Secret to `reframe.env.production` or local `.env.local`

**Groq:**
1. [Get API key](https://console.groq.com/keys)
2. Add to `reframe.env.production` or local `.env.local`

**Upstash Redis:**
1. [Create database](https://console.upstash.com)
2. Copy REST URL and Token to `reframe.env.production` or local `.env.local`

**Razorpay:**
1. [Get API keys](https://dashboard.razorpay.com/app/keys)
2. Create webhook endpoint: `https://your-domain.vercel.app/api/razorpay-webhook`
3. Copy webhook secret to `RAZORPAY_WEBHOOK_SECRET`
4. (Optional) Create subscription plans for recurring payments

### 6. Run Development Server

```bash
npm run dev
```

Visit [http://localhost:3000](http://localhost:3000)

---

## Current Pricing (INR Only)

### Subscriptions
- **Free:** ₹0 - 3 requests/day, 3 tones
- **Weekly:** ₹349/week - 50 requests/week, all tones
- **Monthly:** ₹999/month - Unlimited, all tones
- **Yearly:** ₹7,999/year - Unlimited, save 33%

### Credit Packs (One-Time)
- **Starter:** ₹299 - 10 credits
- **Standard:** ₹699 - 30 credits  
- **Premium:** ₹1,799 - 100 credits

*Credits never expire. 1 credit = 1 request with any tone/limit.*

---

## Production Deployment

### Vercel Setup

1. **Push to GitHub**

```bash
git push origin main
```

2. **Import to Vercel**
   - Connect your repository
   - Vercel auto-detects Next.js

3. **Add Environment Variables**

In Vercel dashboard, add:
- `REFRAME_AUTH_URL` / `AUTH_URL` (deprecated) = `https://your-domain.vercel.app` (prefixed version preferred)
- `REFRAME_AUTH_SECRET` / `AUTH_SECRET` (deprecated) (prefixed version required)
- `REFRAME_GOOGLE_CLIENT_ID` (prefixed version required)
- `REFRAME_GOOGLE_SECRET` (prefixed version required)
- `REFRAME_GROQ_API_KEY` / `GROQ_API_KEY` (deprecated) (prefixed version required)
- `REFRAME_UPSTASH_REDIS_REST_URL` / `UPSTASH_REDIS_REST_URL` (deprecated) (prefixed version required)
- `REFRAME_UPSTASH_REDIS_REST_TOKEN` / `UPSTASH_REDIS_REST_TOKEN` (deprecated) (prefixed version required)
- `REFRAME_RAZORPAY_KEY_ID` / `RAZORPAY_KEY_ID` (deprecated) (use `rzp_live_...` for production, prefixed version required)
- `REFRAME_RAZORPAY_KEY_SECRET` / `RAZORPAY_KEY_SECRET` (deprecated) (prefixed version required)
- `REFRAME_RAZORPAY_WEBHOOK_SECRET` / `RAZORPAY_WEBHOOK_SECRET` (deprecated) (prefixed version required)

4. **Update Google OAuth**

Add production redirect URI:
```
https://your-domain.vercel.app/api/auth/callback/google
```

5. **Setup Razorpay Webhook**

- URL: `https://your-domain.vercel.app/api/razorpay-webhook`
- Events: `payment.captured`, `subscription.activated`, `subscription.charged`, `subscription.cancelled`
- Copy webhook secret to `RAZORPAY_WEBHOOK_SECRET`

6. **Deploy**

Vercel deploys automatically on push to `main`.

---

## Project Structure

```
reframe/
├── app/
│   ├── page.tsx              # Main app (reframe interface)
│   ├── pricing/              # Pricing page
│   ├── settings/             # User settings
│   ├── api/
│   │   ├── reframe-proxy/    # Proxy to FastAPI backend (adds JWT)
│   │   ├── create-checkout/  # Razorpay checkout
│   │   ├── razorpay-webhook/ # Payment webhooks
│   │   └── exchange-rates/   # Live currency conversion
│   ├── sign-in/              # Google OAuth sign-in
│   ├── terms/                # Terms of service
│   └── privacy/              # Privacy policy
├── backend/                  # FastAPI backend (deployed on Render)
│   ├── app/
│   │   ├── main.py           # FastAPI app entry point
│   │   ├── auth.py           # NextAuth JWT validation
│   │   ├── config.py         # Application settings
│   │   ├── models.py         # Pydantic request/response models
│   │   ├── routes/
│   │   │   └── reframe.py    # Main reframe endpoint
│   │   └── services/
│   │       ├── redis_service.py         # Upstash Redis REST API client
│   │       ├── subscription_service.py # Subscription logic
│   │       ├── tone_service.py          # Tone system
│   │       ├── groq_service.py           # Groq API client
│   │       ├── groq_monitor.py          # Usage tracking
│   │       └── user_metadata_service.py # User metadata management
│   ├── requirements.txt      # Python dependencies
│   └── render.yaml          # Render deployment config
├── components/
│   └── ui/                   # shadcn/ui components
├── lib/
│   ├── api-client.ts        # API client (calls FastAPI via proxy)
│   ├── redis.ts             # Redis client (frontend utilities)
│   ├── razorpay.ts          # Razorpay client
│   └── tones.ts             # 6 tone definitions
└── auth.ts                  # NextAuth configuration
```

---

## Tone System

| Tone | Icon | Description | Access |
|------|------|-------------|--------|
| Conversational | 💬 | Friendly, casual, relatable | Free |
| Professional | 💼 | Polished, formal, business-like | Free |
| Academic | 🎓 | Scholarly, analytical | Free |
| Enthusiastic | ⚡ | Energetic, exciting | Pro |
| Empathetic | 💙 | Warm, compassionate | Pro |
| Witty | 😄 | Clever, humorous | Pro |

---

## Character Limits

| Tier | Characters | Cost/Request | Use Case | Free | Pro |
|------|-----------|--------------|----------|------|-----|
| Conservative | 10,000 | ~₹0.03 | Blog posts | ✅ | ✅ |
| Moderate | 50,000 | ~₹0.15 | Essays | ✅ | ✅ |
| Maximum | 250,000 | ~₹0.60 | Books | ❌ | ✅ |

*Using Groq: $0.05/M input + $0.08/M output tokens*

---

## Configuration Files

### Pricing Configuration

Pricing is configured in `app/api/create-checkout/route.ts`:

- **Daily/Weekly:** ₹349/week
- **Monthly:** ₹999/month
- **Yearly:** ₹7,999/year
- **Credit Packs:** ₹299 (10), ₹699 (30), ₹1,799 (100)

For subscription plans, create them in Razorpay dashboard and set plan IDs in environment variables.

---

## Common Issues

### Sign-in redirects to localhost
**Fix:** Set `AUTH_URL` in Vercel environment variables to your production domain.

### Razorpay webhook fails
**Fix:** Verify `RAZORPAY_WEBHOOK_SECRET` matches Razorpay Dashboard, then redeploy.

### Redis connection error
**Fix:** Check `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN` (no quotes).

### 404 on checkout
**Fix:** Ensure you're signed in before accessing checkout URLs.

---

## License

MIT

---

## Contact

- **Email:** writetokushaldsamant@gmail.com
- **Production:** [reframe.kvshvl.in](https://reframe.kvshvl.in)
- **Repository:** [github.com/kushalsamant/kushalsamant.github.io/tree/main/apps/reframe](https://github.com/kushalsamant/kushalsamant.github.io/tree/main/apps/reframe)

---

*Last Updated: November 8, 2025*
