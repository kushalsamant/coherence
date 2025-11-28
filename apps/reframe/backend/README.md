# Reframe FastAPI Backend

FastAPI backend for Reframe AI text reframing service, deployed on Render.

## Architecture

- **Framework**: FastAPI
- **Authentication**: NextAuth JWT validation
- **Storage**: Upstash Redis (REST API)
- **AI**: Groq API (llama-3.1-8b-instant)
- **Deployment**: Render

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
- `GROQ_API_KEY` - Groq API key
- `UPSTASH_REDIS_REST_URL` - Upstash Redis REST URL
- `UPSTASH_REDIS_REST_TOKEN` - Upstash Redis REST token
- `NEXTAUTH_SECRET` - JWT secret (same as frontend)
- `CORS_ORIGINS` - Comma-separated list of allowed origins
- `FREE_LIMIT` - Free tier request limit (default: 5)

3. Run locally:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

### POST /api/reframe
Reframe text using AI with specified tone.

**Request:**
```json
{
  "text": "Text to reframe...",
  "tone": "conversational",
  "generation": "any"
}
```

**Response:**
```json
{
  "output": "Reframed text...",
  "usage": 3
}
```

**Authentication:** Bearer token (NextAuth JWT)

### GET /health
Health check endpoint.

## Deployment

Deploy to Render using `render.yaml`:

1. Connect repository to Render
2. Render will detect `render.yaml` and configure the service
3. Set environment variables in Render dashboard
4. Deploy

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration
│   ├── auth.py              # JWT authentication
│   ├── models.py            # Pydantic models
│   ├── routes/
│   │   └── reframe.py       # Main reframe endpoint
│   └── services/
│       ├── redis_service.py           # Upstash Redis client
│       ├── user_metadata_service.py    # User metadata management
│       ├── subscription_service.py     # Subscription logic
│       ├── tone_service.py             # Tone system
│       ├── groq_service.py             # Groq API client
│       └── groq_monitor.py             # Usage tracking
└── requirements.txt
```

