-- Sketch2BIM Schema Tables
-- Run this in Supabase SQL Editor after running 01_create_schemas.sql
-- URL: https://supabase.com/dashboard/project/twxudlzipbiavnzcitzb/sql/new

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

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_google_id ON users(google_id);
CREATE INDEX IF NOT EXISTS idx_users_stripe_customer_id ON users(stripe_customer_id);

-- Payments table
CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    stripe_payment_intent_id VARCHAR UNIQUE,
    stripe_checkout_session_id VARCHAR UNIQUE,
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
CREATE INDEX IF NOT EXISTS idx_payments_stripe_payment_intent_id ON payments(stripe_payment_intent_id);
CREATE INDEX IF NOT EXISTS idx_payments_stripe_checkout_session_id ON payments(stripe_checkout_session_id);

-- Jobs table (Sketch2BIM specific)
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

RESET search_path;

-- Verify tables were created
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'sketch2bim_schema'
ORDER BY table_name;

