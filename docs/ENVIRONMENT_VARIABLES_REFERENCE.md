# Environment Variables Reference

Complete reference for all environment variables used across applications in the monorepo.

## Overview

Each application has its own environment file:
- `ask.env.production` - ASK application variables
- `reframe.env.production` - Reframe application variables
- `sketch2bim.env.production` - Sketch2BIM application variables

Variables are organized by:
- **Frontend** (Vercel) - Variables needed by Next.js frontend
- **Backend** (Render) - Variables needed by FastAPI backend

## ASK Application

### Frontend Variables (Vercel)

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_AUTH_URL` | Centralized auth URL | `https://kvshvl.in` |
| `ASK_API_BASE_URL` | Backend API URL | `https://ask-api.onrender.com` |
| `ASK_AUTH_SECRET` | Authentication secret | (generated) |
| `ASK_AUTH_URL` | Frontend auth URL | `https://ask.kvshvl.in` |
| `ASK_BACKEND_URL` | Backend API URL | `https://ask-api.onrender.com` |
| `ASK_GROQ_API_BASE` | Groq API base URL | `https://api.groq.com/openai/v1` |
| `ASK_NEXT_PUBLIC_API_URL` | Public API URL | `https://ask-api.onrender.com` |
| `ASK_NEXTAUTH_SECRET` | NextAuth secret | (generated) |
| `ASK_NEXTAUTH_URL` | NextAuth callback URL | `https://ask.kvshvl.in` |

### Backend Variables (Render)

#### Application Configuration
| Variable | Description | Example |
|----------|-------------|---------|
| `ASK_API_HOST` | API host | `0.0.0.0` |
| `ASK_API_PORT` | API port | `8000` |
| `ASK_APP_NAME` | Application name | `ASK: Daily Research` |
| `ASK_CORS_ORIGINS` | Allowed CORS origins | `https://ask.kvshvl.in,https://www.ask.kvshvl.in` |
| `ASK_DEBUG` | Debug mode | `false` |
| `ASK_ENVIRONMENT` | Environment | `production` |
| `ASK_FRONTEND_URL` | Frontend URL | `https://ask.kvshvl.in` |
| `ASK_LOG_CSV_FILE` | Log CSV file | `log.csv` |
| `ASK_LOG_DIR` | Log directory | `logs` |
| `ASK_LOG_LEVEL` | Log level | `INFO` |
| `ASK_PYTHONPATH` | Python path | `.` |

#### Database
| Variable | Description | Example |
|----------|-------------|---------|
| `ASK_DATABASE_URL` | **REQUIRED** - Supabase PostgreSQL connection string | `postgresql://postgres.[PROJECT_REF]:[PASSWORD]@aws-[REGION].pooler.supabase.com:6543/postgres` |
| `DATABASE_SCHEMA` | Database schema | `ask_schema` |
| `ASK_DATABASE_PASSWORD_OVERRIDE` | Password override (optional) | - |
| `ASK_DATABASE_URL_OVERRIDE` | URL override (optional) | - |

#### Groq API
| Variable | Description | Example |
|----------|-------------|---------|
| `ASK_GROQ_API_KEY` | **REQUIRED** - Groq API key | `gsk_...` |
| `ASK_GROQ_MODEL` | Groq model | `llama-3.1-70b-versatile` |
| `ASK_GROQ_DAILY_COST_THRESHOLD` | Daily cost threshold | `10.0` |
| `ASK_GROQ_MONTHLY_COST_THRESHOLD` | Monthly cost threshold | `50.0` |

#### Razorpay
| Variable | Description | Example |
|----------|-------------|---------|
| `ASK_RAZORPAY_KEY_ID` | **REQUIRED** - Razorpay key ID | `rzp_live_...` |
| `ASK_RAZORPAY_KEY_SECRET` | **REQUIRED** - Razorpay key secret | (secret) |
| `ASK_RAZORPAY_WEBHOOK_SECRET` | **REQUIRED** - Webhook secret | (secret) |
| `ASK_RAZORPAY_WEEK_AMOUNT` | Week plan amount (paise) | `129900` |
| `ASK_RAZORPAY_MONTH_AMOUNT` | Month plan amount (paise) | `349900` |
| `ASK_RAZORPAY_YEAR_AMOUNT` | Year plan amount (paise) | `2999900` |
| `ASK_RAZORPAY_PLAN_WEEK` | Week plan ID | `plan_Rha5Ikcm5JrGqx` |
| `ASK_RAZORPAY_PLAN_MONTH` | Month plan ID | `plan_Rha5JNPsk1WmI6` |
| `ASK_RAZORPAY_PLAN_YEAR` | Year plan ID | `plan_Rha5Jzn1sk8o1X` |

