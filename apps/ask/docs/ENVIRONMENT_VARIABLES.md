# Environment Variables Reference

This document describes how environment variables are loaded across all codebases and maps which variables belong to which project.

## Configuration

All production environment variables are in app-specific files:
- **ASK**: `ask.env.production` at the repository root
- **Sketch2BIM**: `sketch2bim.env.production` at the repository root
- **Reframe**: `reframe.env.production` at the repository root

Each app loads its own file independently.

## Variable Mapping by Codebase

### ASK Backend Variables

**Location in file**: Section marked "# ASK - BACKEND VARIABLES" in `ask.env.production`

**Variables used by ASK backend** (`ask/api/config.py`):
- `ASK_API_HOST` / `API_HOST` (deprecated) - API host (default: 0.0.0.0, prefixed version preferred)
- `ASK_API_PORT` / `API_PORT` (deprecated) - API port (default: 8000, prefixed version preferred)
- `ASK_CORS_ORIGINS` / `CORS_ORIGINS` (deprecated) - Allowed CORS origins (comma-separated, prefixed version required)
- `ASK_LOG_CSV_FILE` / `LOG_CSV_FILE` (deprecated) - CSV log file path (default: log.csv, prefixed version preferred)
- `ASK_LOG_DIR` / `LOG_DIR` (deprecated) - Log directory (default: logs, prefixed version preferred)
- `ASK_PYTHONPATH` / `PYTHONPATH` (deprecated) - Python path (default: ., prefixed version preferred)
- `ASK_ENVIRONMENT` / `ENVIRONMENT` (deprecated) - Environment name (production/development, prefixed version preferred)
- `ASK_DATABASE_URL` / `DATABASE_URL` (deprecated) - Supabase PostgreSQL connection string (shared database, prefixed version required)
- `DATABASE_SCHEMA` - Database schema name (default: `ask_schema`) for schema isolation (no prefix needed, set per-service)
- `ASK_GROQ_API_KEY` / `GROQ_API_KEY` (deprecated) - Groq API key for AI processing (prefixed version preferred)
- `ASK_RAZORPAY_KEY_ID` / `RAZORPAY_KEY_ID` / `LIVE_KEY_ID` (deprecated) - Razorpay key ID (prefixed version required)
- `ASK_RAZORPAY_KEY_SECRET` / `RAZORPAY_KEY_SECRET` / `LIVE_KEY_SECRET` (deprecated) - Razorpay key secret (prefixed version required)
- `ASK_RAZORPAY_WEBHOOK_SECRET` / `RAZORPAY_WEBHOOK_SECRET` (deprecated) - Razorpay webhook secret (prefixed version required)
- `ASK_RAZORPAY_WEEK_AMOUNT` / `RAZORPAY_WEEK_AMOUNT` (deprecated) - Weekly subscription amount in paise (prefixed version required)
- `ASK_RAZORPAY_MONTH_AMOUNT` / `RAZORPAY_MONTH_AMOUNT` (deprecated) - Monthly subscription amount in paise (prefixed version required)
- `ASK_RAZORPAY_YEAR_AMOUNT` / `RAZORPAY_YEAR_AMOUNT` (deprecated) - Yearly subscription amount in paise (prefixed version required)
- `ASK_RAZORPAY_PLAN_WEEK` / `RAZORPAY_PLAN_WEEK` (deprecated) - Weekly subscription plan ID (prefixed version required)
- `ASK_RAZORPAY_PLAN_MONTH` / `RAZORPAY_PLAN_MONTH` (deprecated) - Monthly subscription plan ID (prefixed version required)
- `ASK_RAZORPAY_PLAN_YEAR` / `RAZORPAY_PLAN_YEAR` (deprecated) - Yearly subscription plan ID (prefixed version required)
- `ASK_AUTH_SECRET` / `ASK_NEXTAUTH_SECRET` / `NEXTAUTH_SECRET` (deprecated) / `AUTH_SECRET` (deprecated) - NextAuth signing secret for JWT verification (prefixed version preferred)
- `ASK_AUTH_URL` / `AUTH_URL` (deprecated) / `NEXTAUTH_URL` (deprecated) - URL configured for NextAuth callbacks (prefixed version preferred)
- `ASK_JWT_ALGORITHM` / `JWT_ALGORITHM` (deprecated) - JWT algorithm (default: HS256, prefixed version preferred)
- `ASK_FRONTEND_URL` / `FRONTEND_URL` (deprecated) - Frontend URL for CORS and redirects (prefixed version required)

