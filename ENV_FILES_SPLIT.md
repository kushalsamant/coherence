# Environment Files Split Documentation

## Overview

Environment variables have been split into separate frontend and backend files for better security and organization.

## File Structure

### Platform Repo (`kushalsamant.github.io`)

- **Frontend Files:**
  - `.env.local.frontend` - Local development frontend variables (NEXT_PUBLIC_*)
  - `.env.production.frontend` - Production frontend variables (NEXT_PUBLIC_*)

- **Backend Files:**
  - `.env.local.backend` - Local development backend variables (PLATFORM_*)
  - `.env.production.backend` - Production backend variables (PLATFORM_*)

### Sketch2BIM Repo (`sketch2bim`)

- **Frontend Files:**
  - `.env.local.frontend` - Local development frontend variables (NEXT_PUBLIC_*)
  - `.env.production.frontend` - Production frontend variables (NEXT_PUBLIC_*)

- **Backend Files:**
  - `.env.local.backend` - Local development backend variables (SKETCH2BIM_*, PLATFORM_*)
  - `.env.production.backend` - Production backend variables (SKETCH2BIM_*, PLATFORM_*)

## Variable Categorization

### Frontend Variables (`.env.*.frontend`)

These variables are **exposed to the browser** and should only contain public, non-sensitive data:

- `NEXT_PUBLIC_*` - All Next.js public environment variables
- Examples:
  - `NEXT_PUBLIC_SUPABASE_URL`
  - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
  - `NEXT_PUBLIC_SITE_URL`
  - `NEXT_PUBLIC_PLATFORM_API_URL`
  - `NEXT_PUBLIC_GA_ID` (optional analytics)

### Backend Variables (`.env.*.backend`)

These variables are **server-side only** and can contain secrets:

- `PLATFORM_*` - Platform-wide backend configuration
- `SKETCH2BIM_*` - Sketch2BIM-specific backend configuration
- Secrets and sensitive data:
  - `SUPABASE_SERVICE_ROLE_KEY`
  - `PLATFORM_DATABASE_URL`
  - `PLATFORM_RAZORPAY_KEY_SECRET`
  - `PLATFORM_NEXTAUTH_SECRET`
  - `PLATFORM_AUTH_SECRET`
  - API keys (GROQ, OPENAI, etc.)

## Migration Guide

### Step 1: Split Existing Files

If you have existing `.env.local` or `.env.production` files, split them using the provided script:

**Platform Repo:**
```bash
cd kushalsamant.github.io
node scripts/split-env-files.js .env.local
node scripts/split-env-files.js .env.production
```

**Sketch2BIM Repo:**
```bash
cd sketch2bim
node scripts/split-env-files.js .env.local
node scripts/split-env-files.js .env.production
```

### Step 2: Verify Split Files

Check that the split files were created correctly:
- `.env.local.frontend` should contain only `NEXT_PUBLIC_*` variables
- `.env.local.backend` should contain `PLATFORM_*` and other server-side variables

### Step 3: Test Locally

1. **Frontend (Next.js):**
   ```bash
   npm run dev
   ```
   The frontend will automatically load `.env.local.frontend` (or `.env.production.frontend` in production mode).

2. **Backend (FastAPI):**
   ```bash
   # Platform API
   cd apps/platform-api
   python main.py
   
   # Sketch2BIM API
   cd sketch2bim
   python main.py
   ```
   The backend will automatically load `.env.local.backend` (or `.env.production.backend` in production mode).

### Step 4: Update Deployment Platforms

#### Vercel (Frontend)

1. Go to your Vercel project dashboard
2. Navigate to Settings → Environment Variables
3. Add/update variables from `.env.production.frontend`
4. Only `NEXT_PUBLIC_*` variables should be set here

#### Render (Backend)

1. Go to your Render service dashboard
2. Navigate to Environment tab
3. Add/update variables from `.env.production.backend`
4. Use the `prepare_render_env.py` script to generate a checklist:
   ```bash
   python scripts/prepare_render_env.py
   ```

### Step 5: Clean Up (Optional - Manual)

After verifying everything works, you can manually remove or rename the original files if desired:
- Original files are kept as backup by default
- You can delete them manually when ready: `.env.local` and `.env.production`
- Or rename them as backup: `.env.local.old`, `.env.production.old`

## Configuration Details

### Next.js Configuration

The `next.config.js` files have been updated to load frontend environment files:

```javascript
const dotenv = require('dotenv');
const path = require('path');

const envFile = process.env.NODE_ENV === 'production' 
  ? '.env.production.frontend' 
  : '.env.local.frontend';

dotenv.config({ path: path.resolve(__dirname, envFile) });
```

### FastAPI/Pydantic Configuration

The backend config files (`core/config.py` and `config/sketch2bim.py`) have been updated to load backend environment files:

```python
_env_file = ".env.local.backend"
if os.getenv("PLATFORM_ENVIRONMENT", "").lower() == "production":
    _env_file = ".env.production.backend"

model_config = SettingsConfigDict(
    env_file=_env_file,
    ...
)
```

## Security Notes

1. **Never commit `.env*` files** - They are already in `.gitignore`
2. **Frontend variables are public** - Anything with `NEXT_PUBLIC_*` is exposed to the browser
3. **Backend variables are secret** - Never expose `PLATFORM_*` or other backend variables to the frontend
4. **Use template files** - Reference `platform.env.template` for structure, but never commit actual values

## Troubleshooting

### Frontend not loading variables

- Check that `.env.local.frontend` exists in the project root
- Verify `dotenv` is installed: `npm list dotenv`
- Check `next.config.js` is loading the correct file

### Backend not loading variables

- Check that `.env.local.backend` exists in the project root
- Verify the environment detection logic in config files
- Check that `PLATFORM_ENVIRONMENT` or `NODE_ENV` is set correctly

### Variables missing after split

- Re-run the split script to regenerate files
- Manually check that variables are in the correct file (frontend vs backend)
- Verify variable names match the categorization rules

## Additional Resources

- [Next.js Environment Variables](https://nextjs.org/docs/basic-features/environment-variables)
- [Pydantic Settings](https://docs.pydantic.dev/latest/usage/settings/)
- Template file: `platform.env.template` (for reference only)

