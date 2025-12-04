# KVSHVL Platform

Unified platform for ASK (Daily Architectural Research), Reframe (Content Reformulation), and Sketch-to-BIM (Sketch-based 3D Modeling).

## 🚀 Quick Start

### Prerequisites

- Node.js >= 18.0.0
- npm >= 9.0.0
- Python >= 3.10 (for backend services)
- PostgreSQL (for ASK and Sketch2BIM databases)
- Redis (Upstash recommended)

### Installation

```bash
# Clone the repository
git clone https://github.com/kushalsamant/kushalsamant.github.io.git
cd kushalsamant.github.io

# Install dependencies
npm install

# Copy environment template
cp platform.env.template .env.local
# Edit .env.local with your actual credentials

# Run development server
npm run dev
```

Visit `http://localhost:3000` to see the app.

### Production Build

```bash
# Build all workspaces and Next.js
npm run build

# Start production server
npm run start
```

## 📁 Project Structure

```
kushalsamant.github.io/
├── app/                      # Next.js 13+ App Router pages
│   ├── ask/                  # ASK: Daily Architectural Research
│   ├── reframe/              # Reframe: Content reformulation
│   ├── sketch2bim/           # Sketch-to-BIM: 3D modeling from sketches
│   ├── account/              # User account & subscription management
│   ├── api/                  # API routes (auth, payments, webhooks)
│   └── subscribe/            # Subscription checkout pages
├── components/               # React components
│   ├── ask/                  # ASK-specific components
│   ├── reframe/              # Reframe-specific components
│   ├── sketch2bim/           # Sketch2BIM-specific components
│   ├── platform-dashboard/  # Shared dashboard components
│   └── shared/               # Shared components (HeaderWrapper)
├── lib/                      # Shared utilities and libraries
│   ├── ask/                  # ASK client libraries
│   ├── reframe/              # Reframe client libraries
│   ├── sketch2bim/           # Sketch2BIM client libraries
│   ├── shared/               # Platform-wide shared utilities
│   ├── auth.ts               # NextAuth configuration
│   ├── redis.ts              # Redis/Upstash client
│   ├── logger.ts             # Centralized logging
│   ├── rate-limit.ts         # Rate limiting utilities
│   └── validation.ts         # Input validation schemas (Zod)
├── apps/                     # Backend services
│   └── platform-api/         # FastAPI backend (Python)
│       ├── routers/          # API route handlers
│       ├── models/           # Database models
│       ├── services/         # Business logic services
│       └── ai/               # AI/ML services (Sketch2BIM)
├── packages/                 # Monorepo workspace packages
│   ├── design-system/        # Shared UI components (@kushalsamant/design-template)
│   ├── shared-frontend/      # Shared frontend utilities
│   └── shared-backend/       # Shared Python backend utilities
├── content/                  # Content files (Markdown)
│   ├── anthology/            # ASK research articles (300+ files)
│   └── projects/             # Project case studies
├── database/                 # Database migrations
│   └── migrations/           # Alembic migrations
│       ├── ask/              # ASK database migrations
│       └── sketch2bim/       # Sketch2BIM database migrations
├── public/                   # Static assets
│   ├── assets/               # Images, icons, media
│   ├── sitemap.xml           # Generated sitemap
│   └── robots.txt            # SEO crawling instructions
├── scripts/                  # Build and deployment scripts
│   ├── generate-sitemap.ts   # Dynamic sitemap generation
│   ├── platform/             # Platform management scripts
│   └── deployment/           # Deployment utilities
├── .github/                  # GitHub configuration
│   └── dependabot.yml        # Automated dependency updates
├── next.config.js            # Next.js configuration
├── render.yaml               # Render.com deployment config
├── vercel.json               # Vercel deployment config
└── platform.env.template     # Environment variables template
```

## 🔧 Technology Stack

### Frontend
- **Framework**: Next.js 16 (App Router, React 18, TypeScript 5)
- **Styling**: Tailwind CSS 3
- **Authentication**: NextAuth.js v5 (Auth.js) with Google OAuth
- **State Management**: React Context API
- **3D Rendering**: Three.js + web-ifc (for Sketch2BIM IFC viewer)
- **UI Components**: Custom design system + Radix UI primitives
- **Validation**: Zod for type-safe input validation

