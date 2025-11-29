# Infrastructure Consolidation - Remaining Implementation Tasks

## Overview

This plan documents all remaining manual configuration tasks required to complete the infrastructure consolidation. All code changes have been completed and pushed to the repository. The remaining work involves manual configuration in Render dashboard to deploy the three backend services without using the Blueprint method.

**Status:** Code changes ✅ Complete | Manual configuration ⏳ Pending

---

## Completed Work

### ✅ Code Changes (All Complete)

1. **Centralized Authentication**
   - Main site (`kvshvl.in`) configured with NextAuth for Google OAuth
   - All apps redirect to `https://kvshvl.in/api/auth/callback/google`
   - Removed app-specific OAuth credentials from all `.env.production` files
   - Added `NEXT_PUBLIC_AUTH_URL=https://kvshvl.in` to all frontend configs

2. **Redis Consolidation**
   - Migrated Sketch2BIM from Render Redis to Upstash Redis (REST API)
   - Reframe already using Upstash Redis
   - Removed `sketch2bim-redis` service from `render.yaml`
   - Created `RedisService` for Sketch2BIM using Upstash REST API

3. **Shared Backend Packaging**
   - Removed `packages/shared-backend/pyproject.toml` (Poetry)
   - Using `setup.py` (setuptools) for pip installation
   - Fixed build errors on Render

4. **Docker Deployment Removal**
   - Deleted `apps/sketch2bim/backend/Dockerfile`
   - Deleted `apps/sketch2bim/frontend/Dockerfile`
   - Deleted `apps/sketch2bim/infra/docker-compose.yml`
   - Deleted `apps/sketch2bim/infra/docker-compose.prod.yml`
   - Updated documentation to reflect Render Python Web Services only

5. **Environment Files**
   - All `.env.production` files cleaned and verified
   - All required values present (except placeholders for Supabase URLs)
   - PowerShell verification script created

6. **Documentation**
   - `DEPLOYMENT_CONFIGURATION_GUIDE.md` created
   - `INFRASTRUCTURE_CONSOLIDATION_STATUS.md` created
   - Verification scripts created
   - README files updated

---

## Remaining Tasks

### Part 1: Render - Manual Web Service Configuration

**Important:** We are NOT using Render Blueprint (`render.yaml`) for deployment. Instead, we're creating three independent Web Services manually via the Render dashboard.

#### 1.1 ASK Backend Service (`ask-backend`)

**Steps:**

1. **Create Service**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click **New +** → **Web Service**
   - Connect GitHub repository: `kushalsamant/kushalsamant.github.io`
   - Select the repository when prompted

2. **Configure Service Settings**
   - **Name:** `ask-backend`
   - **Root Directory:** `apps/ask`
   - **Environment:** Python
   - **Python Version:** 3.13 (or latest available)
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
   - **Health Check Path:** `/health`

3. **Set Environment Variables**
   Go to the service → **Environment** tab and add all variables from `ask.env.production` (backend section):

   **Required Variables:**
   - `ASK_DATABASE_URL` - Supabase PostgreSQL connection string (pooler, port 6543)
     - Format: `postgresql://postgres.[PROJECT_REF]:[PASSWORD]@aws-[REGION].pooler.supabase.com:6543/postgres`
     - Get from: Supabase Dashboard → Project Settings → Database → Connection Pooling
   - `ASK_GROQ_API_KEY` - Your Groq API key
   - `ASK_RAZORPAY_KEY_ID` - `rzp_live_RhNUuWRBG7lzR4`
   - `ASK_RAZORPAY_KEY_SECRET` - `7T1MCu1xNjX9G4soT7kuqqdB`
   - `ASK_RAZORPAY_WEBHOOK_SECRET` - `bbzTiAtV2LWSt4J`

   **Auto-Configured Variables (verify these are set):**
   - `ASK_API_HOST` = `0.0.0.0`
   - `ASK_API_PORT` = `8000`
   - `ASK_APP_NAME` = `ASK: Daily Research`
   - `ASK_CORS_ORIGINS` = `https://ask.kvshvl.in,https://www.ask.kvshvl.in`
   - `ASK_DEBUG` = `false`
   - `ASK_ENVIRONMENT` = `production`
   - `ASK_FRONTEND_URL` = `https://ask.kvshvl.in`
   - `ASK_LOG_CSV_FILE` = `log.csv`
   - `ASK_LOG_DIR` = `logs`
   - `ASK_LOG_LEVEL` = `INFO`
   - `ASK_PYTHONPATH` = `.`
   - `ASK_JWT_ALGORITHM` = `HS256`
   - `ASK_DATABASE_SCHEMA` = `ask_schema`
   - `RAZORPAY_WEEK_AMOUNT` = `129900`
   - `RAZORPAY_MONTH_AMOUNT` = `349900`
   - `RAZORPAY_YEAR_AMOUNT` = `2999900`
   - `ASK_RAZORPAY_PLAN_WEEK` = `plan_Rha5Ikcm5JrGqx`
   - `ASK_RAZORPAY_PLAN_MONTH` = `plan_Rha5JNPsk1WmI6`
   - `ASK_RAZORPAY_PLAN_YEAR` = `plan_Rha5Jzn1sk8o1X`
   - `ASK_UPSTASH_REDIS_REST_URL` = `https://splendid-platypus-26441.upstash.io`
   - `ASK_UPSTASH_REDIS_REST_TOKEN` = `AWdJAAIncDJjZTMyOGIzZTc3ZmU0MjVhYmZmMDJiODgyYjhlY2NmZHAyMjY0NDE`

