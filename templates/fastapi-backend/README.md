# FastAPI Backend Template

This template provides a standardized FastAPI backend structure for KVSHVL platform apps.

## Features

- ✅ Standardized FastAPI app using factory pattern from `shared-backend`
- ✅ Base database models from `shared-backend/database/models.py`
- ✅ Standard configuration extending BaseSettings
- ✅ Common middleware (CORS, error handling)
- ✅ Health check endpoints
- ✅ Database initialization
- ✅ TypeScript-style type safety with Pydantic

## Quick Start

1. Copy this template to your new app directory:
   ```bash
   cp -r templates/fastapi-backend apps/your-app-name/backend
   ```

2. Update the app name in:
   - `app/config.py` - Update Settings class (APP_NAME, prefixed env vars)
   - `app/main.py` - Update app title and description
   - `requirements.txt` - Ensure all dependencies are listed

3. Set up environment variables (see `.env.template`)

4. Install dependencies:
   ```bash
   cd apps/your-app-name/backend
   pip install -r requirements.txt
   ```

5. Run the server:
   ```bash
   python -m app.main
   # or
   uvicorn app.main:app --reload
   ```

## Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py             # FastAPI app (uses factory)
│   ├── config.py           # Settings (extends BaseSettings)
│   ├── database.py         # Database connection setup
│   ├── models.py           # Database models (extends BaseUser, BasePayment)
│   ├── auth.py             # Authentication dependencies
│   └── routes/
│       ├── __init__.py
│       └── example.py      # Example route
├── requirements.txt
└── README.md
```

## Customization

- Add app-specific routes in `app/routes/`
- Extend database models in `app/models.py`
- Add app-specific settings in `app/config.py`
- Configure CORS origins in `app/config.py`