#### Authentication
| Variable | Description | Example |
|----------|-------------|---------|
| `ASK_JWT_ALGORITHM` | JWT algorithm | `HS256` |

#### Redis
| Variable | Description | Example |
|----------|-------------|---------|
| `ASK_UPSTASH_REDIS_REST_URL` | Upstash Redis REST URL | `https://...` |
| `ASK_UPSTASH_REDIS_REST_TOKEN` | Upstash Redis REST token | (token) |

## Sketch2BIM Application

### Frontend Variables (Vercel)

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_AUTH_URL` | Centralized auth URL | `https://kvshvl.in` |
| `SKETCH2BIM_AUTH_SECRET` | Authentication secret | (generated) |
| `SKETCH2BIM_AUTH_URL` | Frontend auth URL | `https://sketch2bim.kvshvl.in` |
| `SKETCH2BIM_NEXT_PUBLIC_API_URL` | Public API URL | `https://sketch2bim-backend.onrender.com` |
| `SKETCH2BIM_NEXT_PUBLIC_FREE_LIMIT` | Free tier limit | `5` |
| `SKETCH2BIM_NEXTAUTH_SECRET` | NextAuth secret | (generated) |
| `SKETCH2BIM_NEXTAUTH_URL` | NextAuth callback URL | `https://sketch2bim.kvshvl.in` |

### Backend Variables (Render)

#### Application Configuration
| Variable | Description | Example |
|----------|-------------|---------|
| `SKETCH2BIM_APP_ENV` | Environment | `production` |
| `SKETCH2BIM_APP_NAME` | Application name | `Sketch-to-BIM` |
| `SKETCH2BIM_DEBUG` | Debug mode | `false` |
| `SKETCH2BIM_FRONTEND_URL` | Frontend URL | `https://sketch2bim.kvshvl.in` |
| `SKETCH2BIM_ALLOWED_ORIGINS` | Allowed origins | `https://sketch2bim.kvshvl.in` |
| `SKETCH2BIM_HOST` | API host | `0.0.0.0` |
| `SKETCH2BIM_PORT` | API port | `8000` |
| `SKETCH2BIM_WORKERS` | Worker count | `4` |

#### Database
| Variable | Description | Example |
|----------|-------------|---------|
| `SKETCH2BIM_DATABASE_URL` | **REQUIRED** - Supabase PostgreSQL connection string | `postgresql://postgres.[PROJECT_REF]:[PASSWORD]@aws-[REGION].pooler.supabase.com:6543/postgres` |
| `DATABASE_SCHEMA` | Database schema | `sketch2bim_schema` |
| `SKETCH2BIM_DATABASE_PASSWORD_OVERRIDE` | Password override (optional) | - |
| `SKETCH2BIM_DATABASE_URL_OVERRIDE` | URL override (optional) | - |

#### Redis
| Variable | Description | Example |
|----------|-------------|---------|
| `SKETCH2BIM_REDIS_URL` | **REQUIRED** - Redis connection string (from Render Redis service) | (auto-linked) |
| `SKETCH2BIM_REDIS_LIMIT_COMMANDS_PER_DAY` | Daily command limit | `10000` |