### Backend
- **API Framework**: FastAPI (Python 3.10+)
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0 with Alembic migrations
- **Caching**: Redis (Upstash)
- **AI/ML**: Groq API (llama-3.1-8b-instant)
- **File Storage**: BunnyCDN (for Sketch2BIM uploads)
- **Payments**: Razorpay (subscriptions and one-time payments)

### Infrastructure
- **Hosting**: Vercel (frontend), Render.com (backend API)
- **CDN**: Vercel Edge Network, BunnyCDN
- **Monitoring**: Built-in cost tracking and usage monitoring
- **Security**: CSP, HSTS, rate limiting, input validation

## 🔐 Environment Variables

See `platform.env.template` for a complete list of required environment variables.

### Core Variables
```env
# Authentication
AUTH_SECRET=<32-character-secret>
GOOGLE_CLIENT_ID=<google-oauth-client-id>
GOOGLE_CLIENT_SECRET=<google-oauth-secret>

# Redis/Upstash
UPSTASH_REDIS_REST_URL=<upstash-redis-url>
UPSTASH_REDIS_REST_TOKEN=<upstash-token>

# Razorpay Payments
PLATFORM_RAZORPAY_KEY_ID=rzp_live_xxx or rzp_test_xxx
PLATFORM_RAZORPAY_KEY_SECRET=<secret>
PLATFORM_RAZORPAY_WEBHOOK_SECRET=<webhook-secret>

# Database URLs
ASK_DATABASE_URL=postgresql://user:pass@host:5432/ask
SKETCH2BIM_DATABASE_URL=postgresql://user:pass@host:5432/sketch2bim

# API URLs
NEXT_PUBLIC_PLATFORM_API_URL=https://platform-api.onrender.com
```

## 📦 Workspace Packages

This is a monorepo using npm workspaces:

- **`@kushalsamant/design-template`**: Shared UI component library
- **`@kvshvl/shared-frontend`**: Shared frontend utilities
- **Backend packages**: Shared Python backend utilities

Build all workspaces:
```bash
npm run build:workspaces
```

## 🧪 Testing

```bash
# Run tests for all workspaces
npm run test:workspaces

# Run linters
npm run lint
npm run lint:workspaces
```

## 🚢 Deployment

### Vercel (Frontend)
```bash
# Deploy to production
vercel --prod

# Or push to main branch (auto-deploy enabled)
git push origin main
```

### Render (Backend API)
Backend deploys automatically on push to `main` branch. Configuration is in `render.yaml`.

## 📊 Performance & Monitoring

- **Bundle Analyzer**: Run `ANALYZE=true npm run build` to analyze bundle sizes
- **Image Optimization**: Automatic with Next.js Image component
- **Code Splitting**: Dynamic imports for heavy components
- **Sitemap Generation**: Dynamic sitemap generated on build
- **Rate Limiting**: Redis-backed rate limiting on API routes
- **Cost Tracking**: Built-in Groq API cost monitoring

## 🔒 Security Features

- **CSP**: Strict Content Security Policy configured
- **HSTS**: HTTP Strict Transport Security with preload
- **Rate Limiting**: Per-IP rate limits on auth, payments, API
- **Input Validation**: Zod schemas for all user inputs
- **Dependency Scanning**: Dependabot enabled for security updates
- **CORS**: Origin validation for API requests

## 📝 Scripts

```bash
npm run dev              # Start development server
npm run build            # Build all workspaces + Next.js
npm run start            # Start production server
npm run lint             # Run ESLint
npm run generate:sitemap # Generate sitemap.xml
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

MIT License - see LICENSE file for details

## 🔗 Links

- **Production**: https://kvshvl.in
- **Documentation**: See inline code documentation
- **Support**: Contact via /getintouch page

## 📮 Contact

**Kushal Samant**  
Website: https://kvshvl.in  
GitHub: [@kushalsamant](https://github.com/kushalsamant)

---

Built with ❤️ using Next.js, FastAPI, and modern web technologies.
