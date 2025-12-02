# Local Testing Guide

This guide covers how to test all routes, authentication, API calls, and subscriptions locally before deploying to production.

## Prerequisites

1. **Environment Variables**: Copy `.env.example` to `.env.local` and fill in all required values
2. **Databases**: Set up local PostgreSQL or use Upstash Postgres
3. **Redis**: Set up local Redis or use Upstash Redis
4. **Dependencies**: Install all dependencies

## Setup

### 1. Install Dependencies

```bash
# Install Node.js dependencies
npm install

# Install Python dependencies
cd apps/platform-api
pip install -e ../../packages/shared-backend
pip install -r requirements.txt
cd ../..
```

### 2. Set Environment Variables

Create `.env.local` with all required variables (see Environment Variables section below).

### 3. Run Database Migrations

```bash
# ASK database
cd database/migrations/ask
alembic upgrade head

# Sketch2BIM database
cd ../sketch2bim
alembic upgrade head
```

## Running Locally

### Start the Frontend

```bash
npm run dev
```

Frontend will be available at: http://localhost:3000

### Start the Backend

```bash
cd apps/platform-api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000

## Testing Checklist

### Frontend Tests

- [ ] **Home page loads**: http://localhost:3000
- [ ] **ASK page loads**: http://localhost:3000/ask
- [ ] **Reframe page loads**: http://localhost:3000/reframe
- [ ] **Sketch2BIM page loads**: http://localhost:3000/sketch2bim
- [ ] **Subscribe page loads**: http://localhost:3000/subscribe
- [ ] **Account page loads**: http://localhost:3000/account
- [ ] **Projects page loads**: http://localhost:3000/projects

### Backend Tests

- [ ] **Health check**: http://localhost:8000/health
- [ ] **Root endpoint**: http://localhost:8000/
- [ ] **API docs**: http://localhost:8000/docs

### Authentication Tests

- [ ] **Sign in with Google**: Click sign in button
- [ ] **JWT token generated**: Check browser dev tools > Application > Cookies
- [ ] **User created in database**: Check users table
- [ ] **Sign out**: Click sign out button

### ASK API Tests

- [ ] **GET /api/ask/qa-pairs**: Fetch Q&A pairs
- [ ] **GET /api/ask/themes**: Fetch themes
- [ ] **GET /api/ask/stats**: Get statistics
- [ ] **POST /api/ask/generate/start**: Start content generation
- [ ] **POST /api/ask/generate/next**: Continue generation
- [ ] **GET /api/ask/monitoring**: Check monitoring data

### Reframe API Tests

- [ ] **POST /api/reframe**: Submit reframe request
- [ ] **GET /api/reframe/subscription**: Check subscription status

### Sketch2BIM API Tests

- [ ] **POST /api/sketch2bim/generate**: Create new job
- [ ] **GET /api/sketch2bim/health**: Health check
- [ ] **GET /api/sketch2bim/monitoring**: Check monitoring data

### Subscription Tests

- [ ] **GET /api/subscriptions/status**: Get subscription status
- [ ] **POST /api/subscriptions/checkout** with tier: "week"
- [ ] **POST /api/subscriptions/checkout** with tier: "monthly"
- [ ] **POST /api/subscriptions/checkout** with tier: "yearly"

### Payment Tests

**Note**: Use Razorpay test mode credentials

- [ ] Create week subscription
- [ ] Create monthly subscription
- [ ] Create yearly subscription
- [ ] Verify webhook receives payment.captured event
- [ ] Verify user subscription is updated in database
- [ ] Check payment record is created
- [ ] Verify subscription expiry date is correct

### Database Tests

- [ ] **Users table**: Verify users are created on sign-in
- [ ] **Payments table**: Verify payments are recorded
- [ ] **Jobs table**: Verify Sketch2BIM jobs are created
- [ ] **Groq usage table**: Verify API usage is tracked

## Environment Variables

### Required for All Apps

```bash
# NextAuth
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-here

# Google OAuth
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret

# Platform
PLATFORM_FRONTEND_URL=http://localhost:3000
PLATFORM_API_URL=http://localhost:8000
```

### ASK

```bash
ASK_DATABASE_URL=postgresql://user:password@localhost:5432/ask
ASK_GROQ_API_KEY=your-groq-api-key
ASK_GROQ_MONTHLY_COST_THRESHOLD=10.0
ASK_RAZORPAY_KEY_ID=rzp_test_xxxxx
ASK_RAZORPAY_KEY_SECRET=your-secret
ASK_RAZORPAY_WEBHOOK_SECRET=your-webhook-secret
```

### Reframe

```bash
REFRAME_REDIS_URL=redis://localhost:6379
REFRAME_GROQ_API_KEY=your-groq-api-key
REFRAME_GROQ_MONTHLY_COST_THRESHOLD=10.0
REFRAME_RAZORPAY_KEY_ID=rzp_test_xxxxx
REFRAME_RAZORPAY_KEY_SECRET=your-secret
REFRAME_RAZORPAY_WEBHOOK_SECRET=your-webhook-secret
```

### Sketch2BIM

```bash
SKETCH2BIM_DATABASE_URL=postgresql://user:password@localhost:5432/sketch2bim
SKETCH2BIM_GROQ_API_KEY=your-groq-api-key
SKETCH2BIM_GROQ_MONTHLY_COST_THRESHOLD=10.0
SKETCH2BIM_RAZORPAY_KEY_ID=rzp_test_xxxxx
SKETCH2BIM_RAZORPAY_KEY_SECRET=your-secret
SKETCH2BIM_RAZORPAY_WEBHOOK_SECRET=your-webhook-secret
SKETCH2BIM_BUNNY_STORAGE_ZONE=your-zone-id
SKETCH2BIM_BUNNY_API_KEY=your-api-key
SKETCH2BIM_BUNNY_CDN_HOSTNAME=your-hostname.b-cdn.net
```

### Platform (Unified)

```bash
PLATFORM_RAZORPAY_KEY_ID=rzp_test_xxxxx
PLATFORM_RAZORPAY_KEY_SECRET=your-secret
PLATFORM_RAZORPAY_WEBHOOK_SECRET=your-webhook-secret
PLATFORM_RAZORPAY_PLAN_WEEK=plan_xxxxx
PLATFORM_RAZORPAY_PLAN_MONTH=plan_xxxxx
PLATFORM_RAZORPAY_PLAN_YEAR=plan_xxxxx
```

## Using Test Credentials

### Razorpay Test Mode

Use test credentials from Razorpay Dashboard > Settings > API Keys > Test Mode

Test card numbers:
- Success: 4111 1111 1111 1111
- Failure: 4000 0000 0000 0002

CVV: Any 3 digits
Expiry: Any future date

### Database Setup

For local testing, you can use:
- PostgreSQL locally (via Docker or native install)
- Upstash Postgres (free tier)

## Common Issues

### Frontend not connecting to backend
- Check NEXT_PUBLIC_API_URL is set correctly
- Verify backend is running on correct port
- Check CORS settings in backend

### Authentication failing
- Verify NEXTAUTH_SECRET is set
- Check Google OAuth credentials
- Verify callback URLs in Google Console

### Database connection failing
- Check DATABASE_URL format
- Verify database is running
- Check migrations have been run

### API calls failing
- Check JWT token in request headers
- Verify user is authenticated
- Check API endpoint paths are correct

## Next Steps

After all local tests pass:
1. Deploy to staging
2. Run same tests on staging
3. Deploy to production
4. Monitor for 1-2 weeks
5. Clean up old services