#### Razorpay
| Variable | Description | Example |
|----------|-------------|---------|
| `SKETCH2BIM_RAZORPAY_KEY_ID` | **REQUIRED** - Razorpay key ID | `rzp_live_...` |
| `SKETCH2BIM_RAZORPAY_KEY_SECRET` | **REQUIRED** - Razorpay key secret | (secret) |
| `SKETCH2BIM_RAZORPAY_WEBHOOK_SECRET` | **REQUIRED** - Webhook secret | (secret) |
| `SKETCH2BIM_RAZORPAY_WEEK_AMOUNT` | Week plan amount (paise) | `129900` |
| `SKETCH2BIM_RAZORPAY_MONTH_AMOUNT` | Month plan amount (paise) | `349900` |
| `SKETCH2BIM_RAZORPAY_YEAR_AMOUNT` | Year plan amount (paise) | `2999900` |
| `SKETCH2BIM_RAZORPAY_PLAN_WEEK` | Week plan ID | `plan_Rha5Ikcm5JrGqx` |
| `SKETCH2BIM_RAZORPAY_PLAN_MONTH` | Month plan ID | `plan_Rha5JNPsk1WmI6` |
| `SKETCH2BIM_RAZORPAY_PLAN_YEAR` | Year plan ID | `plan_Rha5Jzn1sk8o1X` |

#### Bunny CDN
| Variable | Description | Example |
|----------|-------------|---------|
| `SKETCH2BIM_BUNNY_STORAGE_ZONE` | **REQUIRED** - Storage zone | `kvshvl` |
| `SKETCH2BIM_BUNNY_ACCESS_KEY` | **REQUIRED** - Access key | (key) |
| `SKETCH2BIM_BUNNY_CDN_HOSTNAME` | **REQUIRED** - CDN hostname | `kvshvl.b-cdn.net` |
| `SKETCH2BIM_BUNNY_REGION` | Bunny region | `storage.bunnycdn.com` |
| `SKETCH2BIM_BUNNY_SIGNED_URL_EXPIRY` | Signed URL expiry (seconds) | `604800` |
| `SKETCH2BIM_BUNNY_SIGNED_URL_KEY` | Signed URL key (optional) | - |

#### Replicate API
| Variable | Description | Example |
|----------|-------------|---------|
| `SKETCH2BIM_REPLICATE_API_KEY` | **REQUIRED** - Replicate API key | `r8_...` |
| `SKETCH2BIM_REPLICATE_MODEL_ID` | Model ID | `kushalsamant/sketch2bim-processor` |

#### Authentication
| Variable | Description | Example |
|----------|-------------|---------|
| `SKETCH2BIM_NEXTAUTH_SECRET` | **REQUIRED** - NextAuth secret | (generated) |
| `SKETCH2BIM_SECRET_KEY` | Secret key | (generated) |
| `SKETCH2BIM_JWT_ALGORITHM` | JWT algorithm | `HS256` |
| `SKETCH2BIM_JWT_EXPIRATION_HOURS` | JWT expiration | `24` |

#### Other
| Variable | Description | Example |
|----------|-------------|---------|
| `SKETCH2BIM_MAX_UPLOAD_SIZE_MB` | Max upload size | `50` |
| `SKETCH2BIM_FREE_CREDITS_LIMIT` | Free credits limit | `0` |
| `SKETCH2BIM_RATE_LIMIT_PER_HOUR` | Rate limit per hour | `100` |
| `SKETCH2BIM_RATE_LIMIT_PER_MINUTE` | Rate limit per minute | `10` |

## Reframe Application

### Frontend Variables (Vercel)

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_AUTH_URL` | Centralized auth URL | `https://kvshvl.in` |
| `REFRAME_API_URL` | Backend API URL | `https://reframe-api.onrender.com` |
| `REFRAME_AUTH_SECRET` | Authentication secret | (generated) |
| `REFRAME_AUTH_URL` | Frontend auth URL | `https://reframe.kvshvl.in` |
| `REFRAME_NEXT_PUBLIC_API_URL` | Public API URL | `https://reframe-api.onrender.com` |
| `REFRAME_NEXT_PUBLIC_FREE_LIMIT` | Free tier limit | `5` |
| `REFRAME_NEXT_PUBLIC_SITE_URL` | Site URL | `https://reframe.kvshvl.in` |
| `REFRAME_NEXTAUTH_SECRET` | NextAuth secret | (generated) |
| `REFRAME_NEXTAUTH_URL` | NextAuth callback URL | `https://reframe.kvshvl.in` |