### Sketch2BIM Backend Variables

**Location in shared file**: Section marked "# BACKEND VARIABLES"

**Variables used by Sketch2BIM backend** (`sketch2bim/backend/app/config.py`):
- `SKETCH2BIM_DATABASE_URL` / `DATABASE_URL` (deprecated) - PostgreSQL database URL (prefixed version required)
- `SKETCH2BIM_SECRET_KEY` / `SECRET_KEY` (deprecated) - Application secret key (prefixed version required)
- `SKETCH2BIM_BUNNY_ACCESS_KEY` / `BUNNY_ACCESS_KEY` (deprecated) - BunnyCDN storage access key (prefixed version required)
- `SKETCH2BIM_BUNNY_STORAGE_ZONE` / `BUNNY_STORAGE_ZONE` (deprecated) - BunnyCDN storage zone name (prefixed version required)
- `SKETCH2BIM_BUNNY_CDN_HOSTNAME` / `BUNNY_CDN_HOSTNAME` (deprecated) - BunnyCDN CDN hostname (prefixed version required)
- `SKETCH2BIM_BUNNY_REGION` / `BUNNY_REGION` (deprecated) - BunnyCDN region (prefixed version preferred)
- `SKETCH2BIM_BUNNY_SIGNED_URL_KEY` / `BUNNY_SIGNED_URL_KEY` (deprecated) - BunnyCDN signed URL key (optional, prefixed version preferred)
- `SKETCH2BIM_REDIS_URL` / `REDIS_URL` (deprecated) - Redis connection URL (prefixed version required)
- `SKETCH2BIM_RAZORPAY_KEY_ID` / `RAZORPAY_KEY_ID` (deprecated) / `LIVE_KEY_ID` (deprecated) - Razorpay credentials (prefixed version required)
- `SKETCH2BIM_RAZORPAY_KEY_SECRET` / `RAZORPAY_KEY_SECRET` (deprecated) / `LIVE_KEY_SECRET` (deprecated) - Razorpay credentials (prefixed version required)
- `SKETCH2BIM_RAZORPAY_WEBHOOK_SECRET` / `RAZORPAY_WEBHOOK_SECRET` (deprecated) - Razorpay webhook secret (prefixed version required)
- `SKETCH2BIM_RAZORPAY_PLAN_WEEK` / `RAZORPAY_PLAN_WEEK` (deprecated) - Weekly plan ID (prefixed version required)
- `SKETCH2BIM_RAZORPAY_PLAN_MONTH` / `RAZORPAY_PLAN_MONTH` (deprecated) - Monthly plan ID (prefixed version required)
- `SKETCH2BIM_RAZORPAY_PLAN_YEAR` / `RAZORPAY_PLAN_YEAR` (deprecated) - Yearly plan ID (prefixed version required)
- `SKETCH2BIM_ALLOWED_ORIGINS` / `ALLOWED_ORIGINS` (deprecated) - CORS allowed origins (prefixed version required)
- `SKETCH2BIM_APP_ENV` / `APP_ENV` (deprecated) - Application environment (prefixed version preferred)
- `SKETCH2BIM_LOG_LEVEL` / `LOG_LEVEL` (deprecated) - Logging level (prefixed version preferred)
- `SKETCH2BIM_MAX_UPLOAD_SIZE_MB` / `MAX_UPLOAD_SIZE_MB` (deprecated) - Maximum upload size (prefixed version preferred)
- `SKETCH2BIM_FRONTEND_URL` / `FRONTEND_URL` (deprecated) - Frontend URL (prefixed version required)

### Sketch2BIM Frontend Variables

**Location in shared file**: Section marked "# FRONTEND VARIABLES"

