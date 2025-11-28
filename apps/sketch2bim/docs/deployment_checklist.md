# Production Deployment Checklist

This checklist ensures all production environment variables and configurations are set correctly.

## Environment Variables

### Frontend (Vercel)
**Location**: https://vercel.com/kvshvl/sketch2bim/settings/environment-variables

Copy these variables to Vercel:

```
SKETCH2BIM_GOOGLE_CLIENT_ID=620186529337-b5o91ohmbfpbatv8gaa35ct4i0s9i2ru.apps.googleusercontent.com
SKETCH2BIM_GOOGLE_SECRET=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
AUTH_SECRET=lFGHiDWlnSC1yn1F95VgqttX0WZ2s4o+Ybsm9ELw564=
AUTH_URL=https://sketch2bim.kvshvl.in
NEXT_PUBLIC_API_URL=https://sketch2bim-backend.onrender.com
NEXT_PUBLIC_FREE_LIMIT=5
```

**Verification Checklist:**
- [ ] All variables are set in Vercel dashboard
- [ ] `AUTH_URL` matches your frontend URL exactly (no trailing slash)
- [ ] `NEXT_PUBLIC_API_URL` points to your backend URL

### Backend (Render)
**Location**: https://dashboard.render.com/web/srv-xxx/env

Copy these variables to Render:

```
ALLOWED_ORIGINS=https://sketch2bim.kvshvl.in
APP_ENV=production
BUNNY_ACCESS_KEY=4026f19d-3836-4442-ba87fe2013c4-4f75-4944
BUNNY_CDN_HOSTNAME=kvshvl.b-cdn.net
BUNNY_REGION=storage.bunnycdn.com
BUNNY_STORAGE_ZONE=kvshvl
DATABASE_URL=postgresql://postgres.twxudlzipbiavnzcitzb:linkeDin99-k@aws-1-ap-southeast-2.pooler.supabase.com:6543/postgres
DEBUG=false
FRONTEND_URL=https://sketch2bim.kvshvl.in
JSON_LOGGING=false
LOG_LEVEL=INFO
NEXTAUTH_SECRET=lFGHiDWlnSC1yn1F95VgqttX0WZ2s4o+Ybsm9ELw564=
REDIS_URL=redis://default:AWdJAAIncDJjZTMyOGIzZTc3ZmU0MjVhYmZmMDJiODgyYjhlY2NmZHAyMjY0NDE@splendid-platypus-26441.upstash.io:6379
RESEND_API_KEY=re_EXWqUYav_AKcCzgFrSSrahYHJHB6majyk
SECRET_KEY=lFGHiDWlnSC1yn1F95VgqttX0WZ2s4o+Ybsm9ELw564=
# Razorpay Payment Gateway
# Razorpay Payment Gateway (shared across all projects)
SKETCH2BIM_RAZORPAY_KEY_ID=rzp_live_RhNUuWRBG7lzR4
SKETCH2BIM_RAZORPAY_KEY_SECRET=7T1MCu1xNjX9G4soT7kuqqdB
SKETCH2BIM_RAZORPAY_WEBHOOK_SECRET=<SET_IN_RAZORPAY_DASHBOARD>
# Pricing amounts (shared across all projects)
SKETCH2BIM_RAZORPAY_WEEK_AMOUNT=129900
SKETCH2BIM_RAZORPAY_MONTH_AMOUNT=349900
SKETCH2BIM_RAZORPAY_YEAR_AMOUNT=2999900
# Plan IDs (shared across all projects - same plan IDs for ASK, Sketch2BIM, Reframe)
SKETCH2BIM_RAZORPAY_PLAN_WEEK=<PLAN_ID_FROM_RAZORPAY>
SKETCH2BIM_RAZORPAY_PLAN_MONTH=<PLAN_ID_FROM_RAZORPAY>
SKETCH2BIM_RAZORPAY_PLAN_YEAR=<PLAN_ID_FROM_RAZORPAY>
# Note: Code also accepts unprefixed variables (RAZORPAY_*) for backward compatibility
# Optional: Disable auto-migrations (default: enabled)
# AUTO_RUN_MIGRATIONS=false
```

