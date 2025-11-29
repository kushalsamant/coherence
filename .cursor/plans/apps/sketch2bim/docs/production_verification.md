# Production Verification Checklist

This document provides a comprehensive checklist for verifying that the Sketch-to-BIM application is properly configured and functioning in production.

## 1. Environment Variables Verification

### Frontend (Vercel)
**Location**: https://vercel.com/kvshvl/sketch2bim/settings/environment-variables

**Required Variables:**
- [ ] `SKETCH2BIM_GOOGLE_CLIENT_ID` - Google OAuth Client ID
- [ ] `SKETCH2BIM_GOOGLE_SECRET` - Google OAuth Client Secret
- [ ] `AUTH_SECRET` - NextAuth secret key
- [ ] `AUTH_URL` - Frontend URL (must match exactly, no trailing slash)
- [ ] `NEXT_PUBLIC_API_URL` - Backend API URL
- [ ] `NEXT_PUBLIC_FREE_LIMIT` - Free tier limit (default: 5)

**Verification Steps:**
1. Navigate to Vercel dashboard → Project Settings → Environment Variables
2. Verify all variables are present and have correct values
3. Ensure `AUTH_URL` matches your frontend URL exactly: `https://sketch2bim.kvshvl.in`
4. Verify `NEXT_PUBLIC_API_URL` points to backend: `https://sketch2bim-backend.onrender.com`

### Backend (Render)
**Location**: https://dashboard.render.com/web/srv-xxx/env

**Critical Variables:**
- [ ] `SKETCH2BIM_RAZORPAY_KEY_ID` / `RAZORPAY_KEY_ID` (deprecated) - Razorpay API Key ID (prefixed version required)
- [ ] `SKETCH2BIM_RAZORPAY_KEY_SECRET` / `RAZORPAY_KEY_SECRET` (deprecated) - Razorpay API Key Secret (prefixed version required)
- [ ] `SKETCH2BIM_RAZORPAY_WEBHOOK_SECRET` / `RAZORPAY_WEBHOOK_SECRET` (deprecated) - Razorpay webhook secret (from dashboard, prefixed version required)
- [ ] `SKETCH2BIM_RAZORPAY_PLAN_WEEK` / `RAZORPAY_PLAN_WEEK` (deprecated) - Week Pass subscription plan ID (prefixed version required)
- [ ] `SKETCH2BIM_RAZORPAY_PLAN_MONTH` / `RAZORPAY_PLAN_MONTH` (deprecated) - Month subscription plan ID (prefixed version required)
- [ ] `SKETCH2BIM_RAZORPAY_PLAN_YEAR` / `RAZORPAY_PLAN_YEAR` (deprecated) - Year subscription plan ID (prefixed version required)

**Database & Storage:**
- [ ] `SKETCH2BIM_DATABASE_URL` / `DATABASE_URL` (deprecated) - PostgreSQL connection string (Supabase, prefixed version required)
- [ ] `SKETCH2BIM_REDIS_URL` / `REDIS_URL` (deprecated) - Redis connection string (Upstash, prefixed version required)
- [ ] `SKETCH2BIM_BUNNY_ACCESS_KEY` / `BUNNY_ACCESS_KEY` (deprecated) - BunnyCDN access key (prefixed version required)
- [ ] `SKETCH2BIM_BUNNY_CDN_HOSTNAME` / `BUNNY_CDN_HOSTNAME` (deprecated) - BunnyCDN hostname (prefixed version required)
- [ ] `BUNNY_REGION` - BunnyCDN region
- [ ] `BUNNY_STORAGE_ZONE` - BunnyCDN storage zone name

**Application Configuration:**
- [ ] `ALLOWED_ORIGINS` - Frontend URL for CORS
- [ ] `FRONTEND_URL` - Frontend URL
- [ ] `APP_ENV=production`
- [ ] `SECRET_KEY` - Application secret key
- [ ] `NEXTAUTH_SECRET` - NextAuth secret (should match frontend)

**Verification Steps:**
1. Navigate to Render dashboard → Your service → Environment
2. Verify all variables are set (no empty values)
3. Check that `RAZORPAY_WEBHOOK_SECRET` matches the value from Razorpay dashboard
4. Verify all three Razorpay plan IDs are set (not empty or placeholder values)
5. Ensure `DATABASE_URL` uses Supabase pooler (port 6543)
6. Verify `ALLOWED_ORIGINS` and `FRONTEND_URL` match frontend URL

## 2. Service Health Checks

### Backend Health Endpoint
**URL**: `GET https://sketch2bim-backend.onrender.com/health`