**Variables used by Sketch2BIM frontend** (`sketch2bim/frontend/next.config.js`):
- `SKETCH2BIM_NEXT_PUBLIC_API_URL` / `NEXT_PUBLIC_API_URL` (deprecated) - Backend API URL (prefixed version required)
- `SKETCH2BIM_NEXT_PUBLIC_FREE_LIMIT` / `NEXT_PUBLIC_FREE_LIMIT` (deprecated) - Free tier limit (prefixed version preferred)
- `SKETCH2BIM_AUTH_URL` / `AUTH_URL` (deprecated) - Authentication URL (prefixed version preferred)
- `SKETCH2BIM_AUTH_SECRET` / `AUTH_SECRET` (deprecated) / `SKETCH2BIM_NEXTAUTH_SECRET` / `NEXTAUTH_SECRET` (deprecated) - NextAuth secret (prefixed version required)
- `SKETCH2BIM_GOOGLE_CLIENT_ID` / `ASK_GOOGLE_CLIENT_ID` (deprecated) - Google OAuth client ID for Sketch2BIM (prefixed version required)
- `SKETCH2BIM_GOOGLE_SECRET` / `ASK_GOOGLE_SECRET` (deprecated) - Google OAuth client secret for Sketch2BIM (prefixed version required)

### Reframe Variables

**Location in shared file**: Uses variables from various sections

**Variables potentially used by Reframe** (`reframe/next.config.js`):
- `REFRAME_GOOGLE_CLIENT_ID` - Google OAuth client ID for Reframe (prefixed version required)
- `REFRAME_GOOGLE_SECRET` - Google OAuth client secret for Reframe (prefixed version required)
- `REFRAME_API_URL` / `REFRAME_NEXT_PUBLIC_API_URL` - Backend API URL (prefixed version required)
- `REFRAME_AUTH_SECRET` / `REFRAME_NEXTAUTH_SECRET` - NextAuth secret (prefixed version required)
- `REFRAME_GROQ_API_KEY` - Groq API key (prefixed version required)
- `REFRAME_UPSTASH_REDIS_REST_URL` - Upstash Redis REST URL (prefixed version required)
- `REFRAME_UPSTASH_REDIS_REST_TOKEN` - Upstash Redis REST token (prefixed version required)
- Other frontend variables as needed (all with `REFRAME_` prefix)

## Loading Pattern

All codebases follow this loading order:

1. **App-specific production file** (`ask.env.production`)
   - Loaded first with `override=False`
   - Acts as default values for production

2. **Local development files**
   - ASK backend: `ask.env` or `.env.local`
   - Sketch2BIM backend: `.env`
   - Frontend projects: `.env.local`
   - Loaded with `override=True` (can override shared values)
   - Gitignored - never committed

3. **System environment variables**
   - Platform-provided variables (e.g., Render, Vercel)
   - Highest priority - always override file-based config

## Implementation Details

### ASK Backend

**File**: `ask/api/config.py`

```python
# Load app-specific .env.production
BASE_DIR = Path(__file__).resolve().parents[2]  # Go up from api/config.py to ask/
APP_ENV_PATH = BASE_DIR.parent / "ask.env.production"
if APP_ENV_PATH.exists():
    load_dotenv(APP_ENV_PATH, override=False)

# Then Pydantic Settings loads ask.env (if exists) with override=True
class Settings(BaseSettings):
    class Config:
        env_file = "ask.env"
```

**Path Resolution**: `ask/api/config.py` → `ask/` → `GitHub/` → `ask.env.production`

### Sketch2BIM Backend

**File**: `sketch2bim/backend/app/config.py`

```python
# Load app-specific production environment if available
WORKSPACE_ROOT = Path(__file__).resolve().parents[3]  # Go up to workspace root
APP_ENV_PATH = WORKSPACE_ROOT / "sketch2bim.env.production"
if APP_ENV_PATH.exists():
    load_dotenv(APP_ENV_PATH, override=False)

# Then Pydantic Settings loads .env (if exists) with override=True
class Settings(BaseSettings):
    class Config:
        env_file = ".env"
```

