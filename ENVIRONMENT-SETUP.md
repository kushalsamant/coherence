# 🔧 Environment Setup Guide

Complete guide for configuring external services and environment variables for the KVSHVL platform.

**Estimated Time:** 60 minutes  
**Last Updated:** December 5, 2025

---

## 📋 Prerequisites

Before starting, ensure you have:
- [x] Code implementation complete (models directory created)
- [ ] Access to Render.com dashboard
- [ ] Access to Vercel dashboard
- [ ] Credit card for paid services (Upstash, BunnyCDN)
- [ ] API keys ready (Groq, Razorpay)

---

## 🎯 Configuration Checklist

### External Services
- [ ] Razorpay account created (live mode enabled)
- [ ] Upstash Redis database created
- [ ] Upstash Postgres - ASK database created
- [ ] Upstash Postgres - Sketch2BIM database created
- [ ] Groq API key obtained
- [ ] BunnyCDN storage zone created
- [ ] Google OAuth credentials configured

### Render Configuration
- [ ] All environment variables set
- [ ] Webhook secret configured
- [ ] Service redeployed

### Vercel Configuration
- [ ] All environment variables set
- [ ] Frontend redeployed

---

## 1️⃣ Razorpay Configuration (15 minutes)

### Step 1.1: Create Razorpay Account
1. Visit https://dashboard.razorpay.com
2. Sign up or log in
3. Switch to **Live Mode** (top-right toggle)
4. Complete KYC verification if required

### Step 1.2: Get API Keys
1. Go to **Settings** → **API Keys**
2. Click **Generate Live Key**
3. Copy the following:
   - `Key ID` (starts with `rzp_live_`)
   - `Key Secret` (keep this secure!)

**Save these for later:**
```
PLATFORM_RAZORPAY_KEY_ID=rzp_live_XXXXXXXXXXXX
PLATFORM_RAZORPAY_KEY_SECRET=XXXXXXXXXXXXXXXXXXXXXXXX
```

### Step 1.3: Verify Plan IDs (Already Created)
1. Go to **Subscriptions** → **Plans**
2. Verify these plans exist:
   - **Weekly Plan**: `plan_Rnb1CCVRIvBK2W` (₹1,299)
   - **Monthly Plan**: `plan_Rnb1CsrwHntisk` (₹3,499)
   - **Yearly Plan**: `plan_Rnb1DZy2EHhHqT` (₹29,999)

✅ These are already configured in `render.yaml`

### Step 1.4: Configure Webhook
1. Go to **Settings** → **Webhooks**
2. Click **+ Add New Webhook**
3. Enter the following:

**Webhook URL:**
```
https://kvshvl.in/api/platform/razorpay-webhook
```

**Active Events** (check these):
- ✅ `payment.captured` - One-time payments
- ✅ `subscription.created` - Subscription created
- ✅ `subscription.activated` - First payment successful
- ✅ `subscription.charged` - Renewal payment
- ✅ `subscription.cancelled` - Subscription cancelled
- ✅ `subscription.paused` - Subscription paused

4. Click **Create**
5. Copy the **Webhook Secret** shown

**Save this for later:**
```
PLATFORM_RAZORPAY_WEBHOOK_SECRET=XXXXXXXXXXXXXXXXXXXXXXXX
```

### Step 1.5: Test Webhook (Optional)
1. In the webhook settings, click **Test Webhook**
2. Select `payment.captured` event
3. Send test event
4. Verify you receive 200 OK response

---

## 2️⃣ Upstash Redis Configuration (10 minutes)

### Step 2.1: Create Redis Database
1. Visit https://console.upstash.com
2. Click **Create Database**
3. Configure:
   - **Name**: `kvshvl-platform-redis`
   - **Type**: Regional (or Global for better performance)
   - **Region**: Choose closest to your Render region (e.g., `us-east-1`)
4. Click **Create**

### Step 2.2: Get Connection Details
1. Click on your database
2. Scroll to **REST API** section
3. Copy the following:
   - `UPSTASH_REDIS_REST_URL`
   - `UPSTASH_REDIS_REST_TOKEN`

