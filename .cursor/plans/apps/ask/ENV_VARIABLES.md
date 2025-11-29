# Environment Variables Reference

Quick reference for environment variables needed for Render (backend) and Vercel (frontend) deployment.

> **⚠️ IMPORTANT: Environment Variables**  
> All production environment variables are in `ask.env.production` at the repository root.  
> This file serves as a deployment template for copying variables to Vercel/Render.  
> Local development can still use `.env.local` files for overrides, but they should not be committed to git.

## Render (Backend) Environment Variables

Copy these into your Render service environment variables:

```bash
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=https://ask.kvshvl.in,https://www.ask.kvshvl.in,https://ask-kvshvl-in.vercel.app
LOG_CSV_FILE=log.csv
IMAGES_DIR=images
LOG_DIR=logs
ENVIRONMENT=production
```

**Important Notes:**
- Replace `https://ask-kvshvl-in.vercel.app` with your actual Vercel deployment URL
- Add any other frontend URLs that need access (e.g., preview deployments)
- No spaces in the comma-separated `CORS_ORIGINS` list
- Render automatically provides `$PORT` - you can use that instead of `API_PORT=8000`

## Vercel (Frontend) Environment Variables

Copy these into your Vercel project environment variables:

```bash
NEXT_PUBLIC_API_URL=https://ask-api.onrender.com
NEXT_PUBLIC_SITE_URL=https://ask.kvshvl.in
```

**Important Notes:**
- Replace `https://ask-api.onrender.com` with your actual Render backend URL
- `NEXT_PUBLIC_*` variables are exposed to the browser
- Update the URL after your Render service is deployed

## Render Start Command

**Start Command:**
```bash
uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

**Build Command:**
```bash
pip install -r requirements.txt
```

## How to Add in Render

1. Go to your Render dashboard
2. Select your service
3. Click "Environment" tab
4. Click "Add Environment Variable"
5. Add each variable from the list above
6. **Set Start Command**: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
7. Click "Save Changes"
8. Service will automatically redeploy

**Alternative:** Use `render.yaml` file (already created in repo) for automatic setup

## How to Add in Vercel

1. Go to your Vercel project dashboard
2. Click "Settings"
3. Click "Environment Variables"
4. Click "Add New"
5. Add each variable from the list above
6. Select environment (Production, Preview, Development)
7. Click "Save"
8. Redeploy if needed

## Quick Copy-Paste for Render

```
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=https://ask.kvshvl.in,https://www.ask.kvshvl.in
LOG_CSV_FILE=log.csv
IMAGES_DIR=images
LOG_DIR=logs
ENVIRONMENT=production
```

## Quick Copy-Paste for Vercel

```
NEXT_PUBLIC_API_URL=https://ask-api.onrender.com
NEXT_PUBLIC_SITE_URL=https://ask.kvshvl.in
```

## After Deployment

1. **Update CORS_ORIGINS** in Render with your actual Vercel URL
2. **Update NEXT_PUBLIC_API_URL** in Vercel with your actual Render URL
3. **Test the connection** - visit your Vercel site and check browser console
4. **Verify CORS** - ensure API calls work from the frontend