**Path Resolution**: `sketch2bim/backend/app/config.py` → `sketch2bim/backend/app/` → `sketch2bim/backend/` → `sketch2bim/` → `GitHub/` → `sketch2bim.env.production`

### Sketch2BIM Frontend

**File**: `sketch2bim/frontend/next.config.js`

```javascript
const appEnvPath = path.resolve(__dirname, '../../sketch2bim.env.production');
if (fs.existsSync(appEnvPath)) {
  dotenv.config({ path: appEnvPath, override: false });
}
// Next.js automatically loads .env.local with override=True
```

**Path Resolution**: `sketch2bim/frontend/next.config.js` → `sketch2bim/frontend/` → `sketch2bim/` → `GitHub/` → `sketch2bim.env.production`

### Reframe Frontend

**File**: `reframe/next.config.js`

```javascript
const appEnvPath = path.resolve(__dirname, "../reframe.env.production");
if (fs.existsSync(appEnvPath)) {
  dotenv.config({ path: appEnvPath, override: false });
}
// Next.js automatically loads .env.local with override=True
```

**Path Resolution**: `reframe/next.config.js` → `reframe/` → `GitHub/` → `reframe.env.production`

## Variable Conflicts

Some variables are shared across codebases but may have different values:
- `DATABASE_URL` - Shared Supabase PostgreSQL database (same connection string), but uses different schemas (`ask_schema` vs `sketch2bim_schema`) via `DATABASE_SCHEMA` environment variable
- `RAZORPAY_*` - Shared payment gateway, but may have different plan IDs
- `REDIS_URL` - May be shared or separate instances

**Resolution**: Each codebase's local `.env` file can override shared values as needed. For database, use `DATABASE_SCHEMA` to specify which schema to use within the shared database.

## Development Setup

### Local Development

1. **ASK Backend**: Create `ask.env` or `ask/.env.local` with development overrides
2. **Sketch2BIM Backend**: Create `sketch2bim/backend/.env` with development overrides
3. **Frontend Projects**: Create `.env.local` files with development overrides

**Important**: Local env files are gitignored and used only for development.

### Production Deployment

In production (Render, Vercel):
- Environment variables should be set directly in the platform dashboard
- OR the `ask.env.production` file should be available at the repository root
- Platform-set variables take highest priority

## Adding New Variables

When adding new environment variables:

1. **Add to app-specific file**: `ask.env.production` at the repository root
   - Add in the appropriate section (ASK, Sketch2BIM Backend, Sketch2BIM Frontend)
   - Include comments explaining the variable

2. **Update codebase config**:
   - Add variable to Settings class in backend config files
   - Or use `process.env.VARIABLE_NAME` directly in frontend

3. **Update documentation**:
   - Update this file with the new variable
   - Document which codebase uses it

## Troubleshooting

### Variable not loading

Check the loading order:
1. Is the variable in `ask.env.production`?
2. Is it overridden in local `.env` files?
3. Is it set in system environment?
4. System env vars always win

### Path resolution issues

Verify path resolution works from the codebase directory:
- ASK: `ask/api/config.py` → `ask.env.production`
- Sketch2BIM: `sketch2bim/backend/app/config.py` → `sketch2bim.env.production`
- Frontend: `next.config.js` → `{app}.env.production`

### Database connection issues

If you have database connection issues:
1. Verify `DATABASE_URL` is set correctly (Supabase connection string)
2. Check `DATABASE_SCHEMA` is set to the correct schema (`ask_schema` for ASK)
3. Ensure the schema exists in Supabase (see [DATABASE_MIGRATION_GUIDE.md](../../../docs/DATABASE_MIGRATION_GUIDE.md))
4. Verify connection string uses pooler (port 6543) for production

### Shared file not found

If the shared file doesn't exist:
- Scripts continue with local `.env` files or system env vars
- Expected in CI/CD where env vars are set directly
- No error is raised - the file is optional

## Related Documentation

- [Sketch2BIM Environment Variables](../sketch2bim/docs/ENVIRONMENT_VARIABLES.md)
- [ASK ENV_VARIABLES.md](../ENV_VARIABLES.md)
- [Deployment Guides](../DEPLOYMENT.md)

