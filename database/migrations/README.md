# Database Migrations

This directory contains SQL migration scripts for setting up the shared Supabase PostgreSQL database with separate schemas.

## Quick Start

**Easiest way**: Run the complete migration in one go:

1. Open [Supabase SQL Editor](https://supabase.com/dashboard/project/twxudlzipbiavnzcitzb/sql/new)
2. Copy and paste the entire contents of `RUN_ALL_MIGRATIONS.sql`
3. Click "Run" to execute
4. Verify the output shows all schemas and tables were created

## Migration Files

### `RUN_ALL_MIGRATIONS.sql` ⭐ **RECOMMENDED**
Complete migration that creates everything in one go. Use this for initial setup.

### Individual Migration Files

If you prefer to run migrations step by step:

1. **`01_create_schemas.sql`** - Creates `ask_schema` and `sketch2bim_schema`
2. **`02_create_ask_tables.sql`** - Creates tables in `ask_schema`
3. **`03_create_sketch2bim_tables.sql`** - Creates tables in `sketch2bim_schema`

## How to Run

### Option 1: Supabase SQL Editor (Recommended)

1. Go to [Supabase Dashboard](https://supabase.com/dashboard/org/sjidhixuaozynsncusnw)
2. Select project: **kvshvl**
3. Navigate to **SQL Editor** → **New Query**
4. Copy the SQL from `RUN_ALL_MIGRATIONS.sql`
5. Paste and click **Run**
6. Check the results to verify all schemas and tables were created

### Option 2: Supabase CLI

```bash
# Install Supabase CLI if not already installed
npm install -g supabase

# Login to Supabase
supabase login

# Link to your project
supabase link --project-ref twxudlzipbiavnzcitzb

# Run migrations
supabase db push
```

### Option 3: psql Command Line

```bash
# Connect to Supabase
psql "postgresql://postgres.twxudlzipbiavnzcitzb:[PASSWORD]@aws-1-ap-southeast-2.pooler.supabase.com:6543/postgres"

# Run migration
\i database/migrations/RUN_ALL_MIGRATIONS.sql
```

## Verification

After running migrations, verify everything was created:

```sql
-- Check schemas
SELECT schema_name 
FROM information_schema.schemata 
WHERE schema_name IN ('ask_schema', 'sketch2bim_schema');

-- Check ASK tables
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'ask_schema';

-- Check Sketch2BIM tables
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'sketch2bim_schema';
```

Expected results:
- **Schemas**: `ask_schema`, `sketch2bim_schema`
- **ASK tables**: `users`, `payments`, `groq_usage`
- **Sketch2BIM tables**: `users`, `payments`, `jobs`

## Troubleshooting

### "Schema already exists" Error
This is fine - the `IF NOT EXISTS` clause prevents errors. The schema was already created.

### "Table already exists" Error
This is fine - the `IF NOT EXISTS` clause prevents errors. The table was already created.

### Permission Errors
If you get permission errors, ensure you're running as the `postgres` user or have been granted the necessary permissions.

### Connection Issues
- Use the **pooler** connection string (port 6543) for better compatibility
- Ensure your IP is allowed in Supabase dashboard → Settings → Database → Connection Pooling

## Next Steps

After running migrations:

1. ✅ Set `DATABASE_URL` in Render environment variables (Supabase connection string)
2. ✅ Set `DATABASE_SCHEMA=ask_schema` for ASK API service
3. ✅ Set `DATABASE_SCHEMA=sketch2bim_schema` for Sketch2BIM backend service
4. ✅ Test connections from your applications
5. ✅ Migrate existing data (if applicable)

## References

- [Supabase SQL Editor](https://supabase.com/dashboard/project/twxudlzipbiavnzcitzb/sql/new)
- [Database Migration Guide](../docs/DATABASE_MIGRATION_GUIDE.md)
- [Supabase Connection Pooling](https://supabase.com/docs/guides/database/connecting-to-postgres#connection-pooler)
