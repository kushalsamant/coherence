# Deployment Configuration Guide - Vercel & Render

## Overview

This guide provides step-by-step instructions for configuring Vercel and Render after the infrastructure consolidation changes. All authentication is now centralized at `kvshvl.in`, and Redis has been consolidated to Upstash.

---

## Prerequisites

- ✅ Code changes committed and pushed to repository
- ✅ Google OAuth credentials ready:
  - Client ID: `620186529337-lrr0bflcuihq2gnsko6vbrnsdv2u3ugu.apps.googleusercontent.com`
  - Client Secret: `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`
- ✅ Upstash Redis credentials (for Sketch2BIM and Reframe backends)
- ✅ Access to Vercel dashboard (https://vercel.com)
- ✅ Access to Render dashboard (https://dashboard.render.com)

---

## Part 1: Vercel Configuration

### Step 1.1: Main Site (kushalsamant-github-io)

**Project URL:** https://vercel.com/kvshvl/kushalsamant-github-io/settings/environment-variables

1. Navigate to **Project Settings** → **Environment Variables**
2. **Add the following variables:**

   | Variable Name | Value | Environments |
   |--------------|-------|--------------|
   | `GOOGLE_CLIENT_ID` | `620186529337-lrr0bflcuihq2gnsko6vbrnsdv2u3ugu.apps.googleusercontent.com` | Production, Preview, Development |
   | `GOOGLE_CLIENT_SECRET` | `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` | Production, Preview, Development |
   | `NEXTAUTH_SECRET` | (Generate with `openssl rand -base64 32` or use existing) | Production, Preview, Development |
   | `AUTH_SECRET` | (Same value as `NEXTAUTH_SECRET`) | Production, Preview, Development |

3. **Remove old variables (if they exist):**
   - Any `ASK_GOOGLE_*` variables
   - Any `REFRAME_GOOGLE_*` variables
   - Any `SKETCH2BIM_GOOGLE_*` variables

4. **Save all changes**

5. **Redeploy:**
   - Go to **Deployments** tab
   - Click **⋯** (three dots) on latest deployment
   - Select **Redeploy**

---

### Step 1.2: ASK App

**Project URL:** https://vercel.com/kvshvl/ask/settings/environment-variables

1. Navigate to **Project Settings** → **Environment Variables**

2. **Remove old OAuth variables:**
   - `ASK_GOOGLE_CLIENT_ID` (if exists)
   - `ASK_GOOGLE_SECRET` (if exists)

3. **Add/Update the following variable:**

   | Variable Name | Value | Environments |
   |--------------|-------|--------------|
   | `NEXT_PUBLIC_AUTH_URL` | `https://kvshvl.in` | Production, Preview, Development |

4. **Verify other ASK variables are set** (from `ask.env.production` frontend section):
   - `ASK_API_BASE_URL` = `https://ask-api.onrender.com`
   - `ASK_AUTH_SECRET` = `lFGHiDWlnSC1yn1F95VgqttX0WZ2s4o+Ybsm9ELw564=`
   - `ASK_AUTH_URL` = `https://ask.kvshvl.in`
   - `ASK_BACKEND_URL` = `https://ask-api.onrender.com`
   - `ASK_NEXT_PUBLIC_API_URL` = `https://ask-api.onrender.com`
   - `ASK_NEXTAUTH_SECRET` = `lFGHiDWlnSC1yn1F95VgqttX0WZ2s4o+Ybsm9ELw564=`
   - `ASK_NEXTAUTH_URL` = `https://ask.kvshvl.in`

5. **Save all changes**

6. **Redeploy** (same process as Step 1.1)

---

### Step 1.3: Reframe App

**Project URL:** https://vercel.com/kvshvl/reframe/settings/environment-variables

1. Navigate to **Project Settings** → **Environment Variables**

2. **Remove old OAuth variables:**
   - `REFRAME_GOOGLE_CLIENT_ID` (if exists)
   - `REFRAME_GOOGLE_CLIENT_SECRET` (if exists)

3. **Add/Update the following variable:**

   | Variable Name | Value | Environments |
   |--------------|-------|--------------|
   | `NEXT_PUBLIC_AUTH_URL` | `https://kvshvl.in` | Production, Preview, Development |

4. **Verify other Reframe variables are set** (from `reframe.env.production` frontend section):
   - `REFRAME_API_URL` = `https://reframe-api.onrender.com`
   - `REFRAME_AUTH_SECRET` = `lFGHiDWlnSC1yn1F95VgqttX0WZ2s4o+Ybsm9ELw564=`
   - `REFRAME_AUTH_URL` = `https://reframe.kvshvl.in`
   - `REFRAME_NEXT_PUBLIC_API_URL` = `https://reframe-api.onrender.com`
   - `REFRAME_NEXT_PUBLIC_FREE_LIMIT` = `5`
   - `REFRAME_NEXT_PUBLIC_SITE_URL` = `https://reframe.kvshvl.in`
   - `REFRAME_NEXTAUTH_SECRET` = `lFGHiDWlnSC1yn1F95VgqttX0WZ2s4o+Ybsm9ELw564=`
   - `REFRAME_NEXTAUTH_URL` = `https://reframe.kvshvl.in`
   - All Razorpay variables (if needed)

5. **Save all changes**

6. **Redeploy**

---

### Step 1.4: Sketch2BIM App

**Project URL:** https://vercel.com/kvshvl/sketch2bim/settings/environment-variables

1. Navigate to **Project Settings** → **Environment Variables**

2. **Remove old OAuth variables:**
   - `SKETCH2BIM_GOOGLE_CLIENT_ID` (if exists)
   - `SKETCH2BIM_GOOGLE_SECRET` (if exists)

3. **Add/Update the following variable:**

   | Variable Name | Value | Environments |
   |--------------|-------|--------------|
   | `NEXT_PUBLIC_AUTH_URL` | `https://kvshvl.in` | Production, Preview, Development |

4. **Verify other Sketch2BIM variables are set** (from `sketch2bim.env.production` frontend section):
   - `SKETCH2BIM_AUTH_SECRET` = `lFGHiDWlnSC1yn1F95VgqttX0WZ2s4o+Ybsm9ELw564=`
   - `SKETCH2BIM_AUTH_URL` = `https://sketch2bim.kvshvl.in`
   - `SKETCH2BIM_NEXT_PUBLIC_API_URL` = `https://sketch2bim-backend.onrender.com`
   - `SKETCH2BIM_NEXT_PUBLIC_FREE_LIMIT` = `5`
   - `SKETCH2BIM_NEXTAUTH_SECRET` = `lFGHiDWlnSC1yn1F95VgqttX0WZ2s4o+Ybsm9ELw564=`
   - `SKETCH2BIM_NEXTAUTH_URL` = `https://sketch2bim.kvshvl.in`

5. **Save all changes**

6. **Redeploy**

---

## Part 2: Render Configuration

### Step 2.1: Connect Repository (If Not Already Connected)

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **New +** → **Blueprint**
3. Connect GitHub account (if not connected)
4. Select repository: `kushalsamant/kushalsamant.github.io`
5. Render will detect `render.yaml` at root
6. Click **Apply**
7. Render creates all services automatically:
   - `ask-backend`
   - `reframe-backend`
   - `sketch2bim-backend`

**Note:** If services already exist, skip to Step 2.2.

---

### Step 2.2: ASK Backend Service

**Service URL:** https://dashboard.render.com/web/[ASK-BACKEND-SERVICE]/env

1. Navigate to **ask-backend** service → **Environment** tab

2. **Add/Update the following variables** (from `ask.env.production` backend section):

   | Variable Name | Value | Source |
   |--------------|-------|--------|
   | `ASK_DATABASE_URL` | `postgresql://...` | From Supabase dashboard |
   | `ASK_GROQ_API_KEY` | `gsk_...` | Your Groq API key |
   | `ASK_RAZORPAY_KEY_ID` | `rzp_live_RhNUuWRBG7lzR4` | From Razorpay |
   | `ASK_RAZORPAY_KEY_SECRET` | `7T1MCu1xNjX9G4soT7kuqqdB` | From Razorpay |
   | `ASK_RAZORPAY_WEBHOOK_SECRET` | `bbzTiAtV2LWSt4J` | From Razorpay |

3. **Verify these are set** (should be auto-set from `render.yaml`):
   - `API_HOST` = `0.0.0.0`
   - `ASK_CORS_ORIGINS` = `https://ask.kvshvl.in,https://www.ask.kvshvl.in`
   - `ASK_LOG_CSV_FILE` = `log.csv`
   - `ASK_LOG_DIR` = `logs`
   - `ASK_ENVIRONMENT` = `production`
   - `DATABASE_SCHEMA` = `ask_schema`
   - `ASK_FRONTEND_URL` = `https://ask.kvshvl.in`
   - `RAZORPAY_WEEK_AMOUNT` = `129900`
   - `RAZORPAY_MONTH_AMOUNT` = `349900`
   - `RAZORPAY_YEAR_AMOUNT` = `2999900`

4. **Save changes** - Service will auto-deploy

---

### Step 2.3: Reframe Backend Service

**Service URL:** https://dashboard.render.com/web/[REFRAME-BACKEND-SERVICE]/env

1. Navigate to **reframe-backend** service → **Environment** tab

2. **Add/Update the following variables** (from `reframe.env.production` backend section):

   | Variable Name | Value | Source |
   |--------------|-------|--------|
   | `REFRAME_GROQ_API_KEY` | `gsk_...` | Your Groq API key |
   | `REFRAME_UPSTASH_REDIS_REST_URL` | `https://...` | From Upstash console |
   | `REFRAME_UPSTASH_REDIS_REST_TOKEN` | `AWdJ...` | From Upstash console |
   | `REFRAME_NEXTAUTH_SECRET` | `lFGHiDWlnSC1yn1F95VgqttX0WZ2s4o+Ybsm9ELw564=` | Your secret |
   | `REFRAME_AUTH_SECRET` | `lFGHiDWlnSC1yn1F95VgqttX0WZ2s4o+Ybsm9ELw564=` | Your secret |

3. **Verify these are set** (should be auto-set from `render.yaml`):
   - `ENVIRONMENT` = `production`
   - `DEBUG` = `false`
   - `JWT_ALGORITHM` = `HS256`
   - `REFRAME_FREE_LIMIT` = `5`
   - `REFRAME_CORS_ORIGINS` = `https://reframe.kvshvl.in,https://www.reframe.kvshvl.in`

4. **Save changes** - Service will auto-deploy

---

### Step 2.4: Sketch2BIM Backend Service

**Service URL:** https://dashboard.render.com/web/[SKETCH2BIM-BACKEND-SERVICE]/env

1. Navigate to **sketch2bim-backend** service → **Environment** tab

2. **IMPORTANT: Remove old Redis variable:**
   - Delete `SKETCH2BIM_REDIS_URL` (if it exists) - This was from Render Redis service

3. **Add/Update the following variables** (from `sketch2bim.env.production` backend section):

   | Variable Name | Value | Source |
   |--------------|-------|--------|
   | `SKETCH2BIM_DATABASE_URL` | `postgresql://...` | From Supabase dashboard |
   | `SKETCH2BIM_UPSTASH_REDIS_REST_URL` | `https://...` | From Upstash console |
   | `SKETCH2BIM_UPSTASH_REDIS_REST_TOKEN` | `AWdJ...` | From Upstash console |
   | `SKETCH2BIM_NEXTAUTH_SECRET` | `lFGHiDWlnSC1yn1F95VgqttX0WZ2s4o+Ybsm9ELw564=` | Your secret |
   | `SKETCH2BIM_RAZORPAY_KEY_ID` | `rzp_live_RhNUuWRBG7lzR4` | From Razorpay |
   | `SKETCH2BIM_RAZORPAY_KEY_SECRET` | `7T1MCu1xNjX9G4soT7kuqqdB` | From Razorpay |
   | `SKETCH2BIM_RAZORPAY_WEBHOOK_SECRET` | `bbzTiAtV2LWSt4J` | From Razorpay |
   | `SKETCH2BIM_BUNNY_STORAGE_ZONE` | `kvshvl` | From BunnyCDN |
   | `SKETCH2BIM_BUNNY_ACCESS_KEY` | `4026f19d-3836-4442-ba87fe2013c4-4f75-4944` | From BunnyCDN |
   | `SKETCH2BIM_BUNNY_CDN_HOSTNAME` | `kvshvl.b-cdn.net` | From BunnyCDN |
   | `SKETCH2BIM_REPLICATE_API_KEY` | `r8_...` | From Replicate |
   | `SKETCH2BIM_REPLICATE_MODEL_ID` | `kushalsamant/sketch2bim-processor` | Your model ID |

4. **Verify these are set** (should be auto-set from `render.yaml`):
   - `APP_ENV` = `production`
   - `DEBUG` = `false`
   - `DATABASE_SCHEMA` = `sketch2bim_schema`
   - `SKETCH2BIM_FRONTEND_URL` = `https://sketch2bim.kvshvl.in`
   - `SKETCH2BIM_ALLOWED_ORIGINS` = `https://sketch2bim.kvshvl.in`
   - `RAZORPAY_WEEK_AMOUNT` = `129900`
   - `RAZORPAY_MONTH_AMOUNT` = `349900`
   - `RAZORPAY_YEAR_AMOUNT` = `2999900`

5. **Save changes** - Service will auto-deploy

---

## Part 3: Google OAuth Console Verification

### Step 3.1: Verify OAuth Configuration

1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Select the OAuth 2.0 Client: **KVSHVL (PRODUCTION)**
3. **Verify Authorized JavaScript Origins:**
   - ✅ `https://kvshvl.in`
   - ✅ `http://localhost:3000`

4. **Verify Authorized Redirect URIs:**
   - ✅ `https://kvshvl.in/api/auth/callback/google`
   - ✅ `http://localhost:3000/api/auth/callback/google`

5. **If any are missing, add them and save**

---

## Part 4: Upstash Redis Configuration

### Step 4.1: Get Upstash Redis Credentials

1. Go to [Upstash Console](https://console.upstash.com/redis)
2. Select your Redis database (or create a new one)
3. Copy the following:
   - **REST URL**: `https://splendid-platypus-26441.upstash.io` (or your URL)
   - **REST TOKEN**: `AWdJAAIncDJjZTMyOGIzZTc3ZmU0MjVhYmZmMDJiODgyYjhlY2NmZHAyMjY0NDE` (or your token)

### Step 4.2: Add to Render Services

- **Reframe Backend:** Already configured in Step 2.3
- **Sketch2BIM Backend:** Already configured in Step 2.4

**Note:** Both services use the same Upstash Redis instance (shared).

---

## Part 5: Testing & Verification

### Step 5.1: Wait for Deployments

- **Vercel:** Usually completes in 1-3 minutes
- **Render:** Usually completes in 2-5 minutes per service

### Step 5.1a: Automated Verification (Optional)

Run the deployment verification script to check health endpoints:

```powershell
.\scripts\verify-deployment.ps1
```

For verbose output:
```powershell
.\scripts\verify-deployment.ps1 -Verbose
```

This script checks:
- All backend health endpoints
- Environment file existence
- Provides summary of deployment status

### Step 5.2: Test Authentication Flow

1. **Test ASK App:**
   - Go to `https://ask.kvshvl.in`
   - Click "Sign In"
   - Should redirect to `https://kvshvl.in/api/auth/signin?app=ask&returnUrl=...`
   - Complete Google OAuth
   - Should redirect back to `https://ask.kvshvl.in?auth=success`

2. **Test Reframe App:**
   - Go to `https://reframe.kvshvl.in`
   - Click "Sign In"
   - Should redirect to `https://kvshvl.in/api/auth/signin?app=reframe&returnUrl=...`
   - Complete Google OAuth
   - Should redirect back to `https://reframe.kvshvl.in?auth=success`

3. **Test Sketch2BIM App:**
   - Go to `https://sketch2bim.kvshvl.in`
   - Click "Sign In"
   - Should redirect to `https://kvshvl.in/api/auth/signin?app=sketch2bim&returnUrl=...`
   - Complete Google OAuth
   - Should redirect back to `https://sketch2bim.kvshvl.in?auth=success`

4. **Test Main Site:**
   - Go to `https://kvshvl.in/api/auth/signin`
   - Should redirect to Google OAuth
   - After signing in, should redirect back to `https://kvshvl.in`

### Step 5.3: Verify Backend Services

1. Check Render dashboard - all services should show "Live" status
2. Test health endpoints:
   - `https://ask-api.onrender.com/health`
   - `https://reframe-api.onrender.com/health`
   - `https://sketch2bim-backend.onrender.com/health`

---

## Troubleshooting

### Issue: OAuth redirect fails

**Solution:**
- Verify `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` are set in Vercel (main site)
- Check redirect URI in Google Console matches exactly: `https://kvshvl.in/api/auth/callback/google`
- Wait 5-10 minutes after Google OAuth changes for propagation

### Issue: App doesn't redirect to kvshvl.in

**Solution:**
- Verify `NEXT_PUBLIC_AUTH_URL` is set to `https://kvshvl.in` in app's Vercel project
- Check browser console for errors
- Ensure app has been redeployed after adding the variable

### Issue: Backend service fails to start

**Solution:**
- Check Render logs for specific error messages
- Verify all required environment variables are set
- For Sketch2BIM: Ensure `SKETCH2BIM_UPSTASH_REDIS_REST_URL` and `SKETCH2BIM_UPSTASH_REDIS_REST_TOKEN` are set (not `SKETCH2BIM_REDIS_URL`)

### Issue: Redis connection errors

**Solution:**
- Verify Upstash Redis credentials are correct
- Check Upstash console for database status
- Ensure REST URL and REST TOKEN are set correctly (not connection string format)

---

## Checklist

Use this checklist to track your progress:

### Vercel Configuration
- [ ] Main site: Added `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `NEXTAUTH_SECRET`, `AUTH_SECRET`
- [ ] Main site: Removed old app-specific OAuth variables
- [ ] Main site: Redeployed
- [ ] ASK app: Added `NEXT_PUBLIC_AUTH_URL`
- [ ] ASK app: Removed old OAuth variables
- [ ] ASK app: Redeployed
- [ ] Reframe app: Added `NEXT_PUBLIC_AUTH_URL`
- [ ] Reframe app: Removed old OAuth variables
- [ ] Reframe app: Redeployed
- [ ] Sketch2BIM app: Added `NEXT_PUBLIC_AUTH_URL`
- [ ] Sketch2BIM app: Removed old OAuth variables
- [ ] Sketch2BIM app: Redeployed

### Render Configuration
- [ ] Repository connected (or services already exist)
- [ ] ASK backend: All environment variables set
- [ ] Reframe backend: All environment variables set (including Upstash Redis)
- [ ] Sketch2BIM backend: Removed `SKETCH2BIM_REDIS_URL`
- [ ] Sketch2BIM backend: Added `SKETCH2BIM_UPSTASH_REDIS_REST_URL` and `SKETCH2BIM_UPSTASH_REDIS_REST_TOKEN`
- [ ] Sketch2BIM backend: All other environment variables set
- [ ] All services deployed and running

### Google OAuth
- [ ] Authorized JavaScript Origins verified
- [ ] Authorized Redirect URIs verified

### Testing
- [ ] ASK app authentication flow tested
- [ ] Reframe app authentication flow tested
- [ ] Sketch2BIM app authentication flow tested
- [ ] Main site authentication flow tested
- [ ] All backend health endpoints responding

---

## Support

If you encounter issues not covered in this guide:
1. Check Vercel deployment logs
2. Check Render service logs
3. Check browser console for frontend errors
4. Verify all environment variables are set correctly
5. Ensure all services are deployed and running

---

**Last Updated:** After infrastructure consolidation (centralized auth + Upstash Redis)

