<!-- b0928a3f-d244-40f3-8b50-3ccd5c30651b d3e0ff2b-900f-45fb-b1ca-f2b44a7090ae -->
# Add App Prefixes to All Environment Variables

## Overview

Add app-specific prefixes (ASK_, REFRAME_, SKETCH2BIM_) to all environment variables used in each application, including shared variables that are currently unprefixed.

## Strategy

- **ASK**: Prefix all variables with `ASK_`
- **Reframe**: Prefix all variables with `REFRAME_`
- **Sketch2BIM**: Prefix all variables with `SKETCH2BIM_`
- Update both code files and `.env.production` file

## Variables to Prefix

### Shared Variables (Need app-specific prefixes)

- `GROQ_API_KEY` → `ASK_GROQ_API_KEY`, `REFRAME_GROQ_API_KEY`, `SKETCH2BIM_GROQ_API_KEY`
- `RAZORPAY_KEY_ID` → `ASK_RAZORPAY_KEY_ID`, `REFRAME_RAZORPAY_KEY_ID`, `SKETCH2BIM_RAZORPAY_KEY_ID`
- `RAZORPAY_KEY_SECRET` → `ASK_RAZORPAY_KEY_SECRET`, `REFRAME_RAZORPAY_KEY_SECRET`, `SKETCH2BIM_RAZORPAY_KEY_SECRET`
- `RAZORPAY_WEBHOOK_SECRET` → `ASK_RAZORPAY_WEBHOOK_SECRET`, `REFRAME_RAZORPAY_WEBHOOK_SECRET`, `SKETCH2BIM_RAZORPAY_WEBHOOK_SECRET`
- `DATABASE_URL` → `ASK_DATABASE_URL`, `SKETCH2BIM_DATABASE_URL` (Reframe doesn't use DB)
- `UPSTASH_REDIS_REST_URL` → `REFRAME_UPSTASH_REDIS_REST_URL`, `SKETCH2BIM_UPSTASH_REDIS_REST_URL`
- `UPSTASH_REDIS_REST_TOKEN` → `REFRAME_UPSTASH_REDIS_REST_TOKEN`, `SKETCH2BIM_UPSTASH_REDIS_REST_TOKEN`
- `REDIS_URL` → `SKETCH2BIM_REDIS_URL`
- `RESEND_API_KEY` → `REFRAME_RESEND_API_KEY` (if used by Reframe)

### ASK-Specific Variables

- `DATABASE_URL_OVERRIDE` → `ASK_DATABASE_URL_OVERRIDE`
- `DATABASE_PASSWORD_OVERRIDE` → `ASK_DATABASE_PASSWORD_OVERRIDE`
- `FRONTEND_URL` → `ASK_FRONTEND_URL`
- `CORS_ORIGINS` → `ASK_CORS_ORIGINS`
- `GROQ_MODEL` → `ASK_GROQ_MODEL`
- `API_BASE_URL` → `ASK_API_BASE_URL`
- `BACKEND_URL` → `ASK_BACKEND_URL`
- `LOG_CSV_FILE` → `ASK_LOG_CSV_FILE`
- `LOG_DIR` → `ASK_LOG_DIR`
- `AUTH_URL` → `ASK_AUTH_URL`

### Reframe-Specific Variables

- `GROQ_DAILY_COST_THRESHOLD` → `REFRAME_GROQ_DAILY_COST_THRESHOLD`
- `GROQ_MONTHLY_COST_THRESHOLD` → `REFRAME_GROQ_MONTHLY_COST_THRESHOLD`
- `FREE_LIMIT` → `REFRAME_FREE_LIMIT`
- `CORS_ORIGINS` → `REFRAME_CORS_ORIGINS`
- `RAZORPAY_DAILY_AMOUNT` → `REFRAME_RAZORPAY_DAILY_AMOUNT`
- `RAZORPAY_MONTH_AMOUNT` → `REFRAME_RAZORPAY_MONTH_AMOUNT`
- `RAZORPAY_YEAR_AMOUNT` → `REFRAME_RAZORPAY_YEAR_AMOUNT`
- `RAZORPAY_PLAN_DAILY` → `REFRAME_RAZORPAY_PLAN_DAILY`
- `RAZORPAY_PLAN_MONTH` → `REFRAME_RAZORPAY_PLAN_MONTH`
- `RAZORPAY_PLAN_YEAR` → `REFRAME_RAZORPAY_PLAN_YEAR`
- `NEXTAUTH_SECRET` → `REFRAME_NEXTAUTH_SECRET`
- `AUTH_SECRET` → `REFRAME_AUTH_SECRET`
- `NEXT_PUBLIC_API_URL` → `REFRAME_NEXT_PUBLIC_API_URL`
- `NEXT_PUBLIC_SITE_URL` → `REFRAME_NEXT_PUBLIC_SITE_URL`
- `NEXT_PUBLIC_FREE_LIMIT` → `REFRAME_NEXT_PUBLIC_FREE_LIMIT`
- `REFRAME_API_URL` → Already prefixed

### Sketch2BIM-Specific Variables

- `DATABASE_URL_OVERRIDE` → `SKETCH2BIM_DATABASE_URL_OVERRIDE`
- `DATABASE_PASSWORD_OVERRIDE` → `SKETCH2BIM_DATABASE_PASSWORD_OVERRIDE`
- `FRONTEND_URL` → `SKETCH2BIM_FRONTEND_URL`
- `SECRET_KEY` → `SKETCH2BIM_SECRET_KEY`
- `NEXTAUTH_SECRET` → `SKETCH2BIM_NEXTAUTH_SECRET`
- `NEXT_PUBLIC_API_URL` → `SKETCH2BIM_NEXT_PUBLIC_API_URL`
- `AUTH_URL` → `SKETCH2BIM_AUTH_URL`
- `BUNNY_STORAGE_ZONE` → `SKETCH2BIM_BUNNY_STORAGE_ZONE`
- `BUNNY_ACCESS_KEY` → `SKETCH2BIM_BUNNY_ACCESS_KEY`
- `BUNNY_CDN_HOSTNAME` → `SKETCH2BIM_BUNNY_CDN_HOSTNAME`
- `JSON_LOGGING` → `SKETCH2BIM_JSON_LOGGING`

## Files to Update

### ASK Files

1. `apps/ask/api/config.py` - Update all `os.getenv()` calls
2. `apps/ask/api/main.py` - Update `CORS_ORIGINS`
3. `apps/ask/api/services/groq_service.py` - Update `GROQ_API_KEY`, `GROQ_MODEL`
4. `apps/ask/api/routes/qa_pairs.py` - Update `API_BASE_URL`, `BACKEND_URL`
5. `apps/ask/api/services/csv_service.py` - Update `LOG_CSV_FILE`
6. `apps/ask/frontend/auth.ts` - Update `AUTH_URL` (already has `ASK_GOOGLE_CLIENT_ID`)
7. `apps/ask/main.py` - Update `LOG_DIR`
8. `apps/ask/main_text_only.py` - Update `LOG_DIR`
9. `apps/ask/research_csv_manager.py` - Update `LOG_CSV_FILE`
10. `apps/ask/volume_manager.py` - Update `LOG_CSV_FILE`

### Reframe Files

1. `apps/reframe/backend/app/config.py` - Update all `os.getenv()` calls
2. `apps/reframe/backend/app/routes/reframe.py` - Update `FREE_LIMIT`
3. `apps/reframe/backend/app/services/groq_monitor.py` - Update `GROQ_DAILY_COST_THRESHOLD`, `GROQ_MONTHLY_COST_THRESHOLD`
4. `apps/reframe/backend/app/services/groq_service.py` - Update `GROQ_API_KEY`
5. `apps/reframe/backend/app/services/redis_service.py` - Update `UPSTASH_REDIS_REST_URL`, `UPSTASH_REDIS_REST_TOKEN`
6. `apps/reframe/lib/groq-monitor.ts` - Update `GROQ_DAILY_COST_THRESHOLD`, `GROQ_MONTHLY_COST_THRESHOLD`
7. `apps/reframe/lib/groq.ts` - Update `GROQ_API_KEY`
8. `apps/reframe/lib/redis.ts` - Update `UPSTASH_REDIS_REST_URL`, `UPSTASH_REDIS_REST_TOKEN`
9. `apps/reframe/lib/app-config.ts` - Update all Razorpay variables
10. `apps/reframe/app/api/reframe-proxy/route.ts` - Update `REFRAME_API_URL`, `NEXT_PUBLIC_API_URL`, `NEXTAUTH_SECRET`, `AUTH_SECRET`
11. `apps/reframe/app/api/usage/route.ts` - Update `NEXT_PUBLIC_FREE_LIMIT`
12. `apps/reframe/app/api/razorpay/checkout/route.ts` - Update `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`, `AUTH_URL`, `NEXT_PUBLIC_SITE_URL`
13. `apps/reframe/app/api/waitlist/route.ts` - Update `RESEND_API_KEY`
14. `apps/reframe/scripts/create_razorpay_plans.ts` - Update `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`

### Sketch2BIM Files

1. `apps/sketch2bim/backend/app/config.py` - Update all `os.getenv()` calls
2. `apps/sketch2bim/backend/app/routes/payments.py` - Update `FRONTEND_URL`
3. `apps/sketch2bim/backend/app/main.py` - Update `JSON_LOGGING`
4. `apps/sketch2bim/frontend/auth.ts` - Update `AUTH_URL` (already has `SKETCH2BIM_GOOGLE_CLIENT_ID`)
5. `apps/sketch2bim/frontend/lib/api.ts` - Update `NEXT_PUBLIC_API_URL`
6. `apps/sketch2bim/frontend/next.config.js` - Update `NEXT_PUBLIC_API_URL`
7. `apps/sketch2bim/frontend/lib/errorLogger.ts` - Update `NEXT_PUBLIC_API_URL`
8. `apps/sketch2bim/scripts/create_razorpay_plans.py` - Update `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`
9. `apps/sketch2bim/scripts/delete_razorpay_plan.py` - Update `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`

### Configuration Files

1. `apps/ask/render.yaml` - Update environment variable references
2. `apps/reframe/render.yaml` - Update environment variable references
3. `apps/sketch2bim/infra/render.yaml` - Update environment variable references
4. `apps/sketch2bim/infra/vercel.json` - Update environment variable references
5. `apps/sketch2bim/infra/docker-compose.yml` - Update environment variable references
6. `apps/sketch2bim/infra/docker-compose.prod.yml` - Update environment variable references

### Documentation Files

1. `apps/ask/docs/ENVIRONMENT_VARIABLES.md` - Update variable names
2. `apps/sketch2bim/docs/ENVIRONMENT_VARIABLES.md` - Update variable names
3. `apps/reframe/readme.md` - Update variable names (if documented)

### Environment File

1. `.env.production` - Update all variable names using PowerShell to add prefixes

## Implementation Steps

1. **Update .env.production using PowerShell**

- Add prefixed versions of all shared variables
- Update existing prefixed variables if needed
- Keep old unprefixed variables commented out for reference during migration

2. **Update ASK code files**

- Replace all `os.getenv()` and `process.env` references with prefixed versions
- Update config.py to use prefixed variables

3. **Update Reframe code files**

- Replace all environment variable references with `REFRAME_` prefix
- Update both backend Python and frontend TypeScript files

4. **Update Sketch2BIM code files**

- Replace all environment variable references with `SKETCH2BIM_` prefix
- Update both backend Python and frontend TypeScript files

5. **Update deployment configurations**

- Update render.yaml files to use prefixed variable names
- Update vercel.json and docker-compose files

6. **Update documentation**

- Update environment variable documentation to reflect new names

## Notes

- `NODE_ENV` should remain unprefixed (standard Node.js variable)
- Some variables like `DATABASE_SCHEMA` already have prefixes in .env.production
- Google OAuth variables already have prefixes
- Need to ensure backward compatibility is not required (user wants full prefix migration)
- PowerShell will be used to update .env.production file efficiently