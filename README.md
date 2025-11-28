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

- [Monorepo Migration Guide](./docs/MIGRATION_GUIDE.md)
- [Cost Analysis](./docs/COST_ANALYSIS.md)
- [Migration Status](./docs/MONOREPO_MIGRATION_COMPLETE.md)

## License

MIT

