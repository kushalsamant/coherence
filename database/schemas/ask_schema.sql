-- ASK Schema Definition
-- Run this after creating the ask_schema in PostgreSQL

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

RESET search_path;

