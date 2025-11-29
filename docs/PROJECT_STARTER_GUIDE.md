# Project Starter Guide

This guide helps you create a new project using the KVSHVL platform templates and shared components.

## Prerequisites

- Node.js 18+ installed
- Python 3.11+ installed
- Git repository access
- Basic knowledge of Next.js and FastAPI

## Quick Start

### Option 1: Using Project Generator Script (Recommended)

The easiest way to create a new project:

**Linux/macOS:**
\`\`\`bash
./scripts/create-project.sh
\`\`\`

**Windows:**
\`\`\`powershell
.\scripts\create-project.ps1
\`\`\`

Follow the interactive prompts to configure your project.

### Option 2: Manual Setup

#### 1. Copy Templates

Copy the templates to create your project:

\`\`\`bash
# Copy frontend template
cp -r templates/nextjs-app apps/your-app-name/frontend

# Copy backend template
cp -r templates/fastapi-backend apps/your-app-name/backend
\`\`\`

#### 2. Update Placeholders

Replace all placeholders in your project:

- `{{APP_NAME}}` → Your app name (lowercase, e.g., "myapp")
- `{{APP_DISPLAY_NAME}}` → Display name (e.g., "My App")
- `{{APP_PREFIX}}` → Uppercase prefix for env vars (e.g., "MYAPP")
- `{{APP_DESCRIPTION}}` → App description

You can use find/replace in your editor or a script:

**Linux/macOS:**
\`\`\`bash
find apps/your-app-name -type f -exec sed -i '' 's/{{APP_NAME}}/myapp/g' {} +
find apps/your-app-name -type f -exec sed -i '' 's/{{APP_DISPLAY_NAME}}/My App/g' {} +
# ... etc
\`\`\`

#### 3. Create Environment File

Copy the template and update values:

\`\`\`bash
cp templates/fastapi-backend/.env.template your-app-name.env.production
\`\`\`

#### 4. Install Dependencies

**Frontend:**
\`\`\`bash
cd apps/your-app-name/frontend
npm install
\`\`\`

**Backend:**
\`\`\`bash
cd apps/your-app-name/backend
pip install -r requirements.txt
\`\`\`

#### 5. Update Configuration

- Update `frontend/auth.ts` with your app name
- Update `frontend/app/layout.tsx` with metadata
- Update `backend/app/config.py` with app-specific settings
- Customize `frontend/components/HeaderWrapper.tsx` navigation

## Project Structure

Your new project should have this structure:

\`\`\`
apps/your-app-name/
├── frontend/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── pricing/
│   │   └── settings/
│   ├── components/
│   ├── lib/
│   ├── auth.ts
│   ├── package.json
│   └── tsconfig.json
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models.py
│   │   ├── database.py
│   │   ├── auth.py
│   │   └── routes/
│   └── requirements.txt
└── README.md
\`\`\`

## Using Shared Components

### Frontend Components

#### Authentication

Your project already uses shared authentication:

\`\`\`typescript
// auth.ts
import { createAuthFunctions } from "@kvshvl/shared-frontend/auth";

const auth = createAuthFunctions({
  appName: "your-app",
  frontendUrlEnvVar: "YOURAPP_FRONTEND_URL",
  defaultFrontendUrl: "https://your-app.kvshvl.in",
});

export const { signIn, signOut, auth, handlers } = auth;
\`\`\`

#### App Layout

Your layout uses the shared AppLayout:

\`\`\`typescript
// app/layout.tsx
import { AppLayout } from "@kushalsamant/design-template";

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <AppLayout
          appName="Your App"
          header={<HeaderWrapper />}
          LinkComponent={Link}
        >
          {children}
        </AppLayout>
      </body>
    </html>
  );
}
\`\`\`

#### Settings Page

Use shared settings components:

\`\`\`typescript
import { SettingsPage } from "@kvshvl/shared-frontend/settings";

export default function SettingsPage() {
  return (
    <SettingsPage
      user={userMetadata}
      showProfile={true}
      showSubscription={true}
      // ... other props
    />
  );
}
\`\`\`

### Backend Components

#### Database Models

Extend shared base models:

\`\`\`python
# app/models.py
from shared_backend.database.models import BaseUser, BasePayment

class User(BaseUser, Base):
    __tablename__ = "users"
    # Add app-specific fields here

class Payment(BasePayment, Base):
    __tablename__ = "payments"
    # Add app-specific fields here
\`\`\`

#### FastAPI App Factory

Use the shared factory to create your app:

\`\`\`python
# app/main.py
from shared_backend.api.factory import create_app

app = create_app(
    app_name="Your App",
    cors_origins=settings.cors_origins_list,
    # ... other options
)
\`\`\`

## Next Steps

1. **Customize UI**
   - Update branding in `components/HeaderWrapper.tsx`
   - Customize pricing page
   - Add app-specific pages

2. **Add Routes**
   - Create new API routes in `backend/app/routes/`
   - Add frontend pages in `frontend/app/`

3. **Configure Environment**
   - Set up database
   - Configure Razorpay
   - Set environment variables

4. **Test Locally**
   - Start frontend: `npm run dev`
   - Start backend: `python -m app.main`
   - Test all features

5. **Deploy**
   - See [Deployment Guide](DEPLOYMENT.md) for instructions

## Customization Examples

### Adding a New Route

**Backend:**
\`\`\`python
# app/routes/custom.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/custom")
async def custom_endpoint():
    return {"message": "Custom endpoint"}
\`\`\`

Register in `main.py`:
\`\`\`python
from .routes import custom
app.include_router(custom.router, prefix="/api", tags=["custom"])
\`\`\`

### Adding a New Page

**Frontend:**
\`\`\`typescript
// app/custom/page.tsx
export default function CustomPage() {
  return <div>Custom Page</div>;
}
\`\`\`

### Adding Environment Variables

**Backend Config:**
\`\`\`python
# app/config.py
class Settings(BaseSettings):
    # ... existing fields
    
    # Add custom field
    CUSTOM_SETTING: str = os.getenv("YOURAPP_CUSTOM_SETTING", "default")
\`\`\`

## Best Practices

1. **Keep It Standard**
   - Use shared components when possible
   - Follow established patterns
   - Maintain consistency

2. **Configuration**
   - Use environment variables for all config
   - Never hardcode secrets
   - Use prefixed env vars (`YOURAPP_*`)

3. **Database**
   - Extend base models, don't recreate
   - Use migrations for schema changes
   - Test with SQLite locally

4. **Authentication**
   - Use shared auth, don't reinvent
   - Centralize auth at kvshvl.in
   - Handle errors gracefully

5. **Error Handling**
   - Use standard error response format
   - Include correlation IDs
   - Log errors appropriately

## Troubleshooting

### Common Issues

**"Module not found" errors:**
- Ensure shared packages are installed
- Check workspace configuration
- Verify package.json/pyproject.toml

**Authentication not working:**
- Verify AUTH_URL is set correctly
- Check frontend URL matches auth config
- Verify OAuth redirect URLs

**Database connection failed:**
- Check DATABASE_URL format
- Verify database is running
- Check credentials

## Resources

- [Shared Components Reference](SHARED_COMPONENTS_REFERENCE.md)
- [API Documentation Template](templates/API_DOCUMENTATION.md.template)
- [Environment Variables Reference](templates/ENVIRONMENT_VARIABLES.md.template)
- [Deployment Guide](templates/DEPLOYMENT.md.template)

## Support

For questions or issues:
- Check existing documentation
- Review shared component source code
- Contact: [Get in Touch](https://kvshvl.in/getintouch)

