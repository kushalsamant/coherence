-- Create Schemas for Monorepo Applications
-- Run this in Supabase SQL Editor: https://supabase.com/dashboard/project/twxudlzipbiavnzcitzb/sql/new
-- This creates the schemas and sets up permissions

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

-- Verify schemas were created
SELECT schema_name 
FROM information_schema.schemata 
WHERE schema_name IN ('ask_schema', 'sketch2bim_schema')
ORDER BY schema_name;