4. **Save and Deploy**
   - Click **Save Changes**
   - Render will automatically start building and deploying
   - Wait for status to show **Live** (usually 2-5 minutes)

5. **Verify Deployment**
   - Check service URL (e.g., `https://ask-api.onrender.com`)
   - Test health endpoint: `https://ask-api.onrender.com/health`
   - Should return `{"status": "healthy", "service": "ASK API"}`

---

#### 1.2 Reframe Backend Service (`reframe-backend`)

**Steps:**

1. **Create Service**
   - In Render Dashboard, click **New +** → **Web Service**
   - Connect same repository: `kushalsamant/kushalsamant.github.io`

2. **Configure Service Settings**
   - **Name:** `reframe-backend`
   - **Root Directory:** `apps/reframe/backend` ⚠️ **Important:** Must be `apps/reframe/backend`, NOT `apps/reframe/frontend`
   - **Environment:** Python
   - **Python Version:** 3.13 (or latest available)
   - **Build Command:** `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Health Check Path:** `/health`

3. **Set Environment Variables**
   Go to the service → **Environment** tab and add all variables from `reframe.env.production` (backend section):

   **Required Variables:**
   - `REFRAME_GROQ_API_KEY` - Your Groq API key
   - `REFRAME_UPSTASH_REDIS_REST_URL` - `https://splendid-platypus-26441.upstash.io`
   - `REFRAME_UPSTASH_REDIS_REST_TOKEN` - `AWdJAAIncDJjZTMyOGIzZTc3ZmU0MjVhYmZmMDJiODgyYjhlY2NmZHAyMjY0NDE`
   - `REFRAME_NEXTAUTH_SECRET` - `lFGHiDWlnSC1yn1F95VgqttX0WZ2s4o+Ybsm9ELw564=`
   - `REFRAME_AUTH_SECRET` - `lFGHiDWlnSC1yn1F95VgqttX0WZ2s4o+Ybsm9ELw564=`

   **Auto-Configured Variables (verify these are set):**
   - `REFRAME_APP_NAME` = `Reframe API`
   - `REFRAME_ENVIRONMENT` = `production`
   - `REFRAME_DEBUG` = `false`
   - `REFRAME_CORS_ORIGINS` = `https://reframe.kvshvl.in,https://www.reframe.kvshvl.in`
   - `REFRAME_FREE_LIMIT` = `5`
   - `REFRAME_JWT_ALGORITHM` = `HS256`
   - `REFRAME_GROQ_DAILY_COST_THRESHOLD` = `10.0`
   - `REFRAME_GROQ_MONTHLY_COST_THRESHOLD` = `50.0`

4. **Save and Deploy**
   - Click **Save Changes**
   - Wait for status to show **Live**

5. **Verify Deployment**
   - Test health endpoint: `https://reframe-api.onrender.com/health`
   - Should return healthy status

---

#### 1.3 Sketch2BIM Backend Service (`sketch2bim-backend`)

**Steps:**

1. **Create Service**
   - In Render Dashboard, click **New +** → **Web Service**
   - Connect same repository: `kushalsamant/kushalsamant.github.io`

