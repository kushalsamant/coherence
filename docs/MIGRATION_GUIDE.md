# Monorepo Migration Guide

## Overview

This guide explains how to complete the migration to the monorepo structure and update applications to use shared packages.

## Prerequisites

- All applications moved to `apps/` directory
- Shared packages created in `packages/` directory
- Shared PostgreSQL database set up

## Step 1: Complete Application Moves

If any applications weren't moved automatically:

```powershell
# Move sketch2bim (if not already moved)
Move-Item -Path sketch2bim -Destination apps/sketch2bim -Force
```

**Note**: If `sketch2bim/` directory cannot be moved automatically (file locked), manually move it:
1. Close any files from `sketch2bim/` that are open in editors
2. Stop any running processes (servers, IDEs, etc.) that might have files open
3. Run the command above or use Windows Explorer to drag and drop the folder

## Step 2: Install Shared Packages

### Backend Packages

```bash
# From monorepo root
cd packages/shared-backend
pip install -e .

# Or using Poetry
poetry install
```

### Frontend Packages

```bash
# From monorepo root
npm install
```

## Step 3: Update ASK Backend

### Update imports in `apps/ask/api/auth.py`:

```python
# OLD
from .config import settings
from .database import get_db
from .models_db import User
from .utils.subscription import calculate_expiry, ensure_subscription_status

# NEW
from shared_backend.config.base import get_settings
from shared_backend.database.connection import get_database_url, create_engine_with_schema
from shared_backend.auth.dependencies import (
    get_current_user_factory,
    get_current_user_optional_factory,
    require_active_subscription_factory,
    is_admin_factory,
)
from shared_backend.subscription import (
    calculate_expiry,
    ensure_subscription_status,
    has_active_subscription,
)
from apps.ask.api.database import get_db  # App-specific database
from apps.ask.api.models_db import User  # App-specific User model

# Create dependencies using factory
get_current_user = get_current_user_factory(
    get_db=get_db,
    UserModel=User,
    calculate_expiry=calculate_expiry,
    ensure_subscription_status=ensure_subscription_status,
)
```

### Update `apps/ask/api/config.py`:

```python
from shared_backend.config.base import BaseSettings
from shared_backend.config.razorpay import RazorpaySettings

class Settings(BaseSettings, RazorpaySettings):
    # App-specific settings
    APP_NAME: str = "ASK: Daily Research"
    # ... rest of settings
```

### Update `apps/ask/api/database.py`:

```python
from shared_backend.database.base import Base
from shared_backend.database.connection import create_engine_with_schema
from .config import settings

# Create engine with schema
engine = create_engine_with_schema(
    settings.database_url,
    schema="ask_schema",  # Use ask_schema
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=settings.DEBUG
)
```

## Step 4: Update Sketch2BIM Backend

Similar updates as ASK, but use `sketch2bim_schema`:

```python
# In apps/sketch2bim/backend/app/database.py
engine = create_engine_with_schema(
    settings.database_url,
    schema="sketch2bim_schema",  # Use sketch2bim_schema
    ...
)
```

## Step 5: Update Reframe

Update `apps/reframe/lib/razorpay.ts`:

```typescript
// OLD
import { verifyWebhookSignature } from '@/lib/razorpay';

// NEW
import { verifyWebhookSignature } from '@kvshvl/shared-frontend/payments';
```

## Step 6: Database Schema Setup

### Using Supabase (Current Setup)

The monorepo uses **Supabase PostgreSQL** with schema-based separation:

- **Database**: `postgres` (Supabase default)
- **Project**: `kvshvl` in Supabase
- **Schemas**: `ask_schema` and `sketch2bim_schema`

### Create Schemas and Tables