#### Razorpay (Frontend)
| Variable | Description | Example |
|----------|-------------|---------|
| `REFRAME_RAZORPAY_KEY_ID` | Razorpay key ID | `rzp_live_...` |
| `REFRAME_RAZORPAY_KEY_SECRET` | Razorpay key secret | (secret) |
| `REFRAME_RAZORPAY_WEBHOOK_SECRET` | Webhook secret | (secret) |
| `REFRAME_RAZORPAY_DAILY_AMOUNT` | Daily plan amount | `9900` |
| `REFRAME_RAZORPAY_WEEK_AMOUNT` | Week plan amount | `129900` |
| `REFRAME_RAZORPAY_MONTH_AMOUNT` | Month plan amount | `349900` |
| `REFRAME_RAZORPAY_YEAR_AMOUNT` | Year plan amount | `2999900` |
| `REFRAME_RAZORPAY_PLAN_DAILY` | Daily plan ID | - |
| `REFRAME_RAZORPAY_PLAN_WEEK` | Week plan ID | `plan_Rha5Ikcm5JrGqx` |
| `REFRAME_RAZORPAY_PLAN_MONTH` | Month plan ID | `plan_Rha5JNPsk1WmI6` |
| `REFRAME_RAZORPAY_PLAN_YEAR` | Year plan ID | `plan_Rha5Jzn1sk8o1X` |

### Backend Variables (Render)

#### Application Configuration
| Variable | Description | Example |
|----------|-------------|---------|
| `REFRAME_APP_NAME` | Application name | `Reframe API` |
| `REFRAME_CORS_ORIGINS` | Allowed CORS origins | `https://reframe.kvshvl.in,https://www.reframe.kvshvl.in` |
| `REFRAME_DEBUG` | Debug mode | `false` |
| `REFRAME_ENVIRONMENT` | Environment | `production` |
| `REFRAME_FREE_LIMIT` | Free tier limit | `5` |

#### Groq API
| Variable | Description | Example |
|----------|-------------|---------|
| `REFRAME_GROQ_API_KEY` | **REQUIRED** - Groq API key | `gsk_...` |
| `REFRAME_GROQ_DAILY_COST_THRESHOLD` | Daily cost threshold | `10.0` |
| `REFRAME_GROQ_MONTHLY_COST_THRESHOLD` | Monthly cost threshold | `50.0` |

#### Upstash Redis
| Variable | Description | Example |
|----------|-------------|---------|
| `REFRAME_UPSTASH_REDIS_REST_URL` | **REQUIRED** - Upstash Redis REST URL | `https://...` |
| `REFRAME_UPSTASH_REDIS_REST_TOKEN` | **REQUIRED** - Upstash Redis REST token | (token) |

#### Authentication
| Variable | Description | Example |
|----------|-------------|---------|
| `REFRAME_NEXTAUTH_SECRET` | **REQUIRED** - NextAuth secret | (generated) |
| `REFRAME_AUTH_SECRET` | Auth secret | (generated) |
| `JWT_ALGORITHM` | JWT algorithm | `HS256` |

## Shared Variables

These variables are shared across applications:

### Razorpay Plan IDs
- Week: `plan_Rha5Ikcm5JrGqx`
- Month: `plan_Rha5JNPsk1WmI6`
- Year: `plan_Rha5Jzn1sk8o1X`

### Razorpay Amounts (in paise)
- Week: `129900` (₹1,299)
- Month: `349900` (₹3,499)
- Year: `2999900` (₹29,999)

## Getting Values

### Supabase Database URL
1. Go to: https://supabase.com/dashboard/project/[PROJECT_REF]/settings/database
2. Copy "Connection string" → "URI"
3. Use pooler format: `postgresql://postgres.[PROJECT_REF]:[PASSWORD]@aws-[REGION].pooler.supabase.com:6543/postgres`

### Groq API Key
1. Go to: https://console.groq.com/keys
2. Create or copy API key

### Razorpay Credentials
1. Go to: https://dashboard.razorpay.com/app/keys
2. Copy Key ID and Key Secret
3. Get webhook secret from: https://dashboard.razorpay.com/app/webhooks

### Upstash Redis
1. Go to: https://console.upstash.com/
2. Select Redis database
3. Copy REST URL and token

## Notes

- All secrets should be kept secure and never committed to git
- Use environment variable files (`.env.production`) as templates
- Copy values to deployment platforms (Vercel/Render) manually
- Test with test credentials first before using production credentials
- Rotate secrets regularly for security