**Verification:**
- [ ] Endpoint returns `200 OK` status
- [ ] Response includes service status
- [ ] Response time is acceptable (< 2 seconds)

**Test Command:**
```bash
curl https://sketch2bim-backend.onrender.com/health
```

### Frontend Deployment Status
**Location**: https://vercel.com/kvshvl/sketch2bim

**Verification:**
- [ ] Latest deployment is successful (green status)
- [ ] No build errors in deployment logs
- [ ] Frontend is accessible at https://sketch2bim.kvshvl.in
- [ ] No console errors on page load

### Database Connectivity
**Verification:**
- [ ] Backend can connect to database (check Render logs)
- [ ] No connection timeout errors
- [ ] Database queries execute successfully
- [ ] Connection pool is working (Supabase pooler)

**Check Render Logs For:**
- "Database connection established"
- No "connection refused" or "timeout" errors
- Successful query execution

### Redis Connectivity
**Verification:**
- [ ] Backend can connect to Redis (check Render logs)
- [ ] No connection errors in startup logs
- [ ] Session storage is working (test login/logout)

**Check Render Logs For:**
- "Redis connection established"
- No Redis connection errors

### Storage (BunnyCDN) Accessibility
**Verification:**
- [ ] Files can be uploaded to BunnyCDN
- [ ] Files can be downloaded from BunnyCDN
- [ ] CDN hostname is accessible
- [ ] Access key has correct permissions

**Test:**
1. Upload a test sketch through the application
2. Verify file appears in BunnyCDN dashboard
3. Verify download links work

## 3. Razorpay Configuration

### Webhook Configuration
**Location**: Razorpay Dashboard → Settings → Webhooks

**Webhook URL**: `https://sketch2bim-backend.onrender.com/api/v1/payments/webhook`

**Verification Checklist:**
- [ ] Webhook URL is configured in Razorpay dashboard
- [ ] Webhook URL matches exactly (no trailing slash)
- [ ] Webhook secret is copied and set in Render as `RAZORPAY_WEBHOOK_SECRET`
- [ ] Webhook secret in Render matches Razorpay dashboard

**Required Webhook Events:**
- [ ] `payment.captured` - For one-time payments
- [ ] `subscription.created` - For subscription creation
- [ ] `subscription.activated` - For subscription activation
- [ ] `subscription.charged` - For subscription charges
- [ ] `subscription.cancelled` - For subscription cancellation
- [ ] `subscription.paused` - For subscription pausing

**Test Webhook:**
1. Make a test payment or subscription
2. Check Render logs for webhook reception
3. Verify webhook signature validation passes
4. Verify payment/subscription is processed correctly

### Subscription Plans
**Location**: Razorpay Dashboard → Subscriptions → Plans

**Required Plans:**
- [ ] **Week Pass**: ₹1,299, Weekly, Interval: 1
- [ ] **Month**: ₹3,499, Monthly, Interval: 1
- [ ] **Year**: ₹29,999, Yearly, Interval: 1

**Plan ID Verification:**
- [ ] `SKETCH2BIM_RAZORPAY_PLAN_WEEK` / `RAZORPAY_PLAN_WEEK` (deprecated) - Plan ID from Razorpay dashboard (prefixed version required)
- [ ] `SKETCH2BIM_RAZORPAY_PLAN_MONTH` / `RAZORPAY_PLAN_MONTH` (deprecated) - Plan ID from Razorpay dashboard (prefixed version required)
- [ ] `SKETCH2BIM_RAZORPAY_PLAN_YEAR` / `RAZORPAY_PLAN_YEAR` (deprecated) - Plan ID from Razorpay dashboard (prefixed version required)

**Verification Steps:**
1. Go to Razorpay Dashboard → Subscriptions → Plans
2. Verify all 3 plans exist
3. Copy Plan IDs from each plan
4. Verify Plan IDs are set in Render environment variables
5. Ensure Plan IDs are not empty or placeholder values

**Alternative: Create Plans via Script**
```bash
cd backend
python scripts/create_razorpay_plans.py
```
The script will output Plan IDs that need to be added to Render environment variables.

## 4. Database Migrations

### Auto-Migrations Status
**Verification:**
- [ ] Auto-migrations are enabled (default behavior)
- [ ] Check Render logs after deployment for migration messages
- [ ] Look for: "Database migrations completed successfully"
- [ ] No migration errors in startup logs

**If Auto-Migrations Fail:**
- Check Render logs for error details
- Verify database connectivity
- Check database permissions
- Run manual migration if needed

