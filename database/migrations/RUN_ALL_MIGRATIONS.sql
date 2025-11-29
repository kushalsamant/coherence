-- Complete Database Setup for Monorepo
-- Run this entire file in Supabase SQL Editor in one go
-- URL: https://supabase.com/dashboard/project/twxudlzipbiavnzcitzb/sql/new
-- 
-- This file combines all migrations:
-- 1. Creates schemas
-- 2. Creates ASK tables
-- 3. Creates Sketch2BIM tables

-- ============================================================================
-- STEP 1: Create Schemas
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS ask_schema;
CREATE SCHEMA IF NOT EXISTS sketch2bim_schema;

GRANT USAGE ON SCHEMA ask_schema TO postgres;
GRANT USAGE ON SCHEMA sketch2bim_schema TO postgres;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA ask_schema TO postgres;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA sketch2bim_schema TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA ask_schema TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA sketch2bim_schema TO postgres;

ALTER DEFAULT PRIVILEGES IN SCHEMA ask_schema GRANT ALL ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA sketch2bim_schema GRANT ALL ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA ask_schema GRANT ALL ON SEQUENCES TO postgres;
ALTER DEFAULT PRIVILEGES IN SCHEMA sketch2bim_schema GRANT ALL ON SEQUENCES TO postgres;

-- ============================================================================
-- STEP 2: Create ASK Schema Tables
-- ============================================================================

SET search_path TO ask_schema, public;

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    name VARCHAR,
    google_id VARCHAR UNIQUE,
    credits INTEGER DEFAULT 0,
    subscription_tier VARCHAR DEFAULT 'trial',
    subscription_status VARCHAR DEFAULT 'inactive',
    razorpay_customer_id VARCHAR UNIQUE,
    subscription_expires_at TIMESTAMP,
    razorpay_subscription_id VARCHAR,
    subscription_auto_renew BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_google_id ON users(google_id);
CREATE INDEX IF NOT EXISTS idx_users_razorpay_customer_id ON users(razorpay_customer_id);

CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    razorpay_payment_id VARCHAR UNIQUE,
    razorpay_order_id VARCHAR UNIQUE,
    amount INTEGER,
    currency VARCHAR DEFAULT 'INR',
    status VARCHAR,
    product_type VARCHAR,
    credits_added INTEGER DEFAULT 0,
    processing_fee INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_payments_user_id ON payments(user_id);
CREATE INDEX IF NOT EXISTS idx_payments_razorpay_payment_id ON payments(razorpay_payment_id);
CREATE INDEX IF NOT EXISTS idx_payments_razorpay_order_id ON payments(razorpay_order_id);

CREATE TABLE IF NOT EXISTS groq_usage (
    id SERIAL PRIMARY KEY,
    input_tokens INTEGER DEFAULT 0,
    output_tokens INTEGER DEFAULT 0,
    total_tokens INTEGER DEFAULT 0,
    cost_usd VARCHAR DEFAULT '0.0',
    model VARCHAR DEFAULT 'llama-3.1-70b-versatile',
    request_type VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_groq_usage_created_at ON groq_usage(created_at);

-- ============================================================================
-- STEP 3: Create Sketch2BIM Schema Tables
-- ============================================================================

SET search_path TO sketch2bim_schema, public;

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    name VARCHAR,
    google_id VARCHAR UNIQUE,
    credits INTEGER DEFAULT 0,
    subscription_tier VARCHAR DEFAULT 'trial',
    subscription_status VARCHAR DEFAULT 'inactive',
    razorpay_customer_id VARCHAR UNIQUE,
    subscription_expires_at TIMESTAMP,
    razorpay_subscription_id VARCHAR,
    subscription_auto_renew BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_google_id ON users(google_id);
CREATE INDEX IF NOT EXISTS idx_users_razorpay_customer_id ON users(razorpay_customer_id);

CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    razorpay_payment_id VARCHAR UNIQUE,
    razorpay_order_id VARCHAR UNIQUE,
    amount INTEGER,
    currency VARCHAR DEFAULT 'INR',
    status VARCHAR,
    product_type VARCHAR,
    credits_added INTEGER DEFAULT 0,
    processing_fee INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_payments_user_id ON payments(user_id);
CREATE INDEX IF NOT EXISTS idx_payments_razorpay_payment_id ON payments(razorpay_payment_id);
CREATE INDEX IF NOT EXISTS idx_payments_razorpay_order_id ON payments(razorpay_order_id);

CREATE TABLE IF NOT EXISTS jobs (
    id VARCHAR PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR DEFAULT 'queued',
    progress INTEGER DEFAULT 0,
    sketch_filename VARCHAR,
    sketch_url VARCHAR,
    sketch_format VARCHAR,
    project_type VARCHAR DEFAULT 'architecture',
    detection_confidence REAL,
    plan_data JSONB,
    ifc_url VARCHAR,
    dwg_url VARCHAR,
    rvt_url VARCHAR,
    sketchup_url VARCHAR,
    model_3dm_url VARCHAR,
    preview_image_url VARCHAR,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    qc_report_path VARCHAR,
    requires_review BOOLEAN DEFAULT FALSE,
    legend_data JSONB,
    legend_detected BOOLEAN DEFAULT FALSE,
    cost_usd REAL DEFAULT 0.0,
    batch_id VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    expires_at TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_jobs_user_id ON jobs(user_id);
CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
CREATE INDEX IF NOT EXISTS idx_jobs_batch_id ON jobs(batch_id);

-- ============================================================================
-- STEP 4: Reset and Verify
-- ============================================================================

RESET search_path;

-- Verify schemas
SELECT 'Schemas created:' as status;
SELECT schema_name 
FROM information_schema.schemata 
WHERE schema_name IN ('ask_schema', 'sketch2bim_schema')
ORDER BY schema_name;

-- Verify ASK tables
SELECT 'ASK tables created:' as status;
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'ask_schema'
ORDER BY table_name;

-- Verify Sketch2BIM tables
SELECT 'Sketch2BIM tables created:' as status;
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'sketch2bim_schema'
ORDER BY table_name;

