# Deployment Checklist

Complete deployment checklist for all applications in the monorepo.

## Pre-Deployment Verification

### Code Verification
- [ ] All code committed and pushed to `main` branch
- [ ] No uncommitted changes
- [ ] All tests pass (if applicable)
- [ ] No linter errors
- [ ] All dependencies installed

### Configuration Verification
- [ ] All `package.json` files have correct repository URLs
- [ ] All `render.yaml` files are configured correctly
- [ ] Environment variable files are up to date
- [ ] Database schemas are created
- [ ] Shared packages are properly linked

## ASK Application Deployment

### Frontend (Vercel)

1. **Verify Vercel Project**
   - [ ] Project connected: https://vercel.com/kvshvl/ask
   - [ ] Repository: `kushalsamant/kushalsamant.github.io`
   - [ ] Root Directory: `apps/ask/frontend`
   - [ ] Framework: Next.js

2. **Set Environment Variables**
   - [ ] Go to: https://vercel.com/kvshvl/ask/settings/environment-variables
   - [ ] Copy all variables from `ask.env.production` (Frontend section)
   - [ ] Verify `NEXT_PUBLIC_AUTH_URL=https://kvshvl.in`
   - [ ] Verify `ASK_NEXTAUTH_URL=https://ask.kvshvl.in`
   - [ ] Set for Production environment

3. **Deploy**
   - [ ] Push to `main` branch triggers automatic deployment
   - [ ] Or manually trigger deployment from Vercel dashboard
   - [ ] Verify deployment succeeds
   - [ ] Test at https://ask.kvshvl.in

### Backend (Render)

1. **Verify Render Service**
   - [ ] Service name: `ask-api`
   - [ ] Repository: `kushalsamant/kushalsamant.github.io`
   - [ ] Root Directory: `apps/ask`
   - [ ] Build Command: `pip install -r requirements.txt`
   - [ ] Start Command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`

2. **Set Environment Variables**
   - [ ] Go to: https://dashboard.render.com/web/[ASK-API-SERVICE]/env
   - [ ] Copy all variables from `ask.env.production` (Backend section)
   - [ ] **CRITICAL**: Set `ASK_DATABASE_URL` with Supabase connection string
     - Format: `postgresql://postgres.[PROJECT_REF]:[PASSWORD]@aws-[REGION].pooler.supabase.com:6543/postgres`
     - Get from: https://supabase.com/dashboard/project/[PROJECT_REF]/settings/database
     - Use pooler (port 6543) for connection pooling
   - [ ] Verify `DATABASE_SCHEMA=ask_schema`
   - [ ] Set `ASK_GROQ_API_KEY` (get from Groq dashboard)
   - [ ] Set Razorpay credentials
   - [ ] Set all other required variables

3. **Deploy**
   - [ ] Push to `main` branch triggers automatic deployment
   - [ ] Or manually trigger deployment from Render dashboard
   - [ ] Verify deployment succeeds
   - [ ] Check health endpoint: `https://ask-api.onrender.com/health`
   - [ ] Verify logs show no errors

## Sketch2BIM Application Deployment

### Frontend (Vercel)

1. **Verify Vercel Project**
   - [ ] Project connected: https://vercel.com/kvshvl/sketch2bim
   - [ ] Repository: `kushalsamant/kushalsamant.github.io`
   - [ ] Root Directory: `apps/sketch2bim/frontend`
   - [ ] Framework: Next.js

2. **Set Environment Variables**
   - [ ] Go to: https://vercel.com/kvshvl/sketch2bim/settings/environment-variables
   - [ ] Copy all variables from `sketch2bim.env.production` (Frontend section)
   - [ ] Verify `NEXT_PUBLIC_AUTH_URL=https://kvshvl.in`
   - [ ] Verify `SKETCH2BIM_NEXTAUTH_URL=https://sketch2bim.kvshvl.in`
   - [ ] Set for Production environment

3. **Deploy**
   - [ ] Push to `main` branch triggers automatic deployment
   - [ ] Or manually trigger deployment from Vercel dashboard
   - [ ] Verify deployment succeeds
   - [ ] Test at https://sketch2bim.kvshvl.in

### Backend (Render)

1. **Verify Render Service**
   - [ ] Service name: `sketch2bim-backend`
   - [ ] Repository: `kushalsamant/kushalsamant.github.io`
   - [ ] Root Directory: `apps/sketch2bim/backend`
   - [ ] Build Command: `pip install --upgrade pip && pip install -r requirements.txt`
   - [ ] Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - [ ] Python Version: 3.13

2. **Verify Redis Service**
   - [ ] Service name: `sketch2bim-redis`
   - [ ] Plan: starter
   - [ ] Connection string automatically linked

3. **Set Environment Variables**
   - [ ] Go to: https://dashboard.render.com/web/[SKETCH2BIM-BACKEND-SERVICE]/env
   - [ ] Copy all variables from `sketch2bim.env.production` (Backend section)
   - [ ] **CRITICAL**: Set `SKETCH2BIM_DATABASE_URL` with Supabase connection string
     - Format: `postgresql://postgres.[PROJECT_REF]:[PASSWORD]@aws-[REGION].pooler.supabase.com:6543/postgres`
     - Get from: https://supabase.com/dashboard/project/[PROJECT_REF]/settings/database
     - Use pooler (port 6543) for connection pooling
   - [ ] Verify `DATABASE_SCHEMA=sketch2bim_schema`
   - [ ] Verify `SKETCH2BIM_REDIS_URL` is linked from Redis service
   - [ ] Set all other required variables