**Save these for later:**
```
PLATFORM_UPSTASH_REDIS_REST_URL=https://XXXXX.upstash.io
PLATFORM_UPSTASH_REDIS_REST_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXX
```

---

## 3️⃣ Upstash Postgres - ASK Database (8 minutes)

### Step 3.1: Create Database
1. In Upstash console, go to **Postgres**
2. Click **Create Database**
3. Configure:
   - **Name**: `kvshvl-ask`
   - **Region**: Same as Redis (e.g., `us-east-1`)
4. Click **Create**

### Step 3.2: Get Connection String
1. Click on your database
2. Copy the **Connection String** (Pooled)
   - Format: `postgresql://[USER]:[PASSWORD]@[HOST]:[PORT]/[DATABASE]`

**Save this for later:**
```
ASK_DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DATABASE
```

### Step 3.3: Initialize Tables (After Deployment)
```bash
# SSH into Render service or run locally with remote DB
cd apps/platform-api/database/migrations/ask
alembic upgrade head
```

---

## 4️⃣ Upstash Postgres - Sketch2BIM Database (7 minutes)

### Step 4.1: Create Database
1. In Upstash console, go to **Postgres**
2. Click **Create Database**
3. Configure:
   - **Name**: `kvshvl-sketch2bim`
   - **Region**: Same as Redis
4. Click **Create**

### Step 4.2: Get Connection String
1. Click on your database
2. Copy the **Connection String** (Pooled)

**Save this for later:**
```
SKETCH2BIM_DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DATABASE
```

### Step 4.3: Initialize Tables (After Deployment)
```bash
cd apps/platform-api/database/migrations/sketch2bim
alembic upgrade head
```

---

## 5️⃣ Groq API Keys (5 minutes)

### Step 5.1: Create Groq Account
1. Visit https://console.groq.com
2. Sign up or log in
3. Go to **API Keys**

### Step 5.2: Generate API Key
1. Click **Create API Key**
2. Name: `KVSHVL Platform`
3. Copy the API key

**Save this for later (can use same key for all):**
```
ASK_GROQ_API_KEY=gsk_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
REFRAME_GROQ_API_KEY=gsk_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
SKETCH2BIM_GROQ_API_KEY=gsk_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### Step 5.3: Verify Model Access
Models used:
- ASK: `llama-3.1-70b-versatile`
- Reframe: `llama-3.1-8b-instant`
- Sketch2BIM: `llama-3.1-8b-instant`

All should be available in free tier.

---

## 6️⃣ BunnyCDN Configuration (15 minutes)

### Step 6.1: Create BunnyCDN Account
1. Visit https://bunny.net
2. Sign up or log in
3. Add payment method (required)

### Step 6.2: Create Storage Zone
1. Go to **Storage** → **Add Storage Zone**
2. Configure:
   - **Zone Name**: `kvshvl-sketch2bim`
   - **Region**: Choose closest to your users
   - **Replication**: Optional (costs extra)
3. Click **Add Storage Zone**

### Step 6.3: Get Storage Credentials
1. Click on your storage zone
2. Copy the following:
   - **Storage Zone Name**: `kvshvl-sketch2bim`
   - **Password** (FTP Password)
   - **Hostname**: `storage.bunnycdn.com`

**Save these for later:**
```
SKETCH2BIM_BUNNY_STORAGE_ZONE=kvshvl-sketch2bim
SKETCH2BIM_BUNNY_ACCESS_KEY=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
```

### Step 6.4: Create Pull Zone (CDN)
1. Go to **CDN** → **Add Pull Zone**
2. Configure:
   - **Name**: `kvshvl-sketch2bim-cdn`
   - **Origin Type**: Storage Zone
   - **Storage Zone**: Select your storage zone
3. Click **Add Pull Zone**
4. Copy the **CDN Hostname**

**Save this for later:**
```
SKETCH2BIM_BUNNY_CDN_HOSTNAME=kvshvl-sketch2bim-cdn.b-cdn.net
```

---

## 7️⃣ Authentication Secrets (5 minutes)

### Step 7.1: Generate Auth Secret
Run this command locally:
```bash
openssl rand -base64 32
```

Copy the output and save:
```
PLATFORM_AUTH_SECRET=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
PLATFORM_NEXTAUTH_SECRET=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

