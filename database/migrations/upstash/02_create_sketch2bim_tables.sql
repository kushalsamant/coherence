-- Sketch2BIM Database Tables for Upstash Postgres
-- Run this in Upstash Postgres SQL Editor or via psql
-- Note: Upstash uses separate databases (not schemas), so no schema references needed
-- Connection: Use the Upstash Postgres connection string for Sketch2BIM database

-- Users table
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

-- Payments table
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

-- Verify tables were created
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
  AND table_name IN ('users', 'payments', 'jobs')
ORDER BY table_name;

