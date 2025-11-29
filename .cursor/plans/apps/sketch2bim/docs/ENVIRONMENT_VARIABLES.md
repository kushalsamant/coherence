# Environment Variables Reference

This document describes how environment variables are loaded across the Sketch2BIM codebase.

## Configuration

All production environment variables are in app-specific files:
- **Sketch2BIM**: `sketch2bim.env.production` at the repository root
- **ASK**: `ask.env.production` at the repository root
- **Reframe**: `reframe.env.production` at the repository root

Each app loads its own file independently.

## Loading Order

Environment variables are loaded in the following order (later overrides earlier):

1. **App-specific production file** (`sketch2bim.env.production`)
   - Loaded first with `override=False` (doesn't overwrite existing vars)
   - Acts as default values for production

2. **Local development files**
   - `.env` or `.env.local` (backend)
   - `.env.local` (frontend)
   - Loaded with `override=True` (can override shared values)
   - Gitignored - never committed

3. **System environment variables**
   - Platform-provided variables (e.g., Render, Vercel)
   - Highest priority - always override file-based config

## Implementation by File Type

### Backend Configuration

**File**: `backend/app/config.py`

```python
# Load app-specific production environment if available (fallback for local/CI)
WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
APP_ENV_PATH = WORKSPACE_ROOT / "sketch2bim.env.production"
if APP_ENV_PATH.exists():
    load_dotenv(APP_ENV_PATH, override=False)

# Then load local .env (if exists, override=True)
env_file = ".env"
if Path(env_file).exists():
    load_dotenv(env_file, override=True)
```

**Pattern**: App-specific → Local → System env vars

### Frontend Configuration

**File**: `frontend/next.config.js`

```javascript
const appEnvPath = path.resolve(__dirname, '../../sketch2bim.env.production');
if (fs.existsSync(appEnvPath)) {
  dotenv.config({ path: appEnvPath, override: false });
}

// Local .env.local is loaded automatically by Next.js
```

**Pattern**: App-specific → `.env.local` → System env vars

### Scripts

**Pattern**: App-specific → Local (`.env` or `.env.test`) → System env vars

Example from `scripts/create_razorpay_plans.py`:

```python
# Load app-specific production env first (acts as default)
workspace_root = Path(__file__).resolve().parents[2]
app_env_path = workspace_root / "sketch2bim.env.production"
if app_env_path.exists():
    load_dotenv(app_env_path, override=False)

# Then load local .env.test or .env.production for script-specific overrides
env_file = '.env.test' if Path('.env.test').exists() else '.env.production'
load_dotenv(env_file, override=True)
```

### Infrastructure Scripts

Infrastructure setup scripts (e.g., `infra/digitalocean/setup.py`, `infra/hetzner/setup.py`) follow the same pattern:

```python
# Load app-specific production environment first
workspace_root = Path(__file__).resolve().parents[3]
app_env_path = workspace_root / "sketch2bim.env.production"
if app_env_path.exists():
    load_dotenv(app_env_path, override=False)

# Load local .env overrides
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    load_dotenv(env_file, override=True)
```

## Development Setup

### Local Development

For local development:

1. **Backend**: Create `backend/.env` with development overrides
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env with your local values
   ```

2. **Frontend**: Create `frontend/.env.local` with development overrides
   ```bash
   cd frontend
   # Edit .env.local with your local values
   ```

3. **Scripts**: Create `.env.test` or `.env` in script directory for test values

**Important**: Local `.env` files are gitignored and used only for development overrides.

### Production Deployment

In production environments (Render, Vercel, etc.):

- Environment variables should be set directly in the platform's dashboard
- OR the `sketch2bim.env.production` file should be available at the repository root
- Platform-set variables take highest priority

## Testing Environment

For testing, use `.env.test` files:

- Scripts check for `.env.test` first, then fall back to `.env.production`
- Test files should contain test credentials and API keys
- Never commit test credentials to the repository

Example:
```python
env_file = '.env.test' if Path('.env.test').exists() else '.env.production'
load_dotenv(env_file)
```

## Key Environment Variables

### Backend Variables

- `SKETCH2BIM_DATABASE_URL` / `DATABASE_URL` (deprecated) - Supabase PostgreSQL connection string (shared database, prefixed version required)
- `DATABASE_SCHEMA` - Database schema name (default: `sketch2bim_schema`) for schema isolation (no prefix needed, set per-service)
- `SKETCH2BIM_SECRET_KEY` / `SECRET_KEY` (deprecated) - Application secret key (prefixed version required)
- `SKETCH2BIM_BUNNY_ACCESS_KEY` / `BUNNY_ACCESS_KEY` (deprecated) - BunnyCDN storage access key (prefixed version required)
- `SKETCH2BIM_BUNNY_STORAGE_ZONE` / `BUNNY_STORAGE_ZONE` (deprecated) - BunnyCDN storage zone name (prefixed version required)
- `SKETCH2BIM_BUNNY_CDN_HOSTNAME` / `BUNNY_CDN_HOSTNAME` (deprecated) - BunnyCDN CDN hostname (prefixed version required)
- `SKETCH2BIM_RAZORPAY_KEY_ID` / `RAZORPAY_KEY_ID` (deprecated) - Razorpay API credentials (prefixed version required)
- `SKETCH2BIM_RAZORPAY_KEY_SECRET` / `RAZORPAY_KEY_SECRET` (deprecated) - Razorpay API credentials (prefixed version required)
- `SKETCH2BIM_RAZORPAY_WEBHOOK_SECRET` / `RAZORPAY_WEBHOOK_SECRET` (deprecated) - Razorpay webhook secret (prefixed version required)
- `SKETCH2BIM_RAZORPAY_WEEK_AMOUNT` / `RAZORPAY_WEEK_AMOUNT` (deprecated) - Weekly subscription amount in paise (prefixed version required)
- `SKETCH2BIM_RAZORPAY_MONTH_AMOUNT` / `RAZORPAY_MONTH_AMOUNT` (deprecated) - Monthly subscription amount in paise (prefixed version required)
- `SKETCH2BIM_RAZORPAY_YEAR_AMOUNT` / `RAZORPAY_YEAR_AMOUNT` (deprecated) - Yearly subscription amount in paise (prefixed version required)
- `SKETCH2BIM_RAZORPAY_PLAN_WEEK` / `RAZORPAY_PLAN_WEEK` (deprecated) - Weekly subscription plan ID (prefixed version required)
- `SKETCH2BIM_RAZORPAY_PLAN_MONTH` / `RAZORPAY_PLAN_MONTH` (deprecated) - Monthly subscription plan ID (prefixed version required)
- `SKETCH2BIM_RAZORPAY_PLAN_YEAR` / `RAZORPAY_PLAN_YEAR` (deprecated) - Yearly subscription plan ID (prefixed version required)
- `SKETCH2BIM_REDIS_URL` / `REDIS_URL` (deprecated) - Redis connection URL (prefixed version required)

### Frontend Variables

- `SKETCH2BIM_NEXT_PUBLIC_API_URL` / `NEXT_PUBLIC_API_URL` (deprecated) - Backend API URL (prefixed version required)
- `SKETCH2BIM_NEXT_PUBLIC_SITE_URL` / `NEXT_PUBLIC_SITE_URL` (deprecated) - Frontend site URL (prefixed version preferred)
- `SKETCH2BIM_AUTH_SECRET` / `SKETCH2BIM_NEXTAUTH_SECRET` / `AUTH_SECRET` (deprecated) / `NEXTAUTH_SECRET` (deprecated) - NextAuth secret (prefixed version required)
- `SKETCH2BIM_GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_ID` (deprecated) - Google OAuth client ID for Sketch2BIM (prefixed version required)
- `SKETCH2BIM_GOOGLE_SECRET` / `GOOGLE_SECRET` (deprecated) - Google OAuth client secret for Sketch2BIM (prefixed version required)

## Path Resolution

All scripts use consistent path resolution:

- **From backend/app/config.py**: `Path(__file__).resolve().parents[3]` → workspace root
- **From scripts/**: `Path(__file__).resolve().parents[2]` → workspace root
- **From infra/**: `Path(__file__).resolve().parents[3]` → workspace root

The app-specific file is always at: `{workspace_root}/sketch2bim.env.production`

## Best Practices

1. **Never commit secrets**: All `.env`, `.env.local`, `.env.test` files are gitignored
2. **Use app-specific file for production**: Production secrets go in `sketch2bim.env.production`
3. **Override locally**: Use local `.env` files only for development
4. **Platform variables win**: System environment variables always override file-based config
5. **Consistent loading**: All files should follow the app-specific → local → system pattern

## Troubleshooting

### Shared file not found

If the `sketch2bim.env.production` file doesn't exist:
- Scripts will continue with local `.env` files or system env vars
- This is expected in CI/CD environments where env vars are set directly
- No error is raised - the file is optional

### Variable not loading

Check the loading order:
1. Is the variable in the shared file?
2. Is it overridden in local `.env`?
3. Is it set in system environment?
4. System env vars always win

### Database connection issues

If you have database connection issues:
1. Verify `DATABASE_URL` is set correctly (Supabase connection string)
2. Check `DATABASE_SCHEMA` is set to the correct schema (`sketch2bim_schema` for Sketch2BIM)
3. Ensure the schema exists in Supabase (see [DATABASE_MIGRATION_GUIDE.md](../../../docs/DATABASE_MIGRATION_GUIDE.md))
4. Verify connection string uses pooler (port 6543) for production

### Path resolution issues

Ensure scripts are run from the correct directory or use absolute paths:
- Scripts calculate workspace root dynamically
- Works from any directory in the workspace
- Verify `Path(__file__).resolve().parents[N]` correctly finds workspace root

## Related Documentation

- [Testing Guide](./testing.md) - Testing environment setup
- [Deployment Guide](./deployment_checklist.md) - Production deployment
- [README.md](../README.md) - Main project documentation

