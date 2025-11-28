# Database Migration Guide - Supabase with Schemas

## Overview

This guide explains how to set up the shared Supabase PostgreSQL database with separate schemas for ASK and Sketch2BIM applications.

## Current Setup

- **Database Provider**: Supabase
- **Project**: `kvshvl`
- **Database Name**: `postgres` (Supabase default)
- **Connection**: Supabase pooler (port 6543) recommended for production

## Architecture

```
Supabase Project: kvshvl
└── Database: postgres
    ├── Schema: ask_schema (ASK application tables)
    └── Schema: sketch2bim_schema (Sketch2BIM application tables)
```

## Step 1: Create Schemas in Supabase

### Using Supabase SQL Editor

1. Go to [Supabase Dashboard](https://supabase.com/dashboard/org/sjidhixuaozynsncusnw)
2. Select your project: `kvshvl`
3. Navigate to **SQL Editor**
4. Run the following SQL:

```sql
-- Create schemas for each application
CREATE SCHEMA IF NOT EXISTS ask_schema;
CREATE SCHEMA IF NOT EXISTS sketch2bim_schema;

-- Grant necessary permissions
GRANT USAGE ON SCHEMA ask_schema TO postgres;
GRANT USAGE ON SCHEMA sketch2bim_schema TO postgres;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA ask_schema TO postgres;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA sketch2bim_schema TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA ask_schema TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA sketch2bim_schema TO postgres;

-- Set default privileges for future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA ask_schema GRANT ALL ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA sketch2bim_schema GRANT ALL ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA ask_schema GRANT ALL ON SEQUENCES TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA sketch2bim_schema GRANT ALL ON SEQUENCES TO postgres;
```

## Step 2: Create Tables in Each Schema

### ASK Schema Tables

Run the SQL from `database/schemas/ask_schema.sql` in Supabase SQL Editor:

```sql
SET search_path TO ask_schema, public;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    name VARCHAR,
    google_id VARCHAR UNIQUE,
    credits INTEGER DEFAULT 0,
    subscription_tier VARCHAR DEFAULT 'trial',
    subscription_status VARCHAR DEFAULT 'inactive',
    stripe_customer_id VARCHAR UNIQUE,
    subscription_expires_at TIMESTAMP,
    razorpay_subscription_id VARCHAR,
    subscription_auto_renew BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- ... (rest of ask_schema.sql)
```

### Sketch2BIM Schema Tables

Run the SQL from `database/schemas/sketch2bim_schema.sql` in Supabase SQL Editor:

```sql
SET search_path TO sketch2bim_schema, public;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    name VARCHAR,
    google_id VARCHAR UNIQUE,
    credits INTEGER DEFAULT 0,
    subscription_tier VARCHAR DEFAULT 'trial',
    subscription_status VARCHAR DEFAULT 'inactive',
    stripe_customer_id VARCHAR UNIQUE,
    subscription_expires_at TIMESTAMP,
    razorpay_subscription_id VARCHAR,
    subscription_auto_renew BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- ... (rest of sketch2bim_schema.sql)
```

## Step 3: Get Supabase Connection String

1. Go to Supabase Dashboard → Project Settings → Database
2. Under **Connection String**, select **URI** format
3. Copy the connection string (use **Pooler** for production - port 6543)
4. Format: `postgresql://postgres.[PROJECT_REF]:[PASSWORD]@aws-[REGION].pooler.supabase.com:6543/postgres`

### Example Connection String

```
postgresql://postgres.twxudlzipbiavnzcitzb:YOUR_PASSWORD@aws-1-ap-southeast-2.pooler.supabase.com:6543/postgres
```

## Step 4: Configure Render Environment Variables

### For ASK API Service

In Render dashboard → ASK API service → Environment:

1. Set `DATABASE_URL`:
   - Value: Your Supabase connection string (from Step 3)
   - Use pooler URL (port 6543) for production

2. Set `DATABASE_SCHEMA`:
   - Value: `ask_schema`

3. Optional: Set `DATABASE_PASSWORD_OVERRIDE`:
   - If you want to keep password separate from connection string

### For Sketch2BIM Backend Service

In Render dashboard → Sketch2BIM Backend service → Environment:

1. Set `DATABASE_URL`:
   - Value: Your Supabase connection string (from Step 3)
   - Use pooler URL (port 6543) for production

2. Set `DATABASE_SCHEMA`:
   - Value: `sketch2bim_schema`

3. Optional: Set `DATABASE_PASSWORD_OVERRIDE`:
   - If you want to keep password separate from connection string

## Step 5: Verify Schema Isolation

Test that schemas are properly isolated:

```sql
-- Connect to Supabase database
-- Check ASK schema tables
SET search_path TO ask_schema, public;
\dt

-- Check Sketch2BIM schema tables
SET search_path TO sketch2bim_schema, public;
\dt

-- Verify no cross-schema access
SELECT * FROM ask_schema.users;  -- Should work
SELECT * FROM sketch2bim_schema.users;  -- Should work
SELECT * FROM users;  -- Should only show tables from current schema
```

## Step 6: Migrate Existing Data (If Applicable)

If you have existing data in separate databases, you'll need to migrate it:

### Option A: Using pg_dump and psql

```bash
# Export from old database
pg_dump -h old-host -U user -d old_database -n public > old_data.sql

# Import to new schema
psql -h supabase-host -U postgres -d postgres -c "SET search_path TO ask_schema, public;"
psql -h supabase-host -U postgres -d postgres < old_data.sql
```

### Option B: Using Supabase Migration Tool

1. Use Supabase CLI or dashboard migrations
2. Create migration files in `database/migrations/`
3. Run migrations through Supabase dashboard

## Step 7: Update Application Code

The applications are already configured to use schemas via `shared-backend`:

- `apps/ask/api/config.py` - Uses `shared_backend.database.connection.get_database_url` with `schema="ask"`
- `apps/sketch2bim/backend/app/config.py` - Uses `shared_backend.database.connection.get_database_url` with `schema="sketch2bim"`

The `DATABASE_SCHEMA` environment variable is automatically used by the shared backend connection utilities.

## Connection String Formats

### Direct Connection (Development)
```
postgresql://postgres:[PASSWORD]@db.[PROJECT_REF].supabase.co:5432/postgres
```

### Pooler Connection (Production - Recommended)
```
postgresql://postgres.[PROJECT_REF]:[PASSWORD]@aws-[REGION].pooler.supabase.com:6543/postgres
```

**Why use pooler?**
- Better connection management
- Handles connection pooling automatically
- Recommended for serverless/server environments
- Reduces connection overhead

## Troubleshooting

### Schema Not Found Error

If you get "schema does not exist" errors:

1. Verify schemas were created:
   ```sql
   SELECT schema_name FROM information_schema.schemata WHERE schema_name IN ('ask_schema', 'sketch2bim_schema');
   ```

2. Check environment variable `DATABASE_SCHEMA` is set correctly

3. Verify connection string includes correct database name (`postgres`)

### Connection Issues

1. **IPv4 Compatibility**: Supabase direct connections require IPv6. Use pooler (port 6543) if on IPv4-only network
2. **Password**: Ensure password is correctly URL-encoded in connection string
3. **Region**: Verify region in connection string matches your Supabase project region

### Permission Errors

If you get permission errors:

```sql
-- Grant additional permissions if needed
GRANT ALL PRIVILEGES ON SCHEMA ask_schema TO postgres;
GRANT ALL PRIVILEGES ON SCHEMA sketch2bim_schema TO postgres;
```

## Benefits of Schema-Based Approach

1. **Single Database**: One Supabase project, one database
2. **Cost Effective**: No need for multiple database instances
3. **Easy Management**: All data in one place
4. **Schema Isolation**: Tables are logically separated
5. **Shared Resources**: Can share connections, backups, monitoring

## Next Steps

1. ✅ Create schemas in Supabase
2. ✅ Create tables in each schema
3. ✅ Set environment variables in Render
4. ✅ Test schema isolation
5. ⏳ Migrate existing data (if applicable)
6. ⏳ Update application deployments
7. ⏳ Verify all endpoints work correctly

## References

- [Supabase Connection Pooling](https://supabase.com/docs/guides/database/connecting-to-postgres#connection-pooler)
- [PostgreSQL Schemas](https://www.postgresql.org/docs/current/ddl-schemas.html)
- [Shared Backend Database Utilities](../packages/shared-backend/database/connection.py)