### Manual Migration Check
**Command:**
```bash
cd backend
python scripts/check_migration_status.py
```

**Verification:**
- [ ] Script runs without errors
- [ ] No pending migrations
- [ ] All tables exist in database
- [ ] Migration version matches expected version

### Verify All Tables Exist
**Required Tables:**
- [ ] `users` - User accounts
- [ ] `jobs` - Processing jobs
- [ ] `payments` - Payment records
- [ ] `subscriptions` - Subscription records
- [ ] `alembic_version` - Migration version tracking

**Check via Database Client:**
1. Connect to Supabase database
2. Verify all tables are present
3. Check table schemas match expected structure

## 5. End-to-End Testing

### User Authentication Flow
**Test Steps:**
1. Visit https://sketch2bim.kvshvl.in
2. Click "Sign in with Google"
3. Complete OAuth flow
4. Verify user is redirected back to application
5. Verify user is logged in
6. Check user is created in database

**Verification:**
- [ ] OAuth redirect works correctly
- [ ] User session is created
- [ ] User data is stored in database
- [ ] User can access protected routes
- [ ] Logout functionality works

### Sketch Upload and Processing
**Test Steps:**
1. Log in to application
2. Upload a test sketch (PNG/JPG)
3. Monitor job status updates
4. Wait for processing to complete
5. Verify job status changes to "completed"

**Verification:**
- [ ] File upload succeeds
- [ ] Job is created in database
- [ ] Processing starts (check backend logs)
- [ ] Progress updates are received
- [ ] IFC file is generated
- [ ] Job status updates to "completed"
- [ ] Download links are available

### Payment Flow (Test Mode)
**Test Steps:**
1. Navigate to pricing page
2. Click "Upgrade to Pro" or "Upgrade to Studio"
3. Select a subscription plan
4. Complete payment in Razorpay test mode
5. Verify payment is processed

**Verification:**
- [ ] Payment page loads correctly
- [ ] Razorpay payment gateway opens
- [ ] Test payment succeeds
- [ ] Payment webhook is received (check Render logs)
- [ ] Credits are allocated to user account
- [ ] Subscription is created (if applicable)
- [ ] User subscription status updates

### Webhook Reception
**Verification:**
- [ ] Webhook endpoint is accessible
- [ ] Webhook signature validation works
- [ ] Payment events are processed correctly
- [ ] Subscription events are processed correctly
- [ ] No webhook errors in Render logs

**Check Render Logs For:**
- Webhook requests received
- Signature validation success
- Payment/subscription processing
- No authentication errors

### File Download
**Test Steps:**
1. Open a completed job
2. Click download links for IFC, CSV, Excel files
3. Verify files download correctly

**Verification:**
- [ ] IFC file downloads successfully
- [ ] CSV export downloads successfully
- [ ] Excel export downloads successfully
- [ ] Files are not corrupted
- [ ] File sizes are reasonable

### IFC Viewer Functionality
**Test Steps:**
1. Open a completed job with IFC file
2. Wait for IFC viewer to load
3. Test view controls

**Verification:**
- [ ] IFC file loads in viewer
- [ ] 3D model renders correctly
- [ ] Rotate control works (left click + drag)
- [ ] Pan control works (right click + drag)
- [ ] Zoom control works (scroll)
- [ ] View mode switching works (3D, Plan, Section, Elevation)
- [ ] Orthographic/perspective toggle works
- [ ] Object tree displays correctly
- [ ] Object selection works
- [ ] Focus on selected object works (camera animates to object)
- [ ] Property panel displays when object is selected
- [ ] Measurement tool works
- [ ] Section planes work

## 6. Advanced Features Testing

### Batch Upload
**Test Steps:**
1. Log in to application
2. Navigate to upload page (or use API)
3. Upload multiple sketches (3-5 files) simultaneously
4. Monitor batch processing status

**Verification:**
- [ ] Batch upload endpoint accepts multiple files
- [ ] All files are validated before processing
- [ ] Jobs are created for each file with same batch_id
- [ ] Partial failures are handled gracefully (some files fail, others succeed)
- [ ] Error messages are clear for failed files
- [ ] Successful files proceed to processing
- [ ] Batch status can be queried

**Test Command:**
```bash
curl -X POST https://sketch2bim-backend.onrender.com/api/v1/generate/batch-upload \
  -H "Authorization: Bearer <token>" \
  -F "files=@sketch1.png" \
  -F "files=@sketch2.png" \
  -F "files=@sketch3.png" \
  -F "project_type=architecture"
```

