# Sketch-to-BIM

Convert hand-drawn architectural sketches into editable BIM files using computer vision-based processing.

## Quick Start

1. Visit **[https://sketch2bim.kvshvl.in](https://sketch2bim.kvshvl.in)**
2. Sign in with Google
3. Upload a sketch (PNG, JPG, or PDF)
4. Wait 30–60 seconds for processing
5. Download IFC / DWG / SketchUp (OBJ) files

## What It Does

**Sketch-to-BIM** uses computer vision (OpenCV) to detect geometric elements from hand-drawn sketches and generates professional BIM files (IFC, DWG, SketchUp):

- **Architecture**: Detects walls, rooms, doors, and windows from architectural floor plans using OpenCV edge detection and contour analysis

All project types generate IFC and DWG files. Revit can import IFC files natively. SketchUp files are exported as OBJ format.

## Pricing

**Unified Pricing (shared across ASK, Reframe, and Sketch2BIM):**
- **Week:** ₹1,299 - 7-day access with unlimited conversions
- **Month:** ₹3,499 - 30-day access with unlimited conversions
- **Year:** ₹29,999 - 365-day access with unlimited conversions (33% savings vs monthly)

All three apps (ASK, Reframe, Sketch2BIM) use the same pricing structure for consistency. See [`docs/ENVIRONMENT_VARIABLES_REFERENCE.md`](../../docs/ENVIRONMENT_VARIABLES_REFERENCE.md#pricing--plans) for complete pricing details.

## Documentation

Additional documentation is available in the `/docs` directory:

- **[Deployment Checklist](./docs/deployment_checklist.md)** - Production deployment guide
- **[Production Verification](./docs/production_verification.md)** - Production verification checklist
- **[Testing Guide](./docs/testing.md)** - Complete testing guide for payments and webhooks
- **[Troubleshooting](./docs/troubleshooting.md)** - Common issues and solutions
- **[Migrations](./docs/migrations.md)** - Database migration documentation
- **[Feature Flags](./docs/FEATURE_FLAGS.md)** - Experimental features and optional capabilities

## Tech Stack

**Standardized Infrastructure:**
- **Frontend**: Next.js 14, React, TypeScript, Tailwind CSS (hosted on Vercel)
- **Backend**: FastAPI, Python 3.13, SQLAlchemy (hosted on Render)
- **Database**: PostgreSQL (via Render)
- **Caching**: Redis (via Render)
- **Storage**: BunnyCDN (file storage and CDN)
- **Payments**: Razorpay (unified payment gateway)
- **Authentication**: Google OAuth (NextAuth)
- **Processing**: Computer vision (OpenCV) + Pure Python IfcOpenShell (no Blender required)

## Local Development

```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

---

## Table of Contents

1. [Project Summary](#project-summary)
2. [Getting Started](#getting-started)
3. [FAQ](#faq)
4. [API Documentation](#api-documentation)
5. [Development Guide](#development-guide)
6. [Architecture](#architecture)
7. [Deployment](#deployment)
8. [Windows Setup](#windows-setup)
9. [Legend Parsing](#legend-parsing)
10. [Implementation Summary](#implementation-summary)
11. [Production Fixes](#production-fixes)
12. [Alembic Migrations](#alembic-migrations)

---

## Project Summary

**Updated:** November 11, 2025

### Overview
Sketch-to-BIM converts hand-drawn architectural sketches into editable BIM files. The platform provides:
- Google OAuth authentication
- Credit-based usage & Razorpay billing
- Sketch upload with progress tracking
- Computer vision-based BIM generation (cloud processing)
- Downloadable IFC / DWG / SketchUp (OBJ) files
- Browser-based IFC viewer

Processing uses OpenCV for geometry detection and IfcOpenShell for BIM file generation. All processing occurs in the cloud using FastAPI BackgroundTasks.

---

### Architecture
```
User → Next.js frontend (Vercel)
    → FastAPI backend (Render)
        → PostgreSQL (Supabase)
        → Redis (Upstash)
        → Pure Python IfcOpenShell (direct processing)
        → Storage CDN (BunnyCDN)
```
- **Frontend:** Next.js App Router, Tailwind CSS, TypeScript
- **Backend:** FastAPI, SQLAlchemy, Pydantic
- **Authentication:** NextAuth (Google OAuth)
- **Payments:** Razorpay Checkout + webhooks (unified pricing: Week: ₹1,299, Month: ₹3,499, Year: ₹29,999 - shared across ASK, Reframe, and Sketch2BIM)
- **Storage:** BunnyCDN (signed URLs)
- **Processing:** Computer vision (OpenCV) for sketch reading + Pure Python IfcOpenShell for BIM generation (no Blender, no external processing service required)

---

### Repository Structure
```
sketch2bim/
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── main.py          # Entry point
│   │   ├── config.py        # Settings (Pydantic)
│   │   ├── database.py      # SQLAlchemy session
│   │   ├── models.py        # User, Job, Payment
│   │   ├── schemas.py       # Pydantic response models
│   │   ├── auth.py          # Session helpers
│   │   ├── utils.py         # CDN, email, rate limiting
│   │   └── routes/
│   │       ├── auth.py      # Auth endpoints
│   │       ├── generate.py  # Upload & job status
│   │       ├── payments.py  # Razorpay webhooks
│   │       └── admin.py     # Admin APIs
│   └── requirements.txt
│
├── frontend/                # Next.js application
│   ├── app/                 # Routes (landing, dashboard, viewer)
│   ├── components/          # Upload form, job list, viewer
│   ├── lib/api.ts           # Backend API client
│   └── package.json
│
├── docs/                    # Public documentation
```

> Note: Processing uses open-source OpenCV and IfcOpenShell libraries. No proprietary AI models are required for basic functionality.

---

### Key Components
- **Job Management:** Users upload sketches, jobs stored in PostgreSQL, status updated in real-time
- **Rate Limiting:** Redis-backed per-user throttling (10 uploads/min default)
- **File Downloads:** Users download files directly from the dashboard
- **IFC Viewer:** Custom viewer using `three` and `web-ifc`
- **Security:** Signed download URLs, secrets managed via Vercel/Render env vars

---

### Cost Estimate (Free Tier)
| Service      | Free Allowance        | Notes |
|--------------|-----------------------|-------|
| Vercel       | Unlimited deployments | Frontend |
| Render       | 750 hours/month       | Backend + Processing |
| Supabase     | 500 MB DB             | PostgreSQL |
| Upstash Redis| 10K commands/day      | Rate limiting |
| BunnyCDN     | $1/TB (pay-as-you-go) | Storage |

**Typical monthly cost:** ~$1–3 for 1000 conversions (mostly BunnyCDN storage).
**Cost savings:** 60-80% reduction vs Blender-based processing (no GPU compute fees).

---

### Current Status
- **Frontend**: Live at `https://sketch2bim.kvshvl.in`
- **Backend API**: `https://sketch2bim-backend.onrender.com`
- **Database**: Supabase PostgreSQL (pooler on port 6543)
- **Redis**: Upstash
- **Storage**: BunnyCDN
- **Payments**: Razorpay (live mode)
- Processing runs directly on Render backend using pure Python IfcOpenShell
- All services are cloud-hosted (zero self-hosting)

---

### Production Deployment

For production deployment instructions, see **[deployment_checklist.md](./docs/deployment_checklist.md)**.

For testing guide, see **[testing.md](./docs/testing.md)**.

For troubleshooting, see **[troubleshooting.md](./docs/troubleshooting.md)**.

For migration documentation, see **[migrations.md](./docs/migrations.md)**.

**Quick Verification**:
1. Verify Razorpay plans: Check Razorpay dashboard for active subscription plans
2. Check database migrations: `python backend/scripts/check_migration_status.py`
3. Test health endpoint: `GET https://sketch2bim-backend.onrender.com/health`

### Implementation Details

#### Core Processing Pipeline
1. **Sketch Detection**: OpenCV-based geometry extraction from uploaded sketches
2. **IFC Generation**: Pure Python IfcOpenShell creates IFC files directly
3. **Background Processing**: FastAPI BackgroundTasks handle async processing
4. **File Upload**: Generated IFC files uploaded to BunnyCDN with signed URLs

#### Key Files
- `backend/app/ai/ifc_generator.py` - Pure Python IfcOpenShell IFC generation
- `backend/app/ai/model_generator.py` - Orchestrates sketch → plan → IFC pipeline
- `backend/app/routes/generate.py` - Upload endpoint with BackgroundTasks
- `frontend/components/IfcViewer.tsx` - Browser-based IFC viewer with view controls

---

## Getting Started

### Welcome!

Sketch2BIM converts your architectural sketches into professional BIM models in minutes.

### Quick Start

1. **Sign Up**: Visit [sketch2bim.kvshvl.in](https://sketch2bim.kvshvl.in) and sign in with Google
2. **Upload**: Drag and drop your sketch (PNG, JPG, or PDF)
3. **Wait**: Processing takes 30-60 seconds
4. **Download**: Get your IFC, DWG, or SketchUp (OBJ) files. Revit can import IFC files directly.

### Best Practices

#### Sketch Quality

- **Clear lines**: Use dark pen/marker on white paper
- **High resolution**: Scan at 300 DPI or take clear photos
- **Complete drawings**: Include all walls, rooms, and openings
- **Straight lines**: Use a ruler for best results

#### Supported Formats

- **Input**: PNG, JPG, JPEG, PDF
- **Output**: IFC (works with Revit, Archicad, FreeCAD), DWG (DXF format), SketchUp (OBJ format)

### Tips for Best Results

1. **Clean sketches**: Remove smudges and eraser marks
2. **Label rooms**: Add room labels for better detection
3. **Show scale**: Include a scale reference if possible
4. **Multiple views**: Upload floor plans for best accuracy

### Troubleshooting

**Low confidence scores?**
- Ensure sketch has clear, dark lines
- Remove background noise
- Use higher resolution scan

**Missing elements?**
- Check if sketch is complete
- Verify all walls are clearly drawn
- Try uploading a cleaner version

### Need Help?

- Email: support@sketch2bim.com
- Documentation: [docs.sketch2bim.com](https://docs.sketch2bim.com)

---

## FAQ

### General

**Q: What file formats do you support?**
A: We accept PNG, JPG, JPEG, and PDF for input. Output formats include:
- **IFC**: Industry Foundation Classes format (works with all major BIM software including Revit)
- **DWG**: AutoCAD Drawing format (exported as DXF, which AutoCAD opens natively)
- **SketchUp**: OBJ format (SketchUp can import OBJ files)
- **Revit**: We provide IFC files that Revit can import natively. Revit does not require native RVT files - it imports IFC directly.

**Q: How long does processing take?**
A: Typically 30-60 seconds per sketch, depending on complexity and server load.

**Q: Is my data secure?**
A: Yes. All files are encrypted in transit and at rest. Files are automatically deleted after 7 days.

**Q: Can I use the generated files commercially?**
A: Yes, but we recommend having a licensed architect review and sign off on any construction documents.

### Technical

**Q: What BIM software can open the files?**
A: IFC files can be opened in Revit, Archicad, FreeCAD, and most BIM software. DWG files work with AutoCAD and compatible software.

**Q: Why did my job fail?**
A: Common reasons:
- Sketch quality too low (blurry, unclear lines)
- File too large (>50MB)
- Unsupported format
- Server temporarily unavailable

**Q: What if the detection confidence is low?**
A: Jobs with confidence <50% are flagged for review. You can approve or request a refund.

### Billing

**Q: How do credits work?**
A: Trial tier gets 5 conversions. All paid tiers (Week, Month, Year) get unlimited conversions for the duration of their subscription.

**Q: Can I get a refund?**
A: Yes, if a job fails or you're not satisfied, contact support for a refund. See our refund policy for details.

**Q: Do subscriptions auto-renew?**
A: Subscriptions can be purchased as one-time payments or recurring subscriptions. Recurring subscriptions auto-renew until cancelled.

### Enterprise

**Q: Do you offer on-premise deployment?**
A: Contact sales for enterprise on-premise options.

---

## Known Limitations

### Processing Technology
- **Computer Vision, Not Deep Learning**: The system uses OpenCV for geometry detection (edge detection, contour analysis, Hough line transforms), not neural networks or deep learning models
- **Symbol Detection**: Optional symbol detection using PyTorch Faster R-CNN is available but disabled by default (requires trained model file)
- **No ML Models**: No machine learning models are used for room/wall detection - purely geometric computer vision

### Experimental Features
- **Legend Parsing**: OCR-based legend detection requires pytesseract and may return empty results if text is unclear or legend is in non-standard locations

### Output Formats
- **Revit Support**: We provide IFC files that Revit can import natively. Revit does not require native RVT files - it imports IFC directly, which is the industry standard.
- **SketchUp**: Exported as OBJ format (SketchUp can import OBJ files)
- **DWG**: Exported as DXF format (AutoCAD opens DXF files natively)

### Processing Limitations
- **Basic Detection**: Works best with clear, high-contrast sketches with distinct geometric shapes
- **Complex Sketches**: May struggle with heavily annotated drawings, overlapping elements, or very stylized sketches
- **Symbol-Heavy Plans**: Symbol detection requires a trained model (disabled by default)

---

## API Documentation

### Authentication

#### JWT Authentication (User)
Include JWT token in Authorization header:
```
Authorization: Bearer <token>
```

### Endpoints

#### Generate

##### Upload Sketch
```http
POST /api/v1/generate/upload
Content-Type: multipart/form-data

file: <sketch image>
```

**Response:**
```json
{
  "job_id": "abc123",
  "message": "Sketch uploaded successfully",
  "credits_remaining": 4
}
```

##### Get Job Status
```http
GET /api/v1/generate/status/{job_id}
```

**Response:**
```json
{
  "id": "abc123",
  "status": "completed",
  "progress": 100,
  "message": "Job completed successfully"
}
```

##### List Jobs
```http
GET /api/v1/generate/jobs?limit=50&offset=0
```

##### Review Job
```http
POST /api/v1/generate/review/{job_id}?action=approve
```

### Rate Limits

- **Trial tier**: 10 requests/minute, 100/hour
- **Week/Month/Year tiers**: 50 requests/minute, 2000/hour

### Error Codes

- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `429`: Rate Limit Exceeded
- `500`: Internal Server Error

### Full API Reference

See [docs/api/openapi.yaml](./docs/api/openapi.yaml) for complete OpenAPI specification.

---

## Development Guide

### Development Setup

#### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+ (or Supabase for production)
- Redis 7+ (or Upstash for production)

### Local Development

1. **Clone repository**
   ```bash
   git clone https://github.com/kushalsamant/kushalsamant.github.io.git
   cd kushalsamant.github.io/apps/sketch2bim
   ```

2. **Backend setup**
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Frontend setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Run backend**
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

6. **Run frontend**
   ```bash
   cd frontend
   npm run dev
   ```

### Code Style

#### Python
- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use Black for formatting (optional)

#### TypeScript
- Use ESLint configuration
- Follow Next.js conventions
- Use TypeScript strict mode

### Testing

Run tests:
```bash
# Backend
cd backend
pytest tests/ -v

# Frontend
cd frontend
npm test
```

### Pull Request Process

1. Create feature branch from `main`
2. Make changes with tests
3. Ensure all tests pass
4. Update documentation
5. Submit PR with description

### Commit Messages

Use conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Tests
- `refactor:` Code refactoring

---

## Architecture

### Overview

Sketch2BIM is a cloud-native platform that converts architectural sketches into editable BIM models using computer vision (OpenCV) and IfcOpenShell.

### System Architecture

```
┌─────────────┐
│   Browser   │
│  (Next.js)  │
└──────┬──────┘
       │ HTTPS
       ▼
┌─────────────┐
│   Vercel    │
│  (Frontend) │
└──────┬──────┘
       │
       ▼
┌─────────────┐      ┌─────────────┐
│   Render    │◄────►│  Supabase   │
│  (Backend)  │      │ (Postgres)  │
│ + IfcOpenShell│    └─────────────┘
└──────┬──────┘
       │
       ├─────────────┐
       ▼             ▼
┌─────────────┐  ┌─────────────┐
│   Redis     │  │  BunnyCDN   │
│ (Rate Limit)│  │  (Storage)  │
└─────────────┘  └─────────────┘
```

### Components

#### Frontend (Next.js)
- **Location**: `frontend/`
- **Framework**: Next.js 14 with App Router
- **Features**: File upload, job dashboard, IFC viewer, Razorpay checkout
- **Deployment**: Vercel

#### Backend (FastAPI)
- **Location**: `backend/app/`
- **Framework**: FastAPI with Python 3.11
- **Features**: REST API, job queue, authentication, payments
- **Deployment**: Render

#### Processing Pipeline
- **Location**: `backend/app/ai/`
- **Platform**: Pure Python IfcOpenShell (runs directly on Render backend)
- **Features**: Computer vision-based sketch reading (OpenCV), IFC generation (IfcOpenShell), no Blender required
- **Note**: Uses OpenCV for geometry detection (edge detection, contour analysis, line detection), not deep learning models

#### Database
- **Type**: PostgreSQL (Supabase)
- **Models**: Users, Jobs, Payments, APIKeys

#### Async Processing
- **Type**: FastAPI BackgroundTasks
- **Purpose**: Async job processing (no Celery/Redis worker required)
- **Note**: Redis still used for rate limiting, not job queue

#### Storage
- **Type**: BunnyCDN
- **Purpose**: IFC/DWG file storage and delivery

### Data Flow

1. User uploads sketch via frontend
2. Frontend sends to backend `/api/v1/generate/upload`
3. Backend creates Job record, starts BackgroundTask
4. BackgroundTask processes sketch:
   - Reads sketch using OpenCV (edge detection, contour analysis)
   - Generates IFC using IfcOpenShell (pure Python)
   - Validates IFC (QC module)
   - Exports formats (DWG, OBJ for SketchUp)
   - Uploads to CDN (BunnyCDN)
   - Updates Job status in database
5. Frontend polls status, shows download link

### Security

- JWT authentication (NextAuth)
- API key authentication for programmatic access
- Rate limiting (per-user, per-IP)
- Security headers (CSP, HSTS, etc.)
- Signed download URLs
- Audit logging

### Monitoring

- Client error logger (console + optional backend endpoint)
- Prometheus metrics
- Grafana dashboards
- Structured logging

---

## Deployment

### Production Deployment

#### Prerequisites

- GitHub repository
- Vercel account (frontend)
- Render account (backend)
- Supabase account (database)
- Razorpay account (payments)
- BunnyCDN account (storage)
- Upstash Redis account (rate limiting)

### Frontend (Vercel)

1. **Connect Repository**
   - Go to Vercel Dashboard
   - Import GitHub repository
   - Set root directory to `frontend`

2. **Environment Variables**

> **⚠️ IMPORTANT: Centralized Environment Variables**  
> All production environment variables are in `sketch2bim.env.production` at the repository root.  
> This is the single source of truth for all production secrets across all repos (ASK, Reframe, Sketch2BIM).  
> Both the frontend (`next.config.js`) and backend (`app/config.py`) load that shared file automatically (when present) before applying their local `.env.*` overrides, so local development still works the same way.
   ```
   NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
   NEXTAUTH_SECRET=...
   SKETCH2BIM_GOOGLE_CLIENT_ID=...
   SKETCH2BIM_GOOGLE_SECRET=...
   ```

3. **Deploy**
   - Vercel auto-deploys on push to main
   - Or manually trigger from dashboard

### Backend (Render)

1. **Create Web Service**
   - New → Web Service
   - Connect GitHub repository
   - Root directory: `backend`

2. **Build & Start Commands**
   ```
   Build: pip install -r requirements.txt
   Start: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

3. **Environment Variables**
```
DATABASE_URL=postgresql://... (Supabase pooler URL)
DATABASE_PASSWORD_OVERRIDE=super-secret-password (optional; keeps password out of DATABASE_URL)
DATABASE_URL_OVERRIDE=postgresql://... (optional full override if Render injects a different URL)
REDIS_URL=redis://... (Upstash)
SECRET_KEY=...
RAZORPAY_KEY_ID=...
RAZORPAY_KEY_SECRET=...
RAZORPAY_WEBHOOK_SECRET=...
BUNNY_STORAGE_ZONE=...
BUNNY_ACCESS_KEY=...
BUNNY_CDN_HOSTNAME=...
```

4. **Health Check**
   - Path: `/health`
   - Interval: 30s

### Database (Supabase)

1. **Create Project**
   - New project in Supabase
   - Note connection string

2. **Run Migrations**
   ```bash
   # Using Alembic (if configured)
   alembic upgrade head
   ```

3. **Connection Pooler**
   - Use transaction pooler URL for backend
   - Format: `postgresql://...@...pooler.supabase.com:6543/postgres`

### Redis (Upstash)

1. **Create Database**
   - New Redis database
   - Note REST URL and token

2. **Configure Backend**
   - Set `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN`
   - Used for rate limiting only (not job queue)

### Processing Pipeline

1. **Pure Python Processing**
   - Processing runs directly on Render backend using FastAPI BackgroundTasks
   - No separate worker container required
   - IfcOpenShell processes sketches in-memory
   - No Blender or external processing services needed

2. **Environment Variables**
   - `SKETCH_READER_TYPE`: `opencv|controlnet|hybrid` (default: `hybrid`)
   - No additional processing service configuration required

### Monitoring

1. **Client Error Logger**
   - Client errors surface in the browser console during development
   - In production, enable `/api/logs/client-error` to collect reports (optional)
   - Configure alerts via Render logs or a custom monitoring workflow

2. **Prometheus**
   - Scrape `/metrics` endpoint
   - Configure Grafana data source

3. **Grafana**
   - Import dashboards from `infra/grafana/dashboards/`

### Kubernetes Deployment

See `infra/k8s/` for Kubernetes manifests.

1. **Apply Secrets**
   ```bash
   kubectl create secret generic sketch2bim-secrets \
     --from-literal=database-url=... \
     --from-literal=redis-url=...
   ```

2. **Deploy**
   ```bash
   kubectl apply -f infra/k8s/
   ```

### Alternative Deployment Options

The project supports multiple deployment platforms:

#### VPS Providers (Self-Managed)
- **Hetzner** - See `infra/hetzner/README.md` (€9-12/month, EU-focused)
- **DigitalOcean** - See `infra/digitalocean/README.md` ($6-12/month, excellent docs)
- **Vultr** - Use `infra/vps/bootstrap.sh` ($2.50-6/month, budget-friendly)
- **Linode** - Use `infra/vps/bootstrap.sh` ($5-12/month, strong performance)

#### PaaS Providers (Managed)
- **Fly.io** - See `infra/fly.io/README.md` ($5-15/month, modern PaaS, edge deployment)
- **Railway** - Simple deployment, auto-scaling ($5-20/month)
- **Render** - Currently used (see above) ($7-25/month)
- **Vercel** - Frontend deployment (free tier available)

#### Cost Comparison

| Provider | Type | Cost/Month | Best For |
|----------|------|------------|----------|
| Hetzner | VPS | €9-12 | EU users, cost-conscious |
| DigitalOcean | VPS | $6-12 | US users, good docs |
| Vultr | VPS | $2.50-6 | Budget, global presence |
| Fly.io | PaaS | $5-15 | Modern apps, edge deployment |
| Railway | PaaS | $5-20 | Simplicity, auto-scaling |
| Render | PaaS | $7-25 | Current choice, managed |
| Vercel | PaaS | Free-$20 | Frontend (current) |

For provider-agnostic VPS setup, see `infra/vps/README.md`.

### Health Checks

- Backend: `GET /health`
- Metrics: `GET /metrics`
- API Docs: `GET /docs` (development only)

### Rollback

#### Vercel
- Go to deployment history
- Click "Promote to Production"

#### Render
- Go to service → Manual Deploy
- Select previous deployment

### Monitoring Checklist

- [ ] Client error logger reporting to console/backend
- [ ] Prometheus metrics scraping
- [ ] Grafana dashboards imported
- [ ] Health checks passing
- [ ] Log aggregation working
- [ ] Cost alerts configured

---

## Windows Setup

### 1. Install Prerequisites
- [Python 3.11+](https://www.python.org/downloads/) (check "Add to PATH")
- [Node.js 18+](https://nodejs.org/)
- [Git](https://git-scm.com/downloads)
- [Supabase CLI](https://supabase.com/docs/guides/cli) (optional)

### 2. Clone Repository
```powershell
git clone https://github.com/kushalsamant/kushalsamant.github.io.git
cd kushalsamant.github.io/apps/sketch2bim
```

### 3. Backend Setup
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Backend runs at `http://localhost:8000`.

### 4. Frontend Setup
```powershell
cd ..\frontend
npm install
npm run dev
```
Frontend runs at `http://localhost:3000`.

### 5. Environment Variables
> **⚠️ Configuration:** All production environment variables are in `sketch2bim.env.production` at the repository root  
> For local development, create `.env.local` files in `backend/` and `frontend/` (these are gitignored). Do **not** commit secrets.

### 6. Processing Pipeline
Processing runs directly on the backend using pure Python IfcOpenShell:
- No Blender installation required
- No Docker containers required for processing
- Processing happens in-memory on the Render backend

### 7. Testing
1. Launch backend and frontend
2. Sign in via Google
3. Upload a sample sketch (provided in `/samples`)
4. Monitor job status and download result

### 8. Troubleshooting
- **Missing Redis:** Use Upstash (production) or install Redis locally for development
- **Database connection:** Verify Supabase connection pooler URL
- **SSL issues:** Use `pip install certifi` and restart

> Proprietary processing code is not included in public repository. Contact the team for private deployment guide if needed.

---

## Legend Parsing

### Overview

The legend parser attempts to detect and extract architectural information from sketch images, including scale information, room labels, and standard symbols. **Note**: This feature requires pytesseract (Tesseract OCR) and may return empty results if text is unclear or legends are in non-standard locations. The system gracefully degrades if OCR is unavailable.

### Features

#### Automatic Legend Detection

The legend parser automatically detects legend regions in sketch images by:
- Scanning common legend locations (bottom-right, bottom-left, top-right corners)
- Analyzing edge density to identify text-rich regions
- Using OCR (pytesseract) when available to confirm text presence

#### Scale Extraction

Supports multiple scale formats:
- **Metric scales**: `1:100`, `1/100`, `100mm = 1m`
- **Imperial scales**: `1/4" = 1'-0"`, `1" = 10'-0"`, `1 inch = 10 feet`
- **Text-based scales**: `Scale: 1:100`

#### Room Label Extraction

Detects common room types:
- Bedroom, Bathroom, Kitchen, Living Room, Dining Room
- Office, Study, Closet, Pantry, Laundry, Garage
- Hall, Hallway, Entry, Foyer, Stair, Staircase

#### Symbol Detection

**Note**: Symbol detection is optional and disabled by default. It requires:
- A trained PyTorch Faster R-CNN model file
- PyTorch and torchvision installed
- Model file path configured in `SYMBOL_DETECTOR_MODEL_PATH`

When enabled, attempts to identify standard architectural symbols (doors, windows, etc.). Without the model, only geometric detection (walls, rooms) is available.

### Installation

#### Prerequisites

The legend parser requires:
- OpenCV (`opencv-python`)
- NumPy
- Pillow (PIL)
- pytesseract (optional, for OCR)

#### Installing Tesseract OCR

**Windows:**
1. Download Tesseract installer from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
2. Run the installer (default installation path: `C:\Program Files\Tesseract-OCR`)
3. Add Tesseract to PATH or set environment variable:
   ```bash
   setx TESSDATA_PREFIX "C:\Program Files\Tesseract-OCR\tessdata"
   ```

**macOS:**
```bash
brew install tesseract
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

#### Python Dependencies

```bash
pip install opencv-python numpy pillow pytesseract
```

### Usage

#### Basic Usage

```python
from app.ai.legend_parser import parse_legend_from_sketch

# Parse legend from sketch image
result = parse_legend_from_sketch("path/to/sketch.png")

# Access parsed data
scale = result["scale"]  # e.g., "1:100"
scale_ratio = result["scale_ratio"]  # meters per pixel
room_labels = result["room_labels"]  # dict of room labels
symbols = result["symbols"]  # dict of symbols
confidence = result["confidence"]  # 0.0 to 1.0
```

### How It Works

1. **Legend Region Detection**: Scans common legend locations and analyzes edge density
2. **Scale Extraction**: Searches for scale patterns in extracted text using regex
3. **Room Label Extraction**: Matches room keywords and maps to room types
4. **Confidence Calculation**: Based on legend detection, scale found, room labels, and symbols

### Error Handling

- **Without pytesseract**: System continues with reduced functionality (edge density only)
- **Invalid Images**: Returns empty result with confidence = 0.0
- **OCR Errors**: Falls back to edge density detection

### Troubleshooting

- **"pytesseract not available" Warning**: Install Tesseract OCR and add to PATH
- **Low Confidence Scores**: Ensure clear, high-contrast legend in standard location
- **Incorrect Scale Ratios**: Use standard scale formats
- **Missing Room Labels**: Include room labels in legend, use standard room type names

### Testing

Run tests for the legend parser:
```bash
cd backend
pytest tests/test_legend_parser.py -v
```

---

## Implementation Summary

### Overview

This document summarizes the implementation of production features for Sketch2BIM. The platform uses computer vision (OpenCV) for sketch processing and IfcOpenShell for BIM generation.

### Completed Features

#### Phase 1: Production Hardening & Quality Assurance ✅

- **IFC Validation & Quality Control** (`backend/app/ai/ifc_qc.py`)
  - Comprehensive IFC validation using IfcOpenShell
  - Geometry validation (walls, rooms, topology)
  - Units and standards compliance checking
  - Auto-fix capabilities for common issues
  - QC report generation (JSON and text formats)
  - Confidence scoring (0-100)

- **Sandboxed Job Execution** (`backend/app/worker/docker_runner.py`) - Legacy/optional
  - Containerized execution (optional, not used in production)
  - Kubernetes Job API support (placeholder)
  - Resource limits (CPU, memory, GPU)
  - Network isolation
  - Timeout enforcement
  - Log streaming
  - Note: Production uses Render Python Web Services, not Docker containers

- **Cost Metering & Resource Tracking** (`backend/app/utils/costing.py`)
  - Storage and transfer cost tracking
  - Per-job cost breakdown
  - Admin cost metrics endpoint

- **Human-in-the-Loop Review Workflow**
  - `review` job status
  - Auto-flagging for low confidence (<50%) or QC failures
  - Review approval/rejection endpoint
  - Admin review queue
  - Email notifications for review jobs

#### Phase 2: Complete AI/ML Pipeline Implementation ✅

- **Pure Python Processing** (`backend/app/ai/`)
  - Sketch reading with OpenCV
  - IFC generation with IfcOpenShell (pure Python, no Blender)
  - DWG export support
  - Error handling and logging
  - Structured output

#### Phase 3: Observability & Monitoring ✅

- **Client Error Logger**: Frontend logging with optional backend reporting endpoint
- **Prometheus Metrics**: Job metrics, API request metrics, queue metrics
- **Grafana Dashboards**: Job Metrics, System Health, Cost Tracking
- **Logging Enhancement**: Structured JSON logging with correlation IDs

#### Phase 4: Security & Compliance ✅

- **Security Hardening** (`backend/app/middleware/security.py`)
  - Rate limiting middleware (per-IP, per-user)
  - Request size limits
  - Security headers (HSTS, CSP, X-Frame-Options)
  - CORS validation
  - Input sanitization

- **Audit Logging** (`backend/app/utils/audit.py`)
  - Comprehensive audit trail
  - User action tracking
  - Admin operation logging
  - Searchable audit logs
  - Compliance export

- **Data Privacy & Retention**
  - GDPR data export endpoint
  - User data deletion endpoint
  - Automatic file deletion (7 days)
  - Privacy policy tracking

#### Phase 5: Infrastructure Features ✅

- **Production infrastructure** with scalable architecture

#### Phase 6: Infrastructure & Deployment ✅

- **Production Deployment**: Render Python Web Services for backends, Vercel for frontends
- **Database**: Supabase PostgreSQL (shared across services)
- **Caching**: Upstash Redis (REST API)
- **CI/CD**: Automated deployments via Render and Vercel

#### Phase 7: Testing & Quality ✅

- **Unit Tests**: IFC QC, cost calculation, sketch readers, model generator
- **Integration Tests**: Full job flow, database operations, API endpoints

#### Phase 8: Documentation & Developer Experience ✅

- **API Documentation**: OpenAPI specification, code examples, error codes
- **Developer Documentation**: Architecture diagrams, setup guide, contributing guidelines
- **User Documentation**: Getting started guide, FAQ, best practices

### Database Schema Updates

- **New Fields in Job Model**: `qc_report_path`, `requires_review`, `cost_usd`, `review` status

### Key Improvements

1. **Production-Ready Quality Control**: Every IFC file is validated with comprehensive QC reports
2. **Security**: Rate limiting, security headers, audit logging
3. **Observability**: Client error logger plus Prometheus and Grafana dashboards
4. **Cost Transparency**: Per-job cost tracking and admin dashboards
5. **Production Infrastructure**: Scalable architecture for production use
6. **Scalability**: Kubernetes-ready, auto-scaling support
7. **Developer Experience**: Tests, documentation, CI/CD

### Next Steps for Production

1. Configure Monitoring: Enable Prometheus + Grafana (optional: `/api/logs/client-error`)
2. Database Migrations: Run Alembic migrations for new fields
3. Load Testing: Test system under production load
4. Security Audit: Review security implementation
5. Documentation Review: Ensure all docs are accurate

---

## Production Fixes

### Completed Fixes

#### 1. Fixed Syntax Error in tasks.py
- **Status**: ✅ Already correct
- **Note**: Line 105 had proper syntax - no changes needed

#### 2. Fixed Incomplete Line in tasks.py
- **Status**: ✅ Already correct
- **Note**: Line 153 had complete conditional check - no changes needed

#### 3. Updated Job Queue to Use Celery
- **Status**: ✅ Fixed
- **Files Modified**:
  - `backend/app/routes/generate.py` - Replaced `queue_sketch_processing` with `process_sketch_task.delay()`
  - `backend/app/routes/generate.py` - Fixed batch upload to use Celery

#### 4. Processing Pipeline Implementation
- **Status**: ✅ Complete
- **Note**: Processing now uses pure Python IfcOpenShell (no external services required)

#### 5. Set Up Alembic Database Migrations
- **Status**: ✅ Completed
- **Files Created**:
  - `backend/alembic.ini` - Alembic configuration
  - `backend/alembic/env.py` - Migration environment setup
  - `backend/alembic/script.py.mako` - Migration template
  - `backend/alembic/versions/001_initial_schema.py` - Initial migration with all models
  - `backend/alembic/versions/__init__.py` - Package marker
  - `backend/alembic/versions/README.md` - Migration documentation

#### 6. Environment Variables
- **Status**: ✅ Centralized
- **Location**: `sketch2bim.env.production` at the repository root

#### 7. Created Pytest Configuration
- **Status**: ✅ Completed
- **Files Created**:
  - `backend/pytest.ini` - Complete pytest configuration with:
    - Test discovery patterns
    - Coverage settings
    - Test markers
    - Coverage exclusions

#### 8. Updated Frontend for New Features
- **Status**: ✅ Completed
- **Files Modified**:
  - `frontend/components/JobCard.tsx`: Added review status badge, cost display, Approve/Reject buttons
  - `frontend/components/ReviewQueue.tsx` - New component for review queue
  - `frontend/app/dashboard/page.tsx` - Added ReviewQueue section
  - `frontend/lib/api.ts` - Updated Job interface to include `review` status, `cost_usd`, and `requires_review`

#### 9. Fixed Database Session Handling
- **Status**: ✅ Already correct
- **Note**: `backend/app/database.py` already had proper `yield db` on line 38

#### 10. Added Missing Imports and Dependencies
- **Status**: ✅ Verified
- **Note**: All imports verified, no circular dependencies found

### Additional Improvements

- **Celery Configuration**: Added `enable_utc=True` to Celery config for better timezone handling
- **Frontend API Integration**: Fixed API URLs, added proper error handling for review actions

### Testing Recommendations

1. **Database Migrations**: Run `alembic upgrade head` to verify migrations work
2. **Celery Tasks**: Test job queuing with `process_sketch_task.delay()`
3. **Frontend**: Verify review queue displays correctly and approve/reject actions work
4. **Pytest**: Run `pytest` to ensure test discovery works correctly

### Next Steps

1. Run initial Alembic migration: `cd backend && alembic upgrade head`
2. Configure environment variables in `sketch2bim.env.production` at the repository root
3. Verify frontend review queue functionality
4. Run full test suite: `cd backend && pytest`

**All production fixes from the plan have been completed!** ✨

---

## Alembic Migrations

### Initial Setup

1. Ensure all models are imported in `alembic/env.py`
2. Run migrations: `alembic upgrade head`

### Creating New Migrations

```bash
cd backend
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### Migration Files

- `001_initial_schema.py`: Initial database schema with all models

---

## License

This project contains both open-source and proprietary components:

- **Open Source**: Frontend, backend API, infrastructure code, and documentation
- **Proprietary**: Core AI processing algorithms in `backend/app/ai/` (excluded from repository)

The open-source portions are available for review and contribution. The proprietary AI processing code remains closed-source as trade secrets.

For licensing inquiries, please contact the repository maintainer.