### Environment Variables Verification Checklist

**Critical Variables to Verify:**

- [ ] `SKETCH2BIM_RAZORPAY_KEY_ID` is set (prefixed version required, `RAZORPAY_KEY_ID` deprecated)
- [ ] `SKETCH2BIM_RAZORPAY_KEY_SECRET` is set (prefixed version required, `RAZORPAY_KEY_SECRET` deprecated)
- [ ] `SKETCH2BIM_RAZORPAY_WEBHOOK_SECRET` is set from Razorpay dashboard (prefixed version required, `RAZORPAY_WEBHOOK_SECRET` deprecated)
- [ ] `SKETCH2BIM_RAZORPAY_PLAN_WEEK` is set (Plan ID, not empty, prefixed version required, `RAZORPAY_PLAN_WEEK` deprecated)
- [ ] `SKETCH2BIM_RAZORPAY_PLAN_MONTH` is set (Plan ID, not empty, prefixed version required, `RAZORPAY_PLAN_MONTH` deprecated)
- [ ] `SKETCH2BIM_RAZORPAY_PLAN_YEAR` is set (Plan ID, not empty, prefixed version required, `RAZORPAY_PLAN_YEAR` deprecated)

**Variable Name Compatibility:**

If you have `LIVE_KEY_ID` and `LIVE_KEY_SECRET` set, you must also add:
```
RAZORPAY_KEY_ID=rzp_live_RhNUuWRBG7lzR4
RAZORPAY_KEY_SECRET=7T1MCu1xNjX9G4soT7kuqqdB
```

The code expects `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET`. The `LIVE_KEY_ID` and `LIVE_KEY_SECRET` are kept for backward compatibility but are not used directly.

**Notes:**
- One-time payments will work immediately (no Plans needed)
- Subscriptions require Plans to be created first
- Keep `LIVE_KEY_ID` and `LIVE_KEY_SECRET` for backward compatibility
- Add `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET` as aliases

## Pre-Deployment Steps

### 1. Create Razorpay Subscription Plans

Before configuring webhooks, create the subscription plans:

1. Run the plan creation script:
```bash
python scripts/create_razorpay_plans.py
```

2. The script will output plan IDs for each tier:
   - `RAZORPAY_PLAN_WEEK` - Week Pass subscription
   - `RAZORPAY_PLAN_MONTH` - Month subscription
   - `RAZORPAY_PLAN_YEAR` - Year subscription

3. Copy these plan IDs to Render environment variables:
   - Go to Render dashboard → Your service → Environment
   - Add each plan ID as a separate environment variable
   - Example: `RAZORPAY_PLAN_WEEK=plan_xxxxxxxxxxxxx`

**Note:** The script checks for existing plans and skips creation if they already exist.

**Alternative: Create Plans Manually**
1. Go to Razorpay Dashboard → Subscriptions → Plans
2. Create these plans:
   - Week Pass: ₹1,299, Weekly, Interval: 1
   - Month: ₹3,499, Monthly, Interval: 1
   - Year: ₹29,999, Yearly, Interval: 1
3. Copy Plan IDs and add to Render environment variables

### 2. Configure Razorpay Webhook

1. Go to Razorpay Dashboard: https://dashboard.razorpay.com
2. Navigate to Settings → Webhooks
3. Add webhook URL: `https://sketch2bim-backend.onrender.com/api/v1/payments/webhook`
4. Select required events:
   - `payment.captured`
   - `subscription.created`
   - `subscription.activated`
   - `subscription.charged`
   - `subscription.cancelled`
   - `subscription.paused`
5. Copy the webhook secret and set `RAZORPAY_WEBHOOK_SECRET` in Render environment variables
6. Test the webhook by making a test payment or subscription

### 3. Database Migrations

**Auto-Migrations (Recommended):**

Database migrations now run automatically on application startup. The application will:
- Run `alembic upgrade head` automatically when the backend starts
- Log migration status in the startup logs
- Continue to start even if migrations fail (with warnings)

