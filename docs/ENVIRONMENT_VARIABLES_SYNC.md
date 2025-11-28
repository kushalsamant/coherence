# Environment Variables Synchronization Status

This document tracks how environment variables are loaded across all codebases.

## File Structure

**App-Specific Environment Files:**
- **ASK**: `ask.env.production` - Located at repository root
- **Reframe**: `reframe.env.production` - Located at repository root
- **Sketch2BIM**: `sketch2bim.env.production` - Located at repository root

Each app loads its own `.env.production` file, which serves as:
- **Deployment templates** with clear instructions for copying to Vercel/Render
- **App-specific organization** for easier reference
- **Source of truth** for each app's production variables

**Loading Order:**
1. App-specific `.env.production` file (if exists)
2. Local development files (`.env.local`, `.env`, etc.) - can override
3. System environment variables (platform-provided) - highest priority

## Verification Status

### ✅ Sketch2BIM Backend
**File**: `sketch2bim/backend/app/config.py`
- ✅ Loads `sketch2bim.env.production` first
- ✅ Path resolution: `Path(__file__).resolve().parents[3]` → workspace root → `sketch2bim.env.production`
- ✅ Falls back to local `.env` with override

**Status**: Fully configured

### ✅ Sketch2BIM Frontend
**File**: `sketch2bim/frontend/next.config.js`
- ✅ Loads `sketch2bim.env.production` first
- ✅ Path resolution: `../../sketch2bim.env.production`
- ✅ Falls back to `.env.local` with override

**Status**: Fully configured

### ✅ ASK Backend
**File**: `ask/api/config.py`
- ✅ Loads `ask.env.production` first
- ✅ Path resolution: `BASE_DIR.parent / "ask.env.production"`
- ✅ Falls back to `ask.env` with override (via Pydantic Settings)

**Status**: Fully configured

### ✅ ASK Frontend
**File**: `ask/frontend/next.config.ts`
- ✅ Loads `ask.env.production` first
- ✅ Path resolution: `../../ask.env.production`
- ✅ Falls back to `.env.local` with override

**Status**: Fully configured

### ✅ Reframe Frontend
**File**: `reframe/next.config.js`
- ✅ Loads `reframe.env.production` first
- ✅ Path resolution: `../reframe.env.production`
- ✅ Falls back to `.env.local` with override

**Status**: Fully configured

### ✅ Reframe Backend
**File**: `reframe/backend/app/config.py`
- ✅ Loads `reframe.env.production` first
- ✅ Path resolution: `Path(__file__).resolve().parents[3]` → workspace root → `reframe.env.production`
- ✅ Falls back to system environment variables

**Status**: Fully configured

## Variable Organization

Each app-specific `.env.production` file is organized into sections:

1. **FRONTEND VARIABLES** - For Vercel deployment
2. **BACKEND VARIABLES** - For Render deployment

Each app only loads its own file, ensuring clean separation of concerns.

## Loading Order (Consistent Across All Codebases)

1. **App-specific production file** (`{app}.env.production`)
   - Loaded with `override=False`
   - Acts as default values for production

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
- Error handling: App-specific file is optional (no error if missing)
- Production deployments can use platform env vars instead of file
- Local development always uses file-based config with overrides
- Each app is independent - no shared file dependencies

## Last Updated

December 2024 - All codebases verified and synchronized.

