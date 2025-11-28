# Environment Variables Synchronization Status

This document tracks the synchronization of all codebases with the shared `.env.production` file.

## Shared File Location

**Path**: `../kushalsamant.github.io/.env.production`

This file contains environment variables for all codebases:
- ASK (backend and frontend)
- Sketch2BIM (backend and frontend)
- Reframe (frontend)

## Verification Status

### ✅ Sketch2BIM Backend
**File**: `sketch2bim/backend/app/config.py`
- ✅ Loads shared `.env.production` first
- ✅ Path resolution: `Path(__file__).resolve().parents[3]` → workspace root → shared file
- ✅ Falls back to local `.env` with override

**Status**: Fully configured

### ✅ Sketch2BIM Frontend
**File**: `sketch2bim/frontend/next.config.js`
- ✅ Loads shared `.env.production` first
- ✅ Path resolution: `../../kushalsamant.github.io/.env.production`
- ✅ Falls back to `.env.local` with override

**Status**: Fully configured

### ✅ ASK Backend
**File**: `ask/api/config.py`
- ✅ Loads shared `.env.production` first
- ✅ Path resolution: `BASE_DIR.parent / "kushalsamant.github.io" / ".env.production"`
- ✅ Falls back to `ask.env` with override (via Pydantic Settings)

**Status**: Fully configured

### ✅ ASK Frontend
**File**: `ask/frontend/next.config.ts`
- ✅ Loads shared `.env.production` first
- ✅ Path resolution: `../../kushalsamant.github.io/.env.production`
- ✅ Falls back to `.env.local` with override

**Status**: Fully configured

### ✅ Reframe Frontend
**File**: `reframe/next.config.js`
- ✅ Loads shared `.env.production` first
- ✅ Path resolution: `../kushalsamant.github.io/.env.production`
- ✅ Falls back to `.env.local` with override

**Status**: Fully configured

## Variable Sections in Shared File

The shared `.env.production` file is organized into sections:

1. **FRONTEND VARIABLES** - For Sketch2BIM Vercel deployment
2. **BACKEND VARIABLES** - For Sketch2BIM Render deployment
3. **ASK Backend Environment Variables** - For ASK Render deployment

All sections are loaded by all codebases, but each codebase only uses the variables it needs.

## Loading Order (Consistent Across All Codebases)

1. **Shared production file** (`../kushalsamant.github.io/.env.production`)
   - Loaded with `override=False`
   - Acts as global fallback/default values

2. **Local development files**
   - Backend: `.env`, `ask.env`, etc.
   - Frontend: `.env.local`
   - Loaded with `override=True`
   - Gitignored - never committed

3. **System environment variables**
   - Platform-provided (Render, Vercel)
   - Highest priority - always override

## Documentation

- ✅ `ask/docs/ENVIRONMENT_VARIABLES.md` - Comprehensive mapping document
- ✅ `sketch2bim/docs/ENVIRONMENT_VARIABLES.md` - Sketch2BIM specific guide
- ✅ `ask/ENV_VARIABLES.md` - ASK deployment reference
- ✅ `ask/README.md` - Mentions centralized config
- ✅ `reframe/readme.md` - Mentions centralized config
- ✅ `sketch2bim/README.md` - Mentions centralized config

## Scripts

All utility scripts also load the shared file:
- ✅ `scripts/create_razorpay_plans.py`
- ✅ `scripts/delete_razorpay_plan.py`
- ✅ `infra/digitalocean/setup.py`
- ✅ `infra/hetzner/setup.py`
- ✅ `scripts/reorganize-env-production.ps1` (works with shared file)
- ✅ `scripts/reorganize-env.ps1` (works with shared file)

## Verification Test

To verify variables are loading correctly:

### ASK Backend
```bash
cd ask
python -c "from api.config import settings; print('Config loaded:', settings.APP_NAME)"
```

### Sketch2BIM Backend
```bash
cd sketch2bim/backend
python -c "from app.config import settings; print('Config loaded:', settings.APP_NAME)"
```

### Frontend (Next.js)
Next.js automatically loads environment variables. Check by running:
```bash
npm run dev
```

And accessing variables via `process.env.VARIABLE_NAME`.

## Notes

- All codebases use consistent loading pattern
- Path resolution works from any directory
- Error handling: Shared file is optional (no error if missing)
- Production deployments can use platform env vars instead of file
- Local development always uses file-based config with overrides

## Last Updated

December 2024 - All codebases verified and synchronized.

