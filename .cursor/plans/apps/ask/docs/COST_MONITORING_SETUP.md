# Cost Monitoring and Alerting Setup Guide

## Overview

This guide explains how to set up and use the cost monitoring and alerting system for the ASK Research Tool.

## Features

### 1. Groq Usage Tracking
- Tracks input/output tokens for every Groq API call
- Calculates costs based on current Groq pricing
- Stores usage history in database
- Provides daily and monthly usage statistics

### 2. Payment Fee Tracking
- Automatically calculates Razorpay processing fees (2% of transaction)
- Tracks fees per payment
- Provides fee vs revenue analysis

### 3. Cost Monitoring Dashboard
- Real-time cost breakdown
- Usage statistics
- Active alerts
- Cost projections

### 4. Automated Alerts
- Daily cost threshold alerts (default: $10/day)
- Monthly cost threshold alerts (default: $50/month)
- Usage spike detection
- Configurable via environment variables

## Database Setup

### New Database Fields

The following new fields have been added to the database:

#### Payment Model
- `processing_fee` (Integer): Razorpay processing fee in paise (2% of amount)

#### GroqUsage Model (New Table)
- `input_tokens` (Integer): Input tokens used
- `output_tokens` (Integer): Output tokens used
- `total_tokens` (Integer): Total tokens used
- `cost_usd` (String): Cost in USD (stored as string for precision)
- `model` (String): Groq model used
- `request_type` (String): Type of request (e.g., "question_generation", "answer_generation")
- `created_at` (DateTime): Timestamp of the request

### Database Migration

To add the new fields, run:

```python
from api.database import init_db
init_db()
```

This will create the new `groq_usage` table and add the `processing_fee` column to the `payments` table.

For existing databases, you may need to run a migration:

```sql
-- Add processing_fee column to payments table
ALTER TABLE payments ADD COLUMN processing_fee INTEGER DEFAULT 0;

-- Create groq_usage table
CREATE TABLE groq_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    input_tokens INTEGER DEFAULT 0,
    output_tokens INTEGER DEFAULT 0,
    total_tokens INTEGER DEFAULT 0,
    cost_usd VARCHAR(255) DEFAULT '0.0',
    model VARCHAR(255) DEFAULT 'llama-3.1-70b-versatile',
    request_type VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_groq_usage_created_at ON groq_usage(created_at);
```

## Environment Variables

### Groq Monitoring

```bash
# Groq API configuration (required)
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.1-70b-versatile

# Alert thresholds (optional, defaults shown)
GROQ_DAILY_COST_THRESHOLD=10.0    # Alert if daily cost > $10
GROQ_MONTHLY_COST_THRESHOLD=50.0  # Alert if monthly cost > $50
```

## API Endpoints

### Monitoring Endpoints

All monitoring endpoints require authentication:

- `GET /api/monitoring/costs` - Get cost breakdown
- `GET /api/monitoring/usage?days=30` - Get usage statistics
- `GET /api/monitoring/alerts` - Get active alerts
- `GET /api/monitoring/summary` - Get comprehensive summary

### Payment Endpoints

- `GET /api/payments/fees?days=30` - Get payment processing fees

## Usage

### Viewing Costs

```bash
# Get current month costs
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/monitoring/costs

# Get usage statistics for last 30 days
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/monitoring/usage?days=30

# Get active alerts
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/monitoring/alerts
```

### Setting Up Alerts

Alerts are automatically checked when:
1. Groq API calls are made (usage tracking)
2. Payment webhooks are received (fee tracking)

Alerts are logged to the application logs. To receive email alerts, configure the alert system (see `api/utils/groq_monitor.py`).

## Cost Calculation

### Groq Costs

- **Model**: llama-3.1-70b-versatile
- **Input tokens**: $0.59 per 1M tokens
- **Output tokens**: $0.79 per 1M tokens

Example:
- 1,000 input tokens + 2,000 output tokens
- Cost = (0.001 × $0.59) + (0.002 × $0.79) = $0.00059 + $0.00158 = $0.00217

### Payment Fees

- **Razorpay fee**: 2% of transaction amount
- Automatically calculated and stored with each payment

## Monitoring Best Practices

1. **Set appropriate thresholds**: Adjust `GROQ_DAILY_COST_THRESHOLD` and `GROQ_MONTHLY_COST_THRESHOLD` based on your expected usage
2. **Review alerts regularly**: Check `/api/monitoring/alerts` daily
3. **Monitor trends**: Use `/api/monitoring/usage` to track usage patterns
4. **Compare costs vs revenue**: Use `/api/monitoring/summary` to see cost vs revenue ratio

## Troubleshooting

### No usage data showing

- Check that Groq API calls are being made with database session
- Verify database connection
- Check that `groq_usage` table exists

### Alerts not triggering

- Verify environment variables are set
- Check application logs for alert messages
- Ensure usage tracking is working

### Payment fees not calculated

- Verify payment webhook is receiving events
- Check that `processing_fee` field exists in payments table
- Review payment webhook logs

## Next Steps

1. Set up email alerts (optional - modify `api/utils/groq_monitor.py`)
2. Create a dashboard UI to visualize costs (optional)
3. Set up automated reports (optional)
4. Configure Slack/Discord webhooks for alerts (optional)