**Verification:**
- Check Render logs after deployment for migration success messages
- Look for: "Database migrations completed successfully" in startup logs
- If migrations fail, you'll see: "Database migration failed" with error details

**Manual Migration Check (Optional):**
```bash
cd backend
python scripts/check_migration_status.py
```

**Manual Migration (If Needed):**
If auto-migrations are disabled or you need to run migrations manually:
```bash
cd backend
alembic upgrade head
```

**Disable Auto-Migrations:**
Set `AUTO_RUN_MIGRATIONS=false` in Render environment variables to disable automatic migrations.

### 4. Verify Render Deployment
- Check Render dashboard: https://dashboard.render.com
- Verify service is running
- Check health endpoint: `GET https://sketch2bim-backend.onrender.com/health`
- Review logs for errors

### 5. Verify Vercel Deployment
- Check Vercel dashboard: https://vercel.com/kvshvl/sketch2bim
- Verify latest deployment is successful
- Check build logs for errors

## Post-Deployment Verification

### 1. Test Authentication
- Visit https://sketch2bim.kvshvl.in
- Click "Sign in with Google"
- Verify OAuth flow works
- Check user is created in database

### 2. Test Upload & Processing
- Upload a test sketch
- Monitor job status
- Verify IFC file is generated
- Test download links

### 3. Test Payment Flow
- Go to pricing page
- Click "Upgrade to Pro" or "Upgrade to Studio"
- Complete test payment (use Razorpay test mode or small live amount)
- Verify webhook receives event
- Verify credits are allocated

### 4. Test IFC Viewer
- Open a completed job
- Verify IFC file loads
- Test view controls (rotate, zoom, pan)
- Test orthographic/perspective toggle

## Monitoring

### Error Logging
- Client errors are logged via the in-app logger (see browser console in development)
- In production, client errors can post to `/api/logs/client-error` (configure alerts if backend endpoint is enabled)
- Backend errors are recorded in Render logs (Loguru)

### Render Logs
- Monitor backend logs in Render dashboard
- Check for database connection issues
- Monitor processing times

### Vercel Analytics
- Check deployment status
- Monitor build times
- Review error logs

## Troubleshooting

### Database Connection Issues
- Verify `DATABASE_URL` uses Supabase pooler (port 6543)
- Check database is accessible from Render
- Verify password is correct

### Database Migration Issues
- Check Render logs for migration errors during startup
- Verify `AUTO_RUN_MIGRATIONS` is not set to `false` (if you want auto-migrations)
- Run `python backend/scripts/check_migration_status.py` to check current migration status
- If migrations fail, check database connectivity and permissions
- Manual migration: `cd backend && alembic upgrade head`

### Redis Connection Issues
- Verify `REDIS_URL` is correct
- Check Upstash dashboard
- Test connection manually

### Razorpay Webhook Issues
- Verify webhook endpoint is configured in Razorpay dashboard
- Check `RAZORPAY_WEBHOOK_SECRET` matches Razorpay
- Verify webhook URL: `https://sketch2bim-backend.onrender.com/api/v1/payments/webhook`
- Ensure `payment.captured` event is selected in Razorpay dashboard
- Check Render logs for webhook signature verification errors

### CORS Issues
- Verify `ALLOWED_ORIGINS` includes frontend URL
- Check browser console for CORS errors
- Verify frontend URL matches exactly

## Rollback Procedure

### Vercel
1. Go to deployment history
2. Find previous working deployment
3. Click "Promote to Production"

### Render
1. Go to service dashboard
2. Click "Manual Deploy"
3. Select previous deployment

## Support

For issues:
- Check logs in Render/Vercel dashboards
- Review client console output (or `/api/logs/client-error` if enabled)
- Check database migration status
- Verify all environment variables are set

## Related Documentation

- **[Production Verification Checklist](./production_verification.md)** - Comprehensive production verification guide
- **[Troubleshooting Guide](./TROUBLESHOOTING.md)** - Common issues and solutions
- **[README](../README.md)** - Project overview and setup