### Layout Variations
**Test Steps:**
1. Complete a job (wait for processing to finish)
2. Navigate to job details page
3. Generate layout variations (2-3 variations)
4. Wait for variation processing
5. View and compare variations

**Verification:**
- [ ] Variations endpoint is accessible
- [ ] Variations are generated from completed jobs only
- [ ] Each variation has unique plan_data
- [ ] IFC files are generated for each variation
- [ ] Variations can be listed and retrieved individually
- [ ] Variations can be deleted
- [ ] Variation confidence scores are reasonable

**Test Command:**
```bash
curl -X POST https://sketch2bim-backend.onrender.com/api/v1/variations/jobs/{job_id}/variations \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"num_variations": 3}'
```

**Known Limitations:**
- Variation quality depends on original sketch complexity
- Simple algorithms may produce similar variations
- Works best with clear room boundaries

### Iterations
**Test Steps:**
1. Complete a job
2. Create an iteration from the job
3. Apply changes (move elements, resize rooms)
4. Regenerate IFC with changes
5. Create child iteration from parent iteration
6. List all iterations for a job

**Verification:**
- [ ] Iterations can be created from completed jobs
- [ ] Iterations can have parent-child relationships
- [ ] Changes are applied to plan_data correctly
- [ ] IFC files are regenerated with changes
- [ ] Iterations can be updated (name, notes, changes)
- [ ] Iterations can be listed and retrieved
- [ ] Iterations with children cannot be deleted
- [ ] Change summaries are generated correctly

**Test Command:**
```bash
curl -X POST https://sketch2bim-backend.onrender.com/api/v1/iterations/jobs/{job_id}/iterations \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Modified Layout",
    "changes_json": {
      "moved_elements": [{"element_id": "wall1", "element_type": "wall", "position": {"start": [0,0], "end": [100,0]}}],
      "resized_rooms": [{"room_id": "room1", "size": 6000}]
    }
  }'
```

**Known Limitations:**
- Change application logic is simplified
- Complex geometric transformations may not be fully supported
- Room resizing uses proportional scaling

## 7. Monitoring Setup

### Render Logs
**Location**: https://dashboard.render.com

**Verification:**
- [ ] Logs are accessible in Render dashboard
- [ ] Logs show application startup
- [ ] No critical errors in logs
- [ ] Database connection logs are present
- [ ] Migration logs are present (if applicable)
- [ ] Webhook reception logs are visible

**Monitor For:**
- Application errors
- Database connection issues
- Webhook processing errors
- Payment processing errors
- High response times

### Vercel Logs
**Location**: https://vercel.com/kvshvl/sketch2bim

**Verification:**
- [ ] Deployment logs are accessible
- [ ] Build logs show no errors
- [ ] Runtime logs are available (if applicable)
- [ ] No build failures

**Monitor For:**
- Build errors
- Runtime errors
- Deployment failures

### Error Tracking
**Verification:**
- [ ] Client errors are logged (browser console or backend endpoint)
- [ ] Backend errors are logged (Render logs)
- [ ] Error tracking service is configured (if applicable)

**Check:**
- Browser console for client-side errors
- Render logs for backend errors
- `/api/logs/client-error` endpoint (if enabled)

### Health Check Monitoring
**Verification:**
- [ ] Health endpoint is monitored (if monitoring service is configured)
- [ ] Alerts are set up for health check failures (if applicable)
- [ ] Uptime monitoring is configured (if applicable)

## 8. Verification Summary

After completing all checks above, document:

- **Date of Verification**: ___________
- **Verified By**: ___________
- **Overall Status**: [ ] Pass [ ] Fail [ ] Partial

**Issues Found:**
(List any issues discovered during verification)

**Action Items:**
(List any follow-up actions needed)

---

## Quick Reference

- **Frontend URL**: https://sketch2bim.kvshvl.in
- **Backend URL**: https://sketch2bim-backend.onrender.com
- **Health Endpoint**: https://sketch2bim-backend.onrender.com/health
- **Webhook Endpoint**: https://sketch2bim-backend.onrender.com/api/v1/payments/webhook
- **Razorpay Dashboard**: https://dashboard.razorpay.com
- **Vercel Dashboard**: https://vercel.com/kvshvl/sketch2bim
- **Render Dashboard**: https://dashboard.render.com

## Related Documentation

- [Deployment Checklist](./deployment_checklist.md) - Detailed deployment instructions
- [Troubleshooting Guide](./TROUBLESHOOTING.md) - Common issues and solutions
- [README](../README.md) - Project overview and setup

