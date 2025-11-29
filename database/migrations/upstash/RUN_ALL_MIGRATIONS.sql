-- Complete Database Setup for Upstash Postgres
-- 
-- IMPORTANT: Upstash Postgres uses separate databases (not schemas)
-- Run these migrations in separate databases:
-- 1. ASK database: Run 01_create_ask_tables.sql
-- 2. Sketch2BIM database: Run 02_create_sketch2bim_tables.sql
--
-- This file is for reference only - each database needs its own migration
--
-- Connection strings format:
-- ASK: postgresql://user:password@ask-db.upstash.io:5432/ask
-- Sketch2BIM: postgresql://user:password@sketch2bim-db.upstash.io:5432/sketch2bim
--
-- To run migrations:
-- 1. Connect to ASK database and run: \i database/migrations/upstash/01_create_ask_tables.sql
-- 2. Connect to Sketch2BIM database and run: \i database/migrations/upstash/02_create_sketch2bim_tables.sql
--
-- Or use psql:
-- psql "postgresql://user:password@ask-db.upstash.io:5432/ask" < database/migrations/upstash/01_create_ask_tables.sql
-- psql "postgresql://user:password@sketch2bim-db.upstash.io:5432/sketch2bim" < database/migrations/upstash/02_create_sketch2bim_tables.sql

-- Note: This file does not execute any SQL - it's documentation only
-- Each database migration must be run separately in its respective Upstash Postgres database

SELECT 'Upstash Postgres Migration Guide' as info;
SELECT 'Run migrations separately for each database' as instruction;