2. **Configure Service Settings**
   - **Name:** `sketch2bim-backend`
   - **Root Directory:** `apps/sketch2bim/backend` ⚠️ **Important:** Must be `apps/sketch2bim/backend`
   - **Environment:** Python
   - **Python Version:** 3.13 (or latest available)
   - **Build Command:** `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Health Check Path:** `/health`

3. **Set Environment Variables**
   Go to the service → **Environment** tab and add all variables from `sketch2bim.env.production` (backend section):

   **Required Variables:**
   - `SKETCH2BIM_DATABASE_URL` - Supabase PostgreSQL connection string (pooler, port 6543)
     - Format: `postgresql://postgres.[PROJECT_REF]:[PASSWORD]@aws-[REGION].pooler.supabase.com:6543/postgres`
   - `SKETCH2BIM_UPSTASH_REDIS_REST_URL` - `https://splendid-platypus-26441.upstash.io`
   - `SKETCH2BIM_UPSTASH_REDIS_REST_TOKEN` - `AWdJAAIncDJjZTMyOGIzZTc3ZmU0MjVhYmZmMDJiODgyYjhlY2NmZHAyMjY0NDE`
   - `SKETCH2BIM_NEXTAUTH_SECRET` - `lFGHiDWlnSC1yn1F95VgqttX0WZ2s4o+Ybsm9ELw564=`
   - `SKETCH2BIM_SECRET_KEY` - `lFGHiDWlnSC1yn1F95VgqttX0WZ2s4o+Ybsm9ELw564=`

   **Payment Gateway:**
   - `SKETCH2BIM_RAZORPAY_KEY_ID` - `rzp_live_RhNUuWRBG7lzR4`
   - `SKETCH2BIM_RAZORPAY_KEY_SECRET` - `7T1MCu1xNjX9G4soT7kuqqdB`
   - `SKETCH2BIM_RAZORPAY_WEBHOOK_SECRET` - `bbzTiAtV2LWSt4J`
   - `SKETCH2BIM_RAZORPAY_WEEK_AMOUNT` = `129900`
   - `SKETCH2BIM_RAZORPAY_MONTH_AMOUNT` = `349900`
   - `SKETCH2BIM_RAZORPAY_YEAR_AMOUNT` = `2999900`
   - `SKETCH2BIM_RAZORPAY_PLAN_WEEK` = `plan_Rha5Ikcm5JrGqx`
   - `SKETCH2BIM_RAZORPAY_PLAN_MONTH` = `plan_Rha5JNPsk1WmI6`
   - `SKETCH2BIM_RAZORPAY_PLAN_YEAR` = `plan_Rha5Jzn1sk8o1X`

   **BunnyCDN Storage:**
   - `SKETCH2BIM_BUNNY_STORAGE_ZONE` - `kvshvl`
   - `SKETCH2BIM_BUNNY_ACCESS_KEY` - `4026f19d-3836-4442-ba87fe2013c4-4f75-4944`
   - `SKETCH2BIM_BUNNY_CDN_HOSTNAME` - `kvshvl.b-cdn.net`

   **Replicate (if used):**
   - `SKETCH2BIM_REPLICATE_API_KEY` - Your Replicate API key
   - `SKETCH2BIM_REPLICATE_MODEL_ID` - `kushalsamant/sketch2bim-processor`

   **Stripe (if used):**
   - `SKETCH2BIM_STRIPE_PUBLISHABLE_KEY` - `pk_live_2UDHQxbktN5sOx4URR3p2xBr`
   - `SKETCH2BIM_STRIPE_SECRET_KEY` - `sk_live_ywsRrAeVNphfisdV6gICF5Mj00elbZIAEI`
   - `SKETCH2BIM_STRIPE_WEBHOOK_SECRET` - `whsec_dZTUJE7WCxOpz8il6aKSuaKEPxgc9TPQ`

   **Auto-Configured Variables (verify these are set):**
   - `SKETCH2BIM_APP_NAME` = `Sketch-to-BIM`
   - `SKETCH2BIM_APP_ENV` = `production`
   - `SKETCH2BIM_DEBUG` = `false`
   - `SKETCH2BIM_FRONTEND_URL` = `https://sketch2bim.kvshvl.in`
   - `SKETCH2BIM_ALLOWED_ORIGINS` = `https://sketch2bim.kvshvl.in`
   - `SKETCH2BIM_DATABASE_SCHEMA` = `sketch2bim_schema`
   - `SKETCH2BIM_REDIS_LIMIT_COMMANDS_PER_DAY` = `10000`

   **⚠️ CRITICAL:** Do NOT set `SKETCH2BIM_REDIS_URL` - This was for old Render Redis. We're using Upstash Redis REST API now.

