# Troubleshooting Guide

Common production issues and solutions for Sketch-to-BIM deployment.

## Table of Contents

- [Database Issues](#database-issues)
- [Migration Problems](#migration-problems)
- [Razorpay Webhook Issues](#razorpay-webhook-issues)
- [Environment Variable Issues](#environment-variable-issues)
- [Deployment Errors](#deployment-errors)
- [Authentication Issues](#authentication-issues)
- [Processing Failures](#processing-failures)

---

## Database Issues

### Database Connection Failures

**Symptoms:**
- Application fails to start
- Errors like "could not connect to server" or "connection refused"
- 500 errors on API endpoints

**Solutions:**
1. Verify `DATABASE_URL` is correct in Render environment variables
2. Check if using Supabase pooler (port 6543) for connection pooling
3. Verify database credentials are correct
4. Check if database is accessible from Render's network
5. Verify database is not paused (Supabase free tier pauses after inactivity)
6. Check database connection limits haven't been exceeded

**Debug Steps:**
```bash
# Test database connection locally
psql $DATABASE_URL

# Check connection from Render logs
# Look for connection errors in startup logs
```

### Database Migration Issues

**Symptoms:**
- Migrations fail during startup
- Database schema is out of date
- Errors about missing tables or columns

**Solutions:**
1. Check Render logs for migration errors during startup
2. Verify `AUTO_RUN_MIGRATIONS` is not set to `false` (if you want auto-migrations)
3. Run migration status check:
   ```bash
   cd backend
   python scripts/check_migration_status.py
   ```
4. If migrations fail, check database connectivity and permissions
5. Manual migration:
   ```bash
   cd backend
   alembic upgrade head
   ```
6. If migration conflicts occur, check for multiple migration heads:
   ```bash
   alembic heads
   ```

**Common Migration Errors:**
- **"Target database is not up to date"**: Run `alembic upgrade head`
- **"Can't locate revision identified by"**: Check migration files exist in `backend/alembic/versions/`
- **"Table already exists"**: May need to drop and recreate, or check migration history

---

## Migration Problems

### Auto-Migrations Not Running

**Symptoms:**
- No migration messages in startup logs
- Database schema is outdated

**Solutions:**
1. Check if `AUTO_RUN_MIGRATIONS=false` is set in environment variables
2. Verify `run_migrations()` is called in `backend/app/main.py` lifespan function
3. Check Render logs for migration-related messages
4. Look for "Running database migrations..." in startup logs

### Migration Failures

**Symptoms:**
- "Failed to run database migrations" in logs
- Application starts but database schema is wrong

**Solutions:**
1. Check migration error details in Render logs
2. Verify database permissions allow schema changes
3. Check if migration files are present in repository
4. Test migrations locally first:
   ```bash
   cd backend
   alembic upgrade head
   ```
5. If specific migration fails, check migration file for errors
6. Consider rolling back problematic migration:
   ```bash
   alembic downgrade -1
   ```

---

## Razorpay Webhook Issues

### Webhook Not Receiving Events

**Symptoms:**
- Payments complete but credits not allocated
- Subscriptions created but not activated
- No webhook events in backend logs

**Solutions:**
1. Verify webhook URL is correct in Razorpay dashboard:
   - Should be: `https://sketch2bim-backend.onrender.com/api/v1/payments/webhook`
2. Check webhook is enabled in Razorpay dashboard
3. Verify required events are selected:
   - `payment.captured`
   - `subscription.created`
   - `subscription.activated`
   - `subscription.charged`
   - `subscription.cancelled`
   - `subscription.paused`
4. Test webhook manually from Razorpay dashboard
5. Check Render logs for webhook requests (may be filtered)
6. Verify `RAZORPAY_WEBHOOK_SECRET` matches Razorpay dashboard

### Webhook Signature Verification Failed

**Symptoms:**
- "Webhook signature verification failed" errors in logs
- Webhook events received but rejected

**Solutions:**
1. Verify `RAZORPAY_WEBHOOK_SECRET` matches the secret from Razorpay dashboard
2. Check secret is copied correctly (no extra spaces or newlines)
3. Verify webhook secret is set in Render environment variables
4. Test webhook with correct secret from Razorpay dashboard

### Subscription Plans Not Found

**Symptoms:**
- "Plan not found" errors when creating subscriptions
- Subscription creation fails

**Solutions:**
1. Run plan creation script:
   ```bash
   python scripts/create_razorpay_plans.py
   ```
2. Verify plan IDs are set in Render environment variables:
   - `RAZORPAY_PLAN_WEEK`
   - `RAZORPAY_PLAN_MONTH`
   - `RAZORPAY_PLAN_YEAR`
3. Check plan IDs match Razorpay dashboard
4. Verify plans are active in Razorpay dashboard

---

## Environment Variable Issues

### Missing Environment Variables

**Symptoms:**
- Application fails to start
- "Required environment variable not set" errors
- Features not working (payments, storage, etc.)

**Solutions:**
1. Check `docs/deployment_checklist.md` for required variables
2. Verify all variables are set in Render/Vercel dashboards
3. Check variable names match exactly (case-sensitive)
4. Verify no typos in variable names
5. Check for missing quotes or special characters

### Incorrect Environment Variables

**Symptoms:**
- Features partially work but fail in specific scenarios
- Authentication issues
- Payment processing failures

**Solutions:**
1. Verify `AUTH_URL` matches frontend URL exactly (for OAuth callbacks)
2. Check `FRONTEND_URL` matches frontend deployment URL
3. Verify `ALLOWED_ORIGINS` includes frontend URL
4. Check Razorpay keys are from correct environment (test vs live)
5. Verify database URL format is correct

**Common Issues:**
- **OAuth not working**: Check `AUTH_URL` matches frontend URL exactly
- **CORS errors**: Verify `ALLOWED_ORIGINS` includes frontend URL
- **Payment failures**: Check Razorpay keys are correct (test vs live mode)

---

## Deployment Errors

### Render Deployment Fails

**Symptoms:**
- Build fails
- Service won't start
- Deployment stuck in "Building" or "Deploying"

**Solutions:**
1. Check build logs in Render dashboard
2. Verify `requirements.txt` is up to date
3. Check for Python version compatibility issues
4. Verify all dependencies are listed in `requirements.txt`
5. Check for syntax errors in code
6. Verify Dockerfile (if using) is correct

### Vercel Build Fails

**Symptoms:**
- Frontend build fails
- TypeScript errors
- Missing dependencies

**Solutions:**
1. Check build logs in Vercel dashboard
2. Verify `package.json` dependencies are correct
3. Check for TypeScript errors locally:
   ```bash
   cd frontend
   npm run build
   ```
4. Verify environment variables are set in Vercel
5. Check for missing environment variables referenced in code

---

## Authentication Issues

### OAuth Sign-In Not Working

**Symptoms:**
- "Sign in with Google" button doesn't work
- Redirect loops
- Authentication errors

**Solutions:**
1. Verify `AUTH_URL` matches frontend URL exactly:
   - Production: `https://sketch2bim.kvshvl.in`
   - No trailing slashes
2. Check Google OAuth credentials are correct:
   - `SKETCH2BIM_GOOGLE_CLIENT_ID`
   - `SKETCH2BIM_GOOGLE_SECRET`
3. Verify OAuth redirect URI in Google Console matches:
   - `https://sketch2bim.kvshvl.in/api/auth/callback/google`
4. Check `AUTH_SECRET` is set and matches between frontend and backend
5. Verify `NEXTAUTH_SECRET` matches `AUTH_SECRET`

### Session Not Persisting

**Symptoms:**
- Users logged out frequently
- Session expires too quickly

**Solutions:**
1. Check `AUTH_SECRET` is set correctly
2. Verify cookies are being set (check browser dev tools)
3. Check for CORS issues preventing cookie setting
4. Verify `AUTH_URL` is correct

---

## Processing Failures

### Job Processing Fails

**Symptoms:**
- Jobs stuck in "processing" status
- Jobs fail with errors
- No IFC files generated

**Solutions:**
1. Check Render logs for processing errors
2. Verify BunnyCDN credentials are correct:
   - `BUNNY_STORAGE_ZONE`
   - `BUNNY_ACCESS_KEY`
   - `BUNNY_CDN_HOSTNAME`
3. Check if processing dependencies are installed
4. Verify file upload limits are not exceeded
5. Check for memory or timeout issues in logs

### File Upload Issues

**Symptoms:**
- Uploads fail
- "File too large" errors
- Timeout errors

**Solutions:**
1. Check file size limits in backend configuration
2. Verify request timeout settings
3. Check BunnyCDN storage limits
4. Verify file format is supported (PNG, JPG, PDF)

---

## General Debugging Tips

### Check Logs

**Render:**
- Go to Render dashboard → Your service → Logs
- Filter by error level or search for specific errors
- Check startup logs for initialization issues

**Vercel:**
- Go to Vercel dashboard → Your project → Deployments → Logs
- Check build logs for build-time errors
- Check function logs for runtime errors

### Test Locally

Before deploying, test changes locally:
```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

### Verify Health Endpoints

Check application health:
- Backend: `GET https://sketch2bim-backend.onrender.com/health`
- Should return: `{"status": "healthy", "environment": "production"}`

---

## Getting Help

If issues persist:
1. Check all logs (Render, Vercel, browser console)
2. Verify all environment variables are set correctly
3. Test locally to isolate deployment vs code issues
4. Check migration status: `python backend/scripts/check_migration_status.py`
5. Review recent changes in git history

For specific issues:
- Database: Check Supabase dashboard and connection settings
- Payments: Check Razorpay dashboard and webhook configuration
- Storage: Check BunnyCDN dashboard and credentials

