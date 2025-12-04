# KVSHVL Platform

**A unified platform for architectural research, AI-powered reframing, and sketch-to-BIM conversion.**

[![Deploy Status](https://img.shields.io/badge/deploy-live-success)](https://kvshvl.in)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 🌟 Overview

KVSHVL Platform is a comprehensive web application combining three powerful tools:

- **ASK** - Daily Architectural Research questions and answers
- **Reframe** - AI-powered text reframing with multiple tones and styles
- **Sketch2BIM** - Convert architectural sketches to BIM models

## 🏗️ Architecture

### Monorepo Structure

```
kushalsamant.github.io/
├── app/                      # Next.js App Router pages
│   ├── ask/                  # ASK application
│   ├── reframe/              # Reframe application
│   ├── sketch2bim/           # Sketch2BIM application
│   └── api/                  # Unified API routes
├── components/               # React components
│   ├── ask/                  # ASK-specific components
│   ├── reframe/              # Reframe-specific components
│   ├── sketch2bim/           # Sketch2BIM components
│   └── shared/               # Shared components
├── lib/                      # Utility libraries
├── packages/                 # Workspace packages
│   ├── design-system/        # @kushalsamant/design-template
│   ├── shared-frontend/      # @kvshvl/shared-frontend
│   └── shared-backend/       # Shared Python utilities
├── apps/                     # Backend applications
│   └── platform-api/         # Unified FastAPI backend
├── content/                  # Markdown content
│   ├── anthology/            # ASK content
│   └── projects/             # Project documentation
└── database/                 # Database migrations
    └── migrations/           # Alembic migrations
```

### Technology Stack

**Frontend:**
- Next.js 16 (App Router)
- React 18
- TypeScript
- Tailwind CSS
- Upstash Redis (session storage)

**Backend:**
- FastAPI (Python)
- PostgreSQL (Upstash Postgres)
- Alembic (migrations)
- Razorpay (payments)

**AI/ML:**
- Groq API (LLaMA models)
- Replicate (Sketch2BIM processing)

**Deployment:**
- Frontend: Vercel
- Backend: Render.com
- CDN: BunnyCDN (assets)

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ 
- npm 9+
- Python 3.11+ (for backend development)
- PostgreSQL (Upstash accounts for production)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/kushalsamant/kushalsamant.github.io.git
   cd kushalsamant.github.io
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment variables**
   ```bash
   cp platform.env.template .env.local
   # Edit .env.local with your credentials
   ```

4. **Run database migrations**
   ```bash
   cd database/migrations/ask
   alembic upgrade head
   
   cd ../sketch2bim
   alembic upgrade head
   ```

5. **Start development server**
   ```bash
   npm run dev
   ```

6. **Visit the application**
   - Main site: http://localhost:3000
   - ASK: http://localhost:3000/ask
   - Reframe: http://localhost:3000/reframe
   - Sketch2BIM: http://localhost:3000/sketch2bim

## 📋 Environment Variables

See [`platform.env.template`](platform.env.template) for all required environment variables.

### Core Variables

```env
# Authentication
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-here
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Redis (Upstash)
UPSTASH_REDIS_REST_URL=your-redis-url
UPSTASH_REDIS_REST_TOKEN=your-redis-token

# Database (Upstash Postgres)
ASK_DATABASE_URL=postgresql://user:pass@host:port/db
SKETCH2BIM_DATABASE_URL=postgresql://user:pass@host:port/db

# Payments (Razorpay)
PLATFORM_RAZORPAY_KEY_ID=rzp_test_xxx
PLATFORM_RAZORPAY_KEY_SECRET=your-secret
PLATFORM_RAZORPAY_PLAN_WEEK=plan_xxx
PLATFORM_RAZORPAY_PLAN_MONTH=plan_xxx
PLATFORM_RAZORPAY_PLAN_YEAR=plan_xxx

# AI APIs
REFRAME_GROQ_API_KEY=your-groq-key
SKETCH2BIM_REPLICATE_API_KEY=your-replicate-key
```

## 🏃 NPM Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run start` | Start production server |
| `npm run lint` | Run ESLint |
| `npm run analyze` | Analyze bundle size |
| `npm run generate:sitemap` | Generate sitemap.xml |

## 🗄️ Database Migrations

### ASK Database
```bash
cd database/migrations/ask
alembic upgrade head        # Apply migrations
alembic current             # Show current version
alembic revision -m "msg"   # Create new migration
```

### Sketch2BIM Database
```bash
cd database/migrations/sketch2bim
alembic upgrade head        # Apply migrations
alembic current             # Show current version
```

**Auto-migration:** Set `AUTO_RUN_MIGRATIONS=true` to run migrations on app startup.

## 💳 Payment Integration

The platform uses Razorpay for subscription management.

### Test Mode (Development)
```env
PLATFORM_RAZORPAY_KEY_ID=rzp_test_RmnbZXF6kOQine
PLATFORM_RAZORPAY_PLAN_WEEK=plan_RnZU4WDSvPT6qe
PLATFORM_RAZORPAY_PLAN_MONTH=plan_Rnaq9KJ0QzgV7Y
PLATFORM_RAZORPAY_PLAN_YEAR=plan_RnZU5nSKQEiOcC
```

### Live Mode (Production)
```env
PLATFORM_RAZORPAY_KEY_ID=rzp_live_RhNUuWRBG7lzR4
PLATFORM_RAZORPAY_PLAN_WEEK=plan_Rnb1CCVRIvBK2W
PLATFORM_RAZORPAY_PLAN_MONTH=plan_Rnb1CsrwHntisk
PLATFORM_RAZORPAY_PLAN_YEAR=plan_Rnb1DZy2EHhHqT
```

### Verify Plans
```bash
python scripts/platform/create_razorpay_plans.py
```

## 🚢 Deployment

### Frontend (Vercel)

1. **Connect repository to Vercel**
2. **Configure environment variables** in Vercel dashboard
3. **Deploy:** Automatic on push to `main` branch

**Vercel Dashboard:** https://vercel.com/kvshvl/kushalsamant-github-io

### Backend (Render)

1. **Connect repository to Render**
2. **Point to `render.yaml` blueprint**
3. **Configure environment variables** in Render dashboard
4. **Deploy:** Automatic on push to `main` branch

**Configuration:** See [`render.yaml`](render.yaml)

### Domain Configuration

- **Primary:** https://kvshvl.in
- **ASK:** https://ask.kvshvl.in
- **Reframe:** https://reframe.kvshvl.in
- **Sketch2BIM:** https://sketch2bim.kvshvl.in

Domain routing is configured in [`vercel.json`](vercel.json).

## 🧪 Testing

```bash
# Run all tests
npm run test:workspaces

# Test Razorpay integration
python scripts/platform/create_razorpay_plans.py

# Test build
npm run build
```

### Test Card (Razorpay)
```
Card: 4111 1111 1111 1111
CVV: Any 3 digits
Expiry: Any future date
```

## 📦 Workspace Packages

### @kushalsamant/design-template
Unified design system and component library.

```bash
cd packages/design-system
npm run build
```

### @kvshvl/shared-frontend
Shared frontend utilities (auth, payments, settings).

```bash
cd packages/shared-frontend
npm run build
```

### shared-backend
Shared Python utilities for backend services.

```bash
pip install -e packages/shared-backend
```

## 🔒 Security

- **Authentication:** NextAuth v5 with Google OAuth
- **Rate Limiting:** Upstash Rate Limit on all API routes
- **Security Headers:** CSP, HSTS, X-Frame-Options configured
- **Input Validation:** Zod schemas for TypeScript, Pydantic for Python
- **Payment Security:** Razorpay webhook signature verification

## 📊 Monitoring

- **Error Tracking:** Logger utility (implement Sentry for production)
- **Analytics:** Vercel Analytics
- **Performance:** Lighthouse CI
- **Uptime:** Monitor via Vercel dashboard

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Commit changes (`git commit -m 'Add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Style

- **TypeScript:** Follow ESLint rules (`.eslintrc.json`)
- **Python:** Follow PEP 8 (Black + Ruff)
- **Commits:** Conventional Commits format

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Kushal Samant**
- Website: https://kvshvl.in
- Email: writetokushaldsamant@gmail.com

## 🔗 Links

- **Production:** https://kvshvl.in
- **Razorpay Dashboard:** https://dashboard.razorpay.com
- **Vercel Dashboard:** https://vercel.com/kvshvl/kushalsamant-github-io
- **Documentation:** See [`.cursor/plans/merged-platform.plan.md`](.cursor/plans/merged-platform.plan.md)

## 🎯 Project Status

**Status:** 🚀 **LIVE & DEPLOYED**  
**Last Updated:** December 5, 2025  
**Build:** ✅ Passing  
**Deployment:** ✅ Automatic via Vercel + Render

See [merged-platform.plan.md](.cursor/plans/merged-platform.plan.md) for detailed status and roadmap.

