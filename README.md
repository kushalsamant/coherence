# KVSHVL Platform Monorepo

Unified monorepo for KVSHVL platform applications: ASK Research Tool, Sketch2BIM, and Reframe AI.

## Structure

```
kvshvl-platform/
├── packages/              # Shared packages
│   ├── shared-backend/    # Python shared code (auth, payments, database, etc.)
│   ├── shared-frontend/   # TypeScript shared code (auth, payments, etc.)
│   └── design-system/     # Design template component library
├── apps/                  # Applications
│   ├── ask/               # ASK Research Tool
│   ├── sketch2bim/        # Sketch-to-BIM
│   └── reframe/           # Reframe AI
└── database/              # Database migrations and schemas
```

## Platform Architecture (High Level)

- **Applications**
  - `apps/ask`: *ASK: Daily Research* – content Q&A + platform admin dashboard.
  - `apps/sketch2bim`: Sketch-to-BIM conversion backend + Next.js frontend.
  - `apps/reframe`: Text reframing service (backend + frontend).
- **Shared code**
  - `packages/shared-backend`: auth, payments (Razorpay), subscription helpers, cost tracking, and configuration utilities.
  - `packages/shared-frontend`: shared auth/payment helpers for the frontends.
  - `packages/design-system`: UI component library used by the Next.js apps.
- **Cost tracking**
  - **ASK / Sketch2BIM**: store detailed cost data in Postgres (Supabase) using app-specific schemas (`ask_schema`, `sketch2bim_schema`).
  - **Reframe**: tracks Groq usage and cost aggregates in Upstash Redis.
  - Shared Razorpay plan IDs and pricing are documented in `docs/ENVIRONMENT_VARIABLES_REFERENCE.md` and wired via `render.yaml`.
- **Admin dashboard**
  - Implemented in `apps/ask/frontend` under `/admin/platform-dashboard`.
  - Talks to ASK backend feasibility and monitoring endpoints:
    - `/api/feasibility/platform/*` for platform-wide economics.
    - `/api/monitoring/*` for cost, usage, and alert summaries.

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL (for shared database)
- Redis (for caching)

### Installation

```bash
# Install all dependencies
npm install

# Install Python dependencies (if using Poetry)
poetry install
```

### Development

```bash
# Run all apps in development mode
npm run dev

# Run specific app
cd apps/ask/frontend && npm run dev
cd apps/ask/api && uvicorn main:app --reload
```

## Shared Packages

### Backend Packages

- **shared-backend/auth**: Authentication utilities (JWT, user dependencies)
- **shared-backend/payments**: Razorpay integration and webhook handling
- **shared-backend/database**: Database models and schema utilities
- **shared-backend/subscription**: Subscription management
- **shared-backend/cost-monitoring**: Cost tracking and alerts
- **shared-backend/config**: Shared configuration

### Frontend Packages

- **shared-frontend/auth**: NextAuth configuration
- **shared-frontend/payments**: Razorpay client utilities
- **shared-frontend/cost-monitoring**: Cost monitoring UI components
- **design-system**: Component library (@kushalsamant/design-template)

## Database

The platform uses a shared PostgreSQL database with separate schemas:

- `ask_schema`: ASK application tables
- `sketch2bim_schema`: Sketch2BIM application tables
- `shared_schema`: Optional shared tables

## Deployment

Each application deploys independently:

- **ASK**: Frontend on Vercel, Backend on Render
- **Sketch2BIM**: Frontend on Vercel, Backend on Render
- **Reframe**: Next.js app on Vercel

## Documentation

- [Documentation Index](./docs/DOCUMENTATION_INDEX.md) - Complete documentation guide
- [Monorepo Migration Guide](./docs/MIGRATION_GUIDE.md) - Migration instructions
- [Migration Status](./docs/MONOREPO_MIGRATION.md) - Current migration status
- [Cost Analysis](./docs/COST_ANALYSIS.md) - Infrastructure cost analysis
- [Deployment Configuration Guide](./DEPLOYMENT_CONFIGURATION_GUIDE.md) - Vercel/Render and OAuth config
- [Deployment Checklist](./docs/DEPLOYMENT_CHECKLIST.md) - End-to-end deployment steps
- [Environment Variables Reference](./docs/ENVIRONMENT_VARIABLES_REFERENCE.md) - Canonical env var list
- [API Versioning Strategy](./docs/API_VERSIONING.md) - How APIs are versioned across apps
- [SLOs](./docs/SLOs.md) - Service-level objectives and alerting hooks

## License

MIT

