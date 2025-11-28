# ASK Deployment Guide

This document provides environment variable configurations for deploying ASK to Render (backend) and Vercel (frontend).

> **⚠️ Important:** This is part of the KVSHVL Platform monorepo. All production environment variables are centralized in `ask.env.production` at the repository root.

## Backend Deployment (Render)

### Environment Variables

Add these to your Render service environment variables:

```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# CORS Origins (comma-separated, no spaces)
CORS_ORIGINS=https://ask.kvshvl.in,https://www.ask.kvshvl.in,https://ask-kvshvl-in.vercel.app

# File Paths
LOG_CSV_FILE=log.csv
IMAGES_DIR=images
LOG_DIR=logs

# Environment
ENVIRONMENT=production
```

### Render Setup Steps

1. **Create a new Web Service** in Render
2. **Connect your GitHub repository** (monorepo: `kushalsamant.github.io`)
3. **Set Root Directory**: `apps/ask`
4. **Build Command**: `pip install -r requirements-api.txt`
5. **Start Command**: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
6. **Add Environment Variables** from the list above (or load from `ask.env.production` at repo root)
7. **Database**: Configure Supabase PostgreSQL connection (shared database with `ask_schema`)

### Important Notes for Render

- Render provides a `$PORT` environment variable automatically
- Update `CORS_ORIGINS` to include your Render backend URL if needed
- Ensure `images/` directory and `log.csv` are in your repository or use persistent disk
- For persistent storage, consider using Render Disk or external storage (S3, etc.)

## Frontend Deployment (Vercel)

### Environment Variables

Add these to your Vercel project environment variables:

```bash
# API Base URL
# Replace with your Render backend URL
NEXT_PUBLIC_API_URL=https://ask-api.onrender.com

# Site URL (optional, for metadata)
NEXT_PUBLIC_SITE_URL=https://ask.kvshvl.in
```

### Vercel Setup Steps

1. **Import your GitHub repository** in Vercel (monorepo: `kushalsamant.github.io`)
2. **Set Root Directory**: `apps/ask/frontend`
3. **Framework Preset**: Next.js (auto-detected)
4. **Build Command**: `npm run build` (default)
5. **Output Directory**: `.next` (default)
6. **Add Environment Variables** from the list above (or load from `ask.env.production` at repo root)
7. **Deploy**

### Important Notes for Vercel

- `NEXT_PUBLIC_*` variables are exposed to the browser
- Update `NEXT_PUBLIC_API_URL` to match your Render backend URL
- Vercel automatically handles Next.js optimizations
- Custom domain: Add `ask.kvshvl.in` in Vercel project settings

## Local Development

> **Note:** For local development, create `.env.local` files in `apps/ask/api/` and `apps/ask/frontend/`. These files are gitignored and will override values from `ask.env.production` at the repository root.

### Backend (.env.local)

Create `apps/ask/api/.env.local`:

```bash
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
LOG_CSV_FILE=log.csv
IMAGES_DIR=images
LOG_DIR=logs
ENVIRONMENT=development
# Database (use Supabase connection string for local dev)
DATABASE_URL=postgresql://user:password@host:port/database
DATABASE_SCHEMA=ask_schema
```

### Frontend (.env.local)

Create `apps/ask/frontend/.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Environment Variable Reference

### Backend Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `API_HOST` | Host to bind to | `0.0.0.0` | No |
| `API_PORT` | Port to bind to | `8000` | No (Render uses `$PORT`) |
| `CORS_ORIGINS` | Allowed CORS origins (comma-separated) | - | Yes |
| `LOG_CSV_FILE` | Path to CSV file | `log.csv` | No |
| `IMAGES_DIR` | Images directory | `images` | No |
| `LOG_DIR` | Logs directory | `logs` | No |
| `ENVIRONMENT` | Environment name | - | No |

### Frontend Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:8000` | Yes |
| `NEXT_PUBLIC_SITE_URL` | Frontend site URL | - | No |

## Post-Deployment Checklist

### Backend (Render)

- [ ] Verify API is accessible at Render URL
- [ ] Test `/health` endpoint
- [ ] Test `/api/stats` endpoint
- [ ] Verify CORS is working (test from frontend)
- [ ] Check that images are being served correctly
- [ ] Verify CSV file is readable

### Frontend (Vercel)

- [ ] Verify site loads at Vercel URL
- [ ] Test API connection (check browser console)
- [ ] Test browsing Q&A pairs
- [ ] Test theme filtering
- [ ] Test Q&A detail page
- [ ] Test image loading
- [ ] Verify custom domain (if configured)

## Troubleshooting

### CORS Errors

If you see CORS errors:
1. Check `CORS_ORIGINS` includes your frontend URL
2. Ensure no spaces in comma-separated list
3. Include both `https://ask.kvshvl.in` and `https://www.ask.kvshvl.in`
4. Restart backend after changing CORS settings

### API Connection Errors

If frontend can't connect to backend:
1. Verify `NEXT_PUBLIC_API_URL` matches your Render backend URL
2. Check backend is running and accessible
3. Test backend URL directly in browser
4. Check browser console for specific error messages

### Image Loading Issues

If images don't load:
1. Verify `images/` directory exists in backend
2. Check image filenames match CSV data
3. Test image URL directly: `{BACKEND_URL}/static/images/{filename}`
4. Check Next.js image configuration in `next.config.ts`

## Security Notes

- Never commit `.env` files to git
- Use `.env.example` files as templates
- Rotate API keys and secrets regularly
- Use environment-specific configurations
- Enable HTTPS in production
- Review CORS origins regularly

