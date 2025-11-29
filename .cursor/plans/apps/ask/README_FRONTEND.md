# ASK Frontend - Setup Guide

This document describes the frontend implementation for the ASK Research Tool.

## Architecture

- **Backend**: FastAPI server (Python) - `api/` directory
- **Frontend**: Next.js 16 with TypeScript - `frontend/` directory
- **Design System**: `@kushalsamant/design-template` npm package

## Prerequisites

- Node.js 18+ and npm
- Python 3.8+ (for backend)
- FastAPI dependencies installed

## Setup Instructions

### 1. Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run FastAPI server
cd api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.local.example .env.local
# Edit .env.local and set NEXT_PUBLIC_API_URL=http://localhost:8000

# Run development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Project Structure

```
ask/
├── api/                          # FastAPI backend
│   ├── main.py                  # FastAPI app entry point
│   ├── models.py                 # Pydantic data models
│   ├── routes/                   # API endpoints
│   │   ├── qa_pairs.py          # Q&A pairs endpoints
│   │   ├── themes.py             # Themes endpoints
│   │   ├── images.py             # Image serving
│   │   ├── generate.py           # Content generation
│   │   └── stats.py              # Statistics
│   └── services/                 # Business logic
│       ├── csv_service.py        # CSV reading
│       ├── image_service.py      # Image handling
│       └── generation_service.py # Content generation
├── frontend/                     # Next.js frontend
│   ├── app/                     # Next.js app directory
│   │   ├── layout.tsx           # Root layout
│   │   ├── page.tsx             # Homepage
│   │   ├── browse/              # Browse page
│   │   ├── qa/[id]/             # Q&A detail page
│   │   └── generate/            # Generate page
│   ├── components/               # React components
│   │   ├── QAItem.tsx           # Q&A card component
│   │   ├── ImagePreview.tsx     # Image preview component
│   │   ├── ThemeFilter.tsx      # Theme filter component
│   │   └── GenerationForm.tsx   # Generation form
│   └── lib/                     # Utilities
│       └── api.ts               # API client
├── images/                       # Generated images (served by FastAPI)
└── log.csv                       # Q&A data (read by FastAPI)
```

## API Endpoints

- `GET /api/qa-pairs` - List Q&A pairs (with pagination and theme filtering)
- `GET /api/qa-pairs/{id}` - Get single Q&A pair
- `GET /api/themes` - List all themes with counts
- `GET /api/stats` - Get overall statistics
- `POST /api/generate` - Trigger content generation
- `GET /static/images/{filename}` - Serve image files

## Features

- **Browse Q&A Pairs**: Grid view with theme filtering and search
- **Q&A Detail View**: Full question/answer with Instagram story preview
- **Content Generation**: Trigger new Q&A pair generation
- **Theme Filtering**: Filter by research theme
- **Responsive Design**: Mobile and desktop optimized
- **Dark Mode**: Uses design template theme system

## Environment Variables

### Frontend (.env.local)

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (ask.env)

See `ask.env.production` at the repository root for production configuration options.

## Development

### Running Both Servers

Terminal 1 (Backend):
```bash
cd api
uvicorn main:app --reload
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

### Building for Production

```bash
# Frontend
cd frontend
npm run build
npm start

# Backend
cd api
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Design Template Updates

Dependabot is configured to automatically check for updates to `@kushalsamant/design-template` daily. Pull requests will be created when new versions are available.

## Troubleshooting

### Images not loading

- Ensure FastAPI server is running
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Verify images exist in `images/` directory
- Check CORS settings in `api/main.py`

### API connection errors

- Verify backend is running on port 8000
- Check CORS origins in `api/main.py`
- Ensure `NEXT_PUBLIC_API_URL` matches backend URL

### Build errors

- Run `npm install` to ensure all dependencies are installed
- Check Node.js version (18+ required)
- Clear `.next` directory and rebuild

## Deployment

### Frontend

Deploy to Vercel, Netlify, or any Next.js-compatible hosting:

```bash
cd frontend
npm run build
```

### Backend

Deploy FastAPI to any Python hosting (Railway, Render, etc.):

```bash
cd api
pip install -r ../requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

Ensure:
- CORS origins include frontend domain
- Images directory is accessible
- CSV file is readable
- Environment variables are set

