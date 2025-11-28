# Environment Variables Reference Guide

## Overview

This document provides a complete reference for all environment variables used across the KVSHVL Platform monorepo applications.

## File Location

All production environment variables are centralized in:
- **File**: `kushalsamant.github.io/.env.production`
- **Purpose**: Single source of truth for all production secrets
- **Scope**: Shared across ASK, Reframe, and Sketch2BIM

## Variable Organization

The `.env.production` file is organized into sections:

1. **Shared Variables** - Used by multiple projects
2. **ASK - Frontend Variables** - Vercel deployment
3. **ASK - Backend Variables** - Render deployment
4. **Reframe - Frontend Variables** - Vercel deployment
5. **Reframe - Backend Variables** - Render deployment
6. **Sketch2BIM - Frontend Variables** - Vercel deployment
7. **Sketch2BIM - Backend Variables** - Render deployment

## Quick Reference by Project

### ASK Frontend (Vercel)
- `AUTH_URL`, `NEXTAUTH_URL`, `NEXTAUTH_SECRET`, `AUTH_SECRET`
- `AUTH_GOOGLE_ID`, `AUTH_GOOGLE_SECRET`
- `NEXT_PUBLIC_API_URL`, `API_BASE_URL`, `BACKEND_URL`

### ASK Backend (Render)
- `DATABASE_URL`, `DATABASE_SCHEMA=ask_schema`
- `GROQ_API_KEY`, `GROQ_MODEL`, `GROQ_DAILY_COST_THRESHOLD`, `GROQ_MONTHLY_COST_THRESHOLD`
- `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`, `RAZORPAY_WEBHOOK_SECRET`
- `CORS_ORIGINS`, `FRONTEND_URL`
- `LOG_DIR`, `LOG_CSV_FILE`, `LOG_LEVEL`

### Reframe Frontend (Vercel)
- `AUTH_URL`, `NEXTAUTH_URL`, `NEXTAUTH_SECRET`, `AUTH_SECRET`
- `REFRAME_GOOGLE_CLIENT_ID`, `REFRAME_GOOGLE_CLIENT_SECRET`
- `REFRAME_API_URL`, `NEXT_PUBLIC_API_URL`
- `NEXT_PUBLIC_SITE_URL`, `NEXT_PUBLIC_FREE_LIMIT`

### Reframe Backend (Render)
- `UPSTASH_REDIS_REST_URL`, `UPSTASH_REDIS_REST_TOKEN`
- `GROQ_API_KEY`, `GROQ_DAILY_COST_THRESHOLD`, `GROQ_MONTHLY_COST_THRESHOLD`
- `FREE_LIMIT`
- `CORS_ORIGINS`
- `JWT_ALGORITHM`

### Sketch2BIM Frontend (Vercel)
- `AUTH_URL`, `NEXTAUTH_URL`, `NEXTAUTH_SECRET`, `AUTH_SECRET`
- `AUTH_GOOGLE_ID`, `AUTH_GOOGLE_SECRET`
- `NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_FREE_LIMIT`

### Sketch2BIM Backend (Render)
- `DATABASE_URL`, `DATABASE_SCHEMA=sketch2bim_schema`
- `BUNNY_STORAGE_ZONE`, `BUNNY_ACCESS_KEY`, `BUNNY_CDN_HOSTNAME`
- `REDIS_URL`
- `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`, `RAZORPAY_WEBHOOK_SECRET`
- `REPLICATE_API_KEY`, `REPLICATE_MODEL_ID`
- `ALLOWED_ORIGINS`, `FRONTEND_URL`
- `SECRET_KEY`, `JWT_ALGORITHM`

## Shared Variables

These variables are used by multiple projects:

- `GROQ_API_KEY` - ASK, Reframe
- `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`, `RAZORPAY_WEBHOOK_SECRET` - All projects
- `DATABASE_URL` - ASK, Sketch2BIM (shared Supabase database)
- `UPSTASH_REDIS_REST_URL`, `UPSTASH_REDIS_REST_TOKEN` - Reframe, optional for others
- `RESEND_API_KEY` - Email service (used by multiple projects)

## Deployment Instructions

### Vercel (Frontend)

1. Go to your project settings → Environment Variables
2. Copy variables from the **Frontend** section for each app
3. Set environment: **Production** (and Preview/Development if needed)

### Render (Backend)

1. Go to your service → Environment
2. Copy variables from the **Backend** section for each app
3. Set as **Environment Variables** (not secrets, unless sensitive)

## Important Notes

1. **Database Schemas**: 
   - ASK uses `DATABASE_SCHEMA=ask_schema`
   - Sketch2BIM uses `DATABASE_SCHEMA=sketch2bim_schema`
   - Both use the same `DATABASE_URL` (Supabase)

2. **Google OAuth**: Each app has separate credentials
   - ASK: `AUTH_GOOGLE_ID` / `AUTH_GOOGLE_SECRET`
   - Reframe: `REFRAME_GOOGLE_CLIENT_ID` / `REFRAME_GOOGLE_CLIENT_SECRET`
   - Sketch2BIM: `AUTH_GOOGLE_ID` / `AUTH_GOOGLE_SECRET`

3. **Razorpay**: Shared credentials, but plan IDs may differ per project

4. **Security**: Never commit `.env.production` to git (already in `.gitignore`)

## Related Documentation

- [Environment Variables Sync](./ENVIRONMENT_VARIABLES_SYNC.md) - How variables are loaded
- [Database Migration Guide](./DATABASE_MIGRATION_GUIDE.md) - Database setup
- [Migration Guide](./MIGRATION_GUIDE.md) - Application migration