**Note:** Use the **same value** for both variables.

### Step 7.2: Google OAuth (Already Configured?)
If not already set up:
1. Visit https://console.cloud.google.com
2. Create a new project or select existing
3. Enable **Google+ API**
4. Go to **Credentials** → **Create Credentials** → **OAuth 2.0 Client ID**
5. Configure:
   - **Application type**: Web application
   - **Authorized redirect URIs**:
     - `https://kvshvl.in/api/auth/callback/google`
     - `http://localhost:3000/api/auth/callback/google` (for dev)
6. Copy **Client ID** and **Client Secret**

```
GOOGLE_CLIENT_ID=XXXXXXXXXXXXXXXXXXXXXXXXXXXXX.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=XXXXXXXXXXXXXXXXXXXXXXXX
```

---

## 8️⃣ Render Configuration (10 minutes)

### Step 8.1: Access Render Dashboard
1. Visit https://dashboard.render.com
2. Find your service: `platform-api`
3. Click **Environment** tab

### Step 8.2: Set Environment Variables

Copy and paste these variables one by one:

#### Platform-Wide Variables
```
PLATFORM_APP_NAME=KVSHVL Platform API
PLATFORM_ENVIRONMENT=production
PLATFORM_DEBUG=false
PLATFORM_CORS_ORIGINS=https://kvshvl.in,https://www.kvshvl.in,https://ask.kvshvl.in,https://reframe.kvshvl.in,https://sketch2bim.kvshvl.in
```

#### Authentication
```
PLATFORM_AUTH_SECRET=[value from step 7.1]
PLATFORM_NEXTAUTH_SECRET=[same as above]
```

#### Razorpay (from Step 1)
```
PLATFORM_RAZORPAY_KEY_ID=[from step 1.2]
PLATFORM_RAZORPAY_KEY_SECRET=[from step 1.2]
PLATFORM_RAZORPAY_WEBHOOK_SECRET=[from step 1.4]
```

#### Redis (from Step 2)
```
PLATFORM_UPSTASH_REDIS_REST_URL=[from step 2.2]
PLATFORM_UPSTASH_REDIS_REST_TOKEN=[from step 2.2]
```

#### Databases (from Steps 3 & 4)
```
ASK_DATABASE_URL=[from step 3.2]
SKETCH2BIM_DATABASE_URL=[from step 4.2]
```

#### Groq API (from Step 5)
```
ASK_GROQ_API_KEY=[from step 5.2]
REFRAME_GROQ_API_KEY=[from step 5.2]
SKETCH2BIM_GROQ_API_KEY=[from step 5.2]
```

#### BunnyCDN (from Step 6)
```
SKETCH2BIM_BUNNY_STORAGE_ZONE=[from step 6.3]
SKETCH2BIM_BUNNY_ACCESS_KEY=[from step 6.3]
SKETCH2BIM_BUNNY_CDN_HOSTNAME=[from step 6.4]
```

### Step 8.3: Save and Redeploy
1. Click **Save Changes**
2. Service will automatically redeploy
3. Wait for deployment to complete (~3-5 minutes)
4. Check **Logs** for any errors

---

## 9️⃣ Vercel Configuration (10 minutes)

### Step 9.1: Access Vercel Dashboard
1. Visit https://vercel.com/kushalsamant-github-io
2. Click on your project
3. Go to **Settings** → **Environment Variables**

### Step 9.2: Set Environment Variables

#### Authentication
```
NEXTAUTH_URL=https://kvshvl.in
AUTH_SECRET=[same value as PLATFORM_AUTH_SECRET from Render]
GOOGLE_CLIENT_ID=[from step 7.2]
GOOGLE_CLIENT_SECRET=[from step 7.2]
```

#### API Configuration
```
NEXT_PUBLIC_PLATFORM_API_URL=https://kushalsamant-github-io.onrender.com
```

#### Redis (Same as Render)
```
UPSTASH_REDIS_REST_URL=[from step 2.2]
UPSTASH_REDIS_REST_TOKEN=[from step 2.2]
```

