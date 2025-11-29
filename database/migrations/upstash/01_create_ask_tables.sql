-- ASK Database Tables for Upstash Postgres
-- Run this in Upstash Postgres SQL Editor or via psql
-- Note: Upstash uses separate databases (not schemas), so no schema references needed
-- Connection: Use the Upstash Postgres connection string for ASK database

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

-- Groq Usage table
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

-- Verify tables were created
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
  AND table_name IN ('users', 'payments', 'groq_usage')
ORDER BY table_name;