**Option 1: Run Complete Migration (Recommended)**
1. Open [Supabase SQL Editor](https://supabase.com/dashboard/project/twxudlzipbiavnzcitzb/sql/new)
2. Copy contents of `database/migrations/RUN_ALL_MIGRATIONS.sql`
3. Paste and run in SQL Editor

**Option 2: Run Individual Migrations**
1. Run `database/migrations/01_create_schemas.sql`
2. Run `database/migrations/02_create_ask_tables.sql`
3. Run `database/migrations/03_create_sketch2bim_tables.sql`

See [DATABASE_MIGRATION_GUIDE.md](../docs/DATABASE_MIGRATION_GUIDE.md) for detailed instructions.

### Update Connection Strings

Set environment variables in Render:

```bash
# Supabase connection string (use pooler for production)
DATABASE_URL=postgresql://postgres.[PROJECT_REF]:[PASSWORD]@aws-[REGION].pooler.supabase.com:6543/postgres

# Schema-specific (required)
DATABASE_SCHEMA=ask_schema  # For ASK API service
DATABASE_SCHEMA=sketch2bim_schema  # For Sketch2BIM backend service
```

Get your connection string from: [Supabase Dashboard](https://supabase.com/dashboard/project/twxudlzipbiavnzcitzb/settings/database)

## Step 7: Migrate Existing Data (If Applicable)

If you have existing data in separate databases, you'll need to migrate it to the new schemas.

### Using pg_dump and psql

```bash
# Export from old database
pg_dump -h old-host -U user -d old_database -n public > old_data.sql

# Import to new schema in Supabase
psql "postgresql://postgres.[PROJECT_REF]:[PASSWORD]@aws-[REGION].pooler.supabase.com:6543/postgres" \
  -c "SET search_path TO ask_schema, public;" \
  -f old_data.sql
```

### Using Supabase Dashboard

1. Use Supabase SQL Editor to run migration queries
2. Or use Supabase CLI for programmatic migrations

**Note**: If you're starting fresh (no existing data), you can skip this step.

## Step 8: Update Deployment Configs

### Render (Backend)

Update `render.yaml` or Render dashboard:

```yaml
services:
  - type: web
    name: ask-api
    env: python
    buildCommand: cd apps/ask/api && pip install -r requirements.txt
    startCommand: cd apps/ask/api && uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        value: postgresql://.../kvshvl_platform
      - key: PYTHONPATH
        value: /opt/render/project/src
```

### Vercel (Frontend)

Update `vercel.json` or Vercel dashboard to point to correct app directories.

## Testing Checklist

- [ ] ASK authentication works
- [ ] Sketch2BIM authentication works
- [ ] Reframe authentication works
- [ ] Payment webhooks work for all apps
- [ ] Cost monitoring works
- [ ] Database schema isolation verified
- [ ] Separate deployments work
- [ ] Domains route correctly

## Rollback Plan

If issues occur:

1. Keep original repositories as backups
2. Revert deployment configs
3. Use original database connections
4. Restore from git history

## Next Steps

### Immediate Actions Required

1. **Complete Sketch2BIM Move** (if not done)
   - Close any open files/processes using sketch2bim
   - Manually move `sketch2bim/` to `apps/sketch2bim/`

2. **Install Shared Packages**
   ```bash
   # From monorepo root
   
   # Backend packages
   cd packages/shared-backend
   pip install -e .
   # Or: poetry install
   
   # Frontend packages (from root)
   npm install
   ```

3. **Update Application Imports**
   - Follow the steps above to update each app
   - Update ASK backend imports
   - Update Sketch2BIM backend imports  
   - Update Reframe frontend imports

4. **Set Up Shared Database**
   ```sql
   -- Connect to PostgreSQL
   CREATE DATABASE kvshvl_platform;
   \c kvshvl_platform;
   
   -- Create schemas
   CREATE SCHEMA ask_schema;
   CREATE SCHEMA sketch2bim_schema;
   
   -- Run schema scripts
   \i database/schemas/ask_schema.sql
   \i database/schemas/sketch2bim_schema.sql
   ```

5. **Update Environment Variables**
   Set in each app's environment:
   ```bash
   # Shared database
   DATABASE_URL=postgresql://user:password@host:5432/kvshvl_platform
   
   # Schema-specific (optional)
   ASK_DATABASE_SCHEMA=ask_schema
   SKETCH2BIM_DATABASE_SCHEMA=sketch2bim_schema
   ```

6. **Test Each Application**
   - Test ASK authentication and payments
   - Test Sketch2BIM authentication and payments
   - Test Reframe authentication and payments
   - Verify cost monitoring works
   - Verify database schema isolation

7. **Update Deployment Configs**
   - Update Render configs for monorepo paths
   - Update Vercel configs for monorepo paths
   - Test deployments
   - Verify domains still work

## Notes

- Factory patterns allow app-specific customization
- Database schemas provide isolation while sharing infrastructure
- Shared packages are versioned independently
- Each app maintains its own deployment pipeline
- All migrations maintain backward compatibility
- App-specific code preserved where needed