4. **Save and Deploy**
   - Click **Save Changes**
   - Wait for status to show **Live**

5. **Verify Deployment**
   - Test health endpoint: `https://sketch2bim-backend.onrender.com/health`
   - Should return healthy status

---

### Part 2: Upstash Redis Verification

**Goal:** Ensure both Reframe and Sketch2BIM backends are using the same Upstash Redis instance.

**Steps:**

1. **Get Upstash Credentials**
   - Go to [Upstash Console](https://console.upstash.com/redis)
   - Select your Redis database
   - Copy:
     - **REST URL:** `https://splendid-platypus-26441.upstash.io` (or your actual URL)
     - **REST TOKEN:** `AWdJAAIncDJjZTMyOGIzZTc3ZmU0MjVhYmZmMDJiODgyYjhlY2NmZHAyMjY0NDE` (or your actual token)

2. **Verify in Render Services**
   - **Reframe Backend:** Check that `REFRAME_UPSTASH_REDIS_REST_URL` and `REFRAME_UPSTASH_REDIS_REST_TOKEN` match your Upstash credentials
   - **Sketch2BIM Backend:** Check that `SKETCH2BIM_UPSTASH_REDIS_REST_URL` and `SKETCH2BIM_UPSTASH_REDIS_REST_TOKEN` match your Upstash credentials
   - Both services should use the **same** Upstash Redis database (shared instance)

---

### Part 3: Supabase Database Configuration

**Goal:** Ensure ASK and Sketch2BIM backends have correct Supabase connection strings.

**Steps:**

1. **Get Supabase Connection Strings**
   - Go to [Supabase Dashboard](https://supabase.com/dashboard)
   - Select your project
   - Go to **Settings** → **Database**
   - Under **Connection Pooling**, copy the connection string
   - Format: `postgresql://postgres.[PROJECT_REF]:[PASSWORD]@aws-[REGION].pooler.supabase.com:6543/postgres`
   - ⚠️ **Important:** Use the **pooler** connection (port 6543), not direct connection

2. **Set in Render Services**
   - **ASK Backend:** Set `ASK_DATABASE_URL` to your Supabase pooler connection string
   - **Sketch2BIM Backend:** Set `SKETCH2BIM_DATABASE_URL` to your Supabase pooler connection string
   - Both use the same Supabase database but different schemas:
     - ASK uses schema: `ask_schema`
     - Sketch2BIM uses schema: `sketch2bim_schema`

---

### Part 4: Testing & Verification

**Goal:** Verify all services are live and working correctly.

#### 4.1 Backend Health Checks

Test each backend health endpoint:

1. **ASK Backend**
   ```bash
   curl https://ask-api.onrender.com/health
   ```
   Expected: `{"status": "healthy", "service": "ASK API"}`

2. **Reframe Backend**
   ```bash
   curl https://reframe-api.onrender.com/health
   ```
   Expected: `{"status": "healthy", "service": "Reframe API"}`

3. **Sketch2BIM Backend**
   ```bash
   curl https://sketch2bim-backend.onrender.com/health
   ```
   Expected: `{"status": "healthy", "service": "Sketch2BIM API"}`

#### 4.2 Authentication Flow Testing

Test that all apps redirect to centralized auth:

1. **ASK App**
   - Visit: `https://ask.kvshvl.in`
   - Click "Sign In"
   - Should redirect to: `https://kvshvl.in/api/auth/signin?app=ask&returnUrl=...`
   - Complete Google OAuth
   - Should redirect back to: `https://ask.kvshvl.in?auth=success`

2. **Reframe App**
   - Visit: `https://reframe.kvshvl.in`
   - Click "Sign In"
   - Should redirect to: `https://kvshvl.in/api/auth/signin?app=reframe&returnUrl=...`
   - Complete Google OAuth
   - Should redirect back to: `https://reframe.kvshvl.in?auth=success`

3. **Sketch2BIM App**
   - Visit: `https://sketch2bim.kvshvl.in`
   - Click "Sign In"
   - Should redirect to: `https://kvshvl.in/api/auth/signin?app=sketch2bim&returnUrl=...`
   - Complete Google OAuth
   - Should redirect back to: `https://sketch2bim.kvshvl.in?auth=success`

4. **Main Site**
   - Visit: `https://kvshvl.in/api/auth/signin`
   - Should redirect to Google OAuth
   - After signing in, should redirect back to: `https://kvshvl.in`

#### 4.3 Backend Functionality Testing

Test core functionality for each app:

1. **ASK**
   - Sign in and perform a feasibility check
   - Verify backend API calls succeed (check browser Network tab)
   - No 5xx errors should appear

2. **Reframe**
   - Sign in and perform a reframe operation
   - Verify backend API calls succeed
   - Check that rate limiting works (Upstash Redis)

3. **Sketch2BIM**
   - Sign in and upload a sketch
   - Verify backend processing starts
   - Check that rate limiting works (Upstash Redis)

#### 4.4 Automated Verification Script

Run the deployment verification script:

```powershell
cd kushalsamant.github.io
.\scripts\verify-deployment.ps1 -Verbose
```

This script checks:
- All backend health endpoints
- Environment file existence
- Provides summary of deployment status

---

## Common Issues & Troubleshooting

### Issue: Service fails to build on Render

**Symptoms:**
- Build logs show errors about `shared-backend` package
- `ModuleOrPackageNotFoundError` or similar

**Solution:**
- Verify `packages/shared-backend/pyproject.toml` is deleted (we're using `setup.py` now)
- Ensure `requirements.txt` has: `-e ../../packages/shared-backend`
- Check that Root Directory is correct (e.g., `apps/reframe/backend`, not `apps/reframe/frontend`)

### Issue: Service shows wrong root directory error

**Symptoms:**
- `Service Root Directory "/opt/render/project/src/apps/reframe/frontend" is missing`

**Solution:**
- For `reframe-backend`: Root Directory must be `apps/reframe/backend` (NOT `apps/reframe/frontend`)
- For `sketch2bim-backend`: Root Directory must be `apps/sketch2bim/backend`
- For `ask-backend`: Root Directory must be `apps/ask`

### Issue: Redis connection errors

**Symptoms:**
- Backend logs show Redis connection failures
- Rate limiting not working

**Solution:**
- Verify Upstash Redis REST URL and TOKEN are set correctly
- Ensure you're using REST API variables (`*_UPSTASH_REDIS_REST_URL`, `*_UPSTASH_REDIS_REST_TOKEN`)
- Do NOT use old `SKETCH2BIM_REDIS_URL` variable
- Check Upstash console to ensure database is active

### Issue: Database connection errors

**Symptoms:**
- Backend logs show PostgreSQL connection failures
- Database queries fail

**Solution:**
- Verify Supabase connection string uses **pooler** (port 6543)
- Format: `postgresql://postgres.[PROJECT_REF]:[PASSWORD]@aws-[REGION].pooler.supabase.com:6543/postgres`
- Check that schema variables are set: `ASK_DATABASE_SCHEMA=ask_schema`, `SKETCH2BIM_DATABASE_SCHEMA=sketch2bim_schema`
- Verify Supabase project is active and database is accessible

### Issue: OAuth redirect fails

**Symptoms:**
- Sign in redirects fail
- Google OAuth errors

**Solution:**
- Verify `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` are set in Vercel (main site project)
- Check Google OAuth Console has redirect URI: `https://kvshvl.in/api/auth/callback/google`
- Verify `NEXT_PUBLIC_AUTH_URL=https://kvshvl.in` is set in all app Vercel projects
- Wait 5-10 minutes after Google OAuth changes for propagation

### Issue: Service shows "Live" but health check fails

**Symptoms:**
- Render dashboard shows service as "Live"
- Health endpoint returns 404 or 500

**Solution:**
- Check Render logs for startup errors
- Verify Start Command is correct: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Check that health endpoint exists in the code (`/health` route)
- Verify all required environment variables are set

---

## Checklist

Use this checklist to track your progress:

### Render Services
- [ ] `ask-backend` service created
- [ ] `ask-backend` environment variables set (from `ask.env.production`)
- [ ] `ask-backend` deployed and showing "Live"
- [ ] `ask-backend` health endpoint responding
- [ ] `reframe-backend` service created
- [ ] `reframe-backend` Root Directory set to `apps/reframe/backend` (NOT frontend)
- [ ] `reframe-backend` environment variables set (from `reframe.env.production`)
- [ ] `reframe-backend` deployed and showing "Live"
- [ ] `reframe-backend` health endpoint responding
- [ ] `sketch2bim-backend` service created
- [ ] `sketch2bim-backend` Root Directory set to `apps/sketch2bim/backend`
- [ ] `sketch2bim-backend` environment variables set (from `sketch2bim.env.production`)
- [ ] `sketch2bim-backend` deployed and showing "Live"
- [ ] `sketch2bim-backend` health endpoint responding
- [ ] All services using correct Python version (3.13 or latest)
- [ ] All services using correct build/start commands

### Upstash Redis
- [ ] Upstash Redis credentials obtained from console
- [ ] `REFRAME_UPSTASH_REDIS_REST_URL` set in Reframe backend
- [ ] `REFRAME_UPSTASH_REDIS_REST_TOKEN` set in Reframe backend
- [ ] `SKETCH2BIM_UPSTASH_REDIS_REST_URL` set in Sketch2BIM backend
- [ ] `SKETCH2BIM_UPSTASH_REDIS_REST_TOKEN` set in Sketch2BIM backend
- [ ] Both services using same Upstash Redis instance
- [ ] `SKETCH2BIM_REDIS_URL` NOT set (old variable removed)

### Supabase Database
- [ ] Supabase pooler connection string obtained
- [ ] `ASK_DATABASE_URL` set in ASK backend (pooler, port 6543)
- [ ] `SKETCH2BIM_DATABASE_URL` set in Sketch2BIM backend (pooler, port 6543)
- [ ] `ASK_DATABASE_SCHEMA=ask_schema` set
- [ ] `SKETCH2BIM_DATABASE_SCHEMA=sketch2bim_schema` set

### Testing
- [ ] All three backend health endpoints responding
- [ ] ASK app authentication flow tested
- [ ] Reframe app authentication flow tested
- [ ] Sketch2BIM app authentication flow tested
- [ ] Main site authentication flow tested
- [ ] ASK backend functionality tested (feasibility check works)
- [ ] Reframe backend functionality tested (reframe operation works)
- [ ] Sketch2BIM backend functionality tested (upload/processing works)
- [ ] Verification script run successfully

---

## Expected Final State

After completing all tasks:

- ✅ All three backend services running on Render as Python Web Services
- ✅ All services showing "Live" status in Render dashboard
- ✅ All health endpoints responding with 200 OK
- ✅ All authentication flows working through centralized `kvshvl.in` endpoint
- ✅ All apps successfully calling their respective backends
- ✅ Upstash Redis working for rate limiting (Reframe + Sketch2BIM)
- ✅ Supabase PostgreSQL working for data storage (ASK + Sketch2BIM)
- ✅ No Docker-related build errors
- ✅ No shared-backend packaging errors
- ✅ Single, clear deployment path: Vercel (frontends) + Render (backends)

---

## Notes

- **Render Blueprint:** The `render.yaml` file remains in the repository but is **not used** for deployment. It serves as documentation/reference only. All services are created manually via Render dashboard.

- **Environment Variables:** All required values are documented in the respective `.env.production` files at the repository root. Copy values from the "BACKEND VARIABLES" section of each file.

- **Cost Optimization:** Using Upstash Redis (free tier: 256MB, 500K commands/month) instead of Render Redis saves costs. Both Reframe and Sketch2BIM share the same Upstash instance.

- **Database Schemas:** ASK and Sketch2BIM use the same Supabase database but different schemas (`ask_schema` and `sketch2bim_schema`). This allows for shared infrastructure while maintaining data separation.

---

## Support

If you encounter issues not covered in this guide:

1. Check Render service logs for specific error messages
2. Check Vercel deployment logs for frontend errors
3. Verify all environment variables are set correctly
4. Run `.\scripts\verify-deployment.ps1 -Verbose` for automated checks
5. Review `DEPLOYMENT_CONFIGURATION_GUIDE.md` for additional troubleshooting

---

**Last Updated:** After Docker removal and shared-backend packaging fix
**Status:** Ready for manual Render configuration