4. **Deploy**
   - [ ] Push to `main` branch triggers automatic deployment
   - [ ] Or manually trigger deployment from Render dashboard
   - [ ] Verify deployment succeeds
   - [ ] Check health endpoint: `https://sketch2bim-backend.onrender.com/health`
   - [ ] Verify logs show no errors

## Reframe Application Deployment

### Frontend (Vercel)

1. **Verify Vercel Project**
   - [ ] Project connected: https://vercel.com/kvshvl/reframe
   - [ ] Repository: `kushalsamant/kushalsamant.github.io`
   - [ ] Root Directory: `apps/reframe`
   - [ ] Framework: Next.js

2. **Set Environment Variables**
   - [ ] Go to: https://vercel.com/kvshvl/reframe/settings/environment-variables
   - [ ] Copy all variables from `reframe.env.production` (Frontend section)
   - [ ] Verify `NEXT_PUBLIC_AUTH_URL=https://kvshvl.in`
   - [ ] Verify `REFRAME_NEXTAUTH_URL=https://reframe.kvshvl.in`
   - [ ] Set for Production environment

3. **Deploy**
   - [ ] Push to `main` branch triggers automatic deployment
   - [ ] Or manually trigger deployment from Vercel dashboard
   - [ ] Verify deployment succeeds
   - [ ] Test at https://reframe.kvshvl.in

### Backend (Render)

1. **Verify Render Service**
   - [ ] Service name: `reframe-api`
   - [ ] Repository: `kushalsamant/kushalsamant.github.io`
   - [ ] Root Directory: `apps/reframe/backend`
   - [ ] Build Command: `pip install --upgrade pip && pip install -r requirements.txt`
   - [ ] Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

2. **Set Environment Variables**
   - [ ] Go to: https://dashboard.render.com/web/[REFRAME-API-SERVICE]/env
   - [ ] Copy all variables from `reframe.env.production` (Backend section)
   - [ ] Set `REFRAME_GROQ_API_KEY` (get from Groq dashboard)
   - [ ] Set `REFRAME_UPSTASH_REDIS_REST_URL` (get from Upstash dashboard)
   - [ ] Set `REFRAME_UPSTASH_REDIS_REST_TOKEN` (get from Upstash dashboard)
   - [ ] Set `REFRAME_NEXTAUTH_SECRET`
   - [ ] Set all other required variables

3. **Deploy**
   - [ ] Push to `main` branch triggers automatic deployment
   - [ ] Or manually trigger deployment from Render dashboard
   - [ ] Verify deployment succeeds
   - [ ] Check health endpoint: `https://reframe-api.onrender.com/health`
   - [ ] Verify logs show no errors

## Post-Deployment Verification

### All Applications

- [ ] **Health Checks**
  - [ ] ASK backend health endpoint responds
  - [ ] Sketch2BIM backend health endpoint responds
  - [ ] Reframe backend health endpoint responds
  - [ ] Run automated verification: `.\scripts\verify-deployment.ps1`

- [ ] **Authentication**
  - [ ] Sign in works on all frontends
  - [ ] OAuth redirects to kvshvl.in correctly
  - [ ] Sessions persist correctly

- [ ] **API Connectivity**
  - [ ] Frontends can connect to backends
  - [ ] CORS is configured correctly
  - [ ] API endpoints respond correctly

- [ ] **Database**
  - [ ] ASK database connection works
  - [ ] Sketch2BIM database connection works
  - [ ] Schema isolation verified (no cross-schema access)

- [ ] **Payments**
  - [ ] Razorpay integration works
  - [ ] Webhook endpoints are accessible
  - [ ] Payment processing works

- [ ] **Monitoring**
  - [ ] Logs are accessible
  - [ ] Error tracking works (if configured)
  - [ ] Performance monitoring works (if configured)

## Rollback Procedure

If deployment fails:

1. **Vercel Rollback**
   - Go to project → Deployments
   - Find last successful deployment
   - Click "Promote to Production"

2. **Render Rollback**
   - Go to service → Manual Deploy
   - Select previous successful commit
   - Deploy

3. **Environment Variables**
   - Verify all environment variables are set correctly
   - Check for typos or missing variables
   - Re-deploy after fixing

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Check build logs for errors
   - Verify all dependencies are in requirements.txt/package.json
   - Check Node.js/Python version compatibility

2. **Environment Variable Issues**
   - Verify all required variables are set
   - Check for typos in variable names
   - Verify values are correct (no extra spaces)

3. **Database Connection Issues**
   - Verify DATABASE_URL is set correctly
   - Check Supabase connection string format
   - Verify DATABASE_SCHEMA is set
   - Check network connectivity

4. **Authentication Issues**
   - Verify NEXTAUTH_SECRET is set
   - Check NEXTAUTH_URL matches frontend URL
   - Verify OAuth credentials are correct

5. **CORS Issues**
   - Verify CORS_ORIGINS includes frontend URL
   - Check for trailing slashes
   - Verify protocol (http vs https)

## Notes

- All deployments use automatic deployments from `main` branch
- Environment variables should be set before first deployment
- Database schemas must be created before deployment
- Test in staging environment first if available
- Monitor logs after deployment for any errors
- Keep environment variable files in sync with deployments