#### Razorpay (Frontend needs these too)
```
NEXT_PUBLIC_RAZORPAY_KEY_ID=[from step 1.2]
PLATFORM_RAZORPAY_KEY_SECRET=[from step 1.2]
PLATFORM_RAZORPAY_WEBHOOK_SECRET=[from step 1.4]
```

#### App-Specific Configs
```
REFRAME_FREE_LIMIT=5
```

### Step 9.3: Select Environments
For each variable, select which environments to apply:
- ✅ Production
- ✅ Preview (optional)
- ✅ Development (optional)

### Step 9.4: Redeploy
1. Click **Save**
2. Go to **Deployments** tab
3. Click **Redeploy** on the latest deployment
4. Wait for deployment to complete (~2-3 minutes)

---

## ✅ Verification (15 minutes)

### Test 1: Backend Health Checks
```bash
# Basic health
curl https://kushalsamant-github-io.onrender.com/health

# Expected response:
# {
#   "status": "healthy",
#   "service": "KVSHVL Platform API",
#   "version": "1.0.0",
#   "apps": ["ask", "reframe", "sketch2bim"]
# }

# Liveness probe
curl https://kushalsamant-github-io.onrender.com/health/live

# Readiness probe (checks databases)
curl https://kushalsamant-github-io.onrender.com/health/ready
```

### Test 2: Frontend Pages
Visit these URLs and verify they load:
- https://kvshvl.in
- https://kvshvl.in/ask
- https://kvshvl.in/reframe
- https://kvshvl.in/sketch2bim
- https://kvshvl.in/account

### Test 3: Authentication
1. Go to https://kvshvl.in
2. Click **Sign In**
3. Sign in with Google
4. Verify redirect to account page

### Test 4: Razorpay Webhook
1. Go to Razorpay Dashboard → Webhooks
2. Click on your webhook
3. Click **Test Webhook**
4. Select `payment.captured` event
5. Send test
6. Verify **200 OK** response

### Test 5: End-to-End Flow
1. **ASK**: Generate a question about architecture
2. **Reframe**: Reframe some text with a tone
3. **Sketch2BIM**: Upload a test sketch (if you have credits)
4. **Payments**: Try subscribing (test mode if available)

---

## 🔍 Troubleshooting

### Backend Won't Start
1. Check Render logs: https://dashboard.render.com
2. Verify all environment variables are set
3. Check database connections:
   ```bash
   # Test connection string locally
   psql "postgresql://..."
   ```

### Frontend Errors
1. Check Vercel deployment logs
2. Verify `NEXTAUTH_URL` matches your domain
3. Check browser console for errors

### Database Connection Errors
1. Verify connection strings are correct
2. Check if IP is whitelisted (Upstash allows all by default)
3. Test connection with `psql` command

### Razorpay Webhook Not Working
1. Verify webhook URL is correct
2. Check webhook secret matches environment variable
3. View webhook logs in Razorpay Dashboard

### Redis Connection Errors
1. Verify REST URL and Token are correct
2. Check Upstash Redis dashboard for connection logs
3. Test with curl:
   ```bash
   curl https://YOUR_REDIS_URL/get/test \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```

---

## 📚 Additional Resources

- **Render Docs**: https://render.com/docs
- **Vercel Docs**: https://vercel.com/docs
- **Upstash Docs**: https://docs.upstash.com
- **Razorpay Docs**: https://razorpay.com/docs
- **BunnyCDN Docs**: https://docs.bunny.net
- **Groq Docs**: https://console.groq.com/docs

---

## ✅ Configuration Complete!

Once all steps are complete, your platform should be:
- ✅ Backend deployed and healthy
- ✅ Frontend deployed and accessible
- ✅ Databases connected and migrated
- ✅ Authentication working
- ✅ Payments integrated
- ✅ All services operational

**Estimated Total Time:** 60 minutes  
**Total Cost:** ~$20-30/month (Upstash + BunnyCDN)

---

**Last Updated:** December 5, 2025  
**Next Steps:** Run end-to-end tests and monitor logs for 24 hours

