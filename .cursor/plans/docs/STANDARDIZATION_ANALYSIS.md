# Platform Standardization Analysis

**Purpose:** Identify reusable components, patterns, and infrastructure that can be extracted to create a base template for new projects.

**Analysis Date:** 2025-01-XX  
**Projects Analyzed:** ASK, Reframe, Sketch2BIM, and Home Site (kvshvl.in)

---

## Executive Summary

**Estimated Standardization Potential: ~75-80%**

The three projects share extensive common patterns that can be extracted into:
1. **Base Starter Template** (in home site repo)
2. **Enhanced Shared Packages** (existing packages with expanded functionality)
3. **Standard Project Structure** (consistent layouts across projects)

---

## 1. Authentication System (95% Standardizable)

### Current State
All three projects use:
- ✅ **Home site** handles central OAuth (NextAuth with Google)
- ✅ **Sub-apps** redirect to home site for auth (`auth.ts` files are nearly identical)
- ✅ **Backend** uses JWT tokens from NextAuth (`shared_backend.auth.jwt`)
- ✅ **Shared backend** already provides `decode_nextauth_jwt()`

### Standardization Opportunities

#### 1.1 Frontend Auth Module (`packages/shared-frontend/auth/`)
**Current:** Each app has its own `auth.ts` with only app name differences.

**Standardizable:**
```typescript
// packages/shared-frontend/auth/index.ts
export function createAuthConfig(appName: string, frontendUrl: string) {
  return {
    signIn: () => redirectToCentralAuth(appName, frontendUrl),
    signOut: () => redirectToCentralSignOut(),
    auth: () => null, // Handled by central site
    handlers: { GET: ..., POST: ... }
  };
}
```

**Files to Standardize:**
- `apps/ask/frontend/auth.ts` → Use shared
- `apps/reframe/auth.ts` → Use shared  
- `apps/sketch2bim/frontend/auth.ts` → Use shared

**Benefit:** New projects get auth with 1 line of code.

---

#### 1.2 Backend Auth Dependencies (Already Standardized ✅)
**Current:** All backends use `shared_backend.auth.jwt.decode_nextauth_jwt()`

**Status:** ✅ Already standardized in `packages/shared-backend/auth/`

---

## 2. Payment & Subscription System (90% Standardizable)

### Current State
All projects use:
- ✅ Razorpay integration
- ✅ Unified pricing (₹1,299/week, ₹3,499/month, ₹3,999/year)
- ✅ Unified plan IDs
- ✅ Standardized tier names ("weekly", "monthly", "yearly")
- ✅ Shared subscription utilities

### Standardization Opportunities

#### 2.1 Frontend Payment Components
**Current:** Each app has custom pricing pages and checkout flows.

**Standardizable:**
- **Pricing Page Template** - Create reusable pricing page component
- **Checkout Flow** - Standard Razorpay checkout wrapper
- **Subscription Status Display** - User subscription badge/display

**Create in `packages/shared-frontend/payments/`:**
```typescript
// Reusable PricingPage component
export function PricingPage({
  appName,
  tiers: ['week', 'monthly', 'yearly'],
  features: {...},
  onSubscribe: (tier) => {...}
})

// Reusable SubscriptionBadge component  
export function SubscriptionBadge({ tier, status })

// Reusable PaymentHistory component
export function PaymentHistory({ payments })
```

**Files to Standardize:**
- Pricing pages: `apps/*/app/pricing/page.tsx`
- Payment history: `apps/sketch2bim/frontend/app/settings/payments/page.tsx`
- Subscription displays: Various components showing tier status

**Benefit:** New projects get payment system in ~30 minutes.

---

#### 2.2 Backend Payment Routes (Partially Standardized)
**Current:** Payment routes are very similar but app-specific.

**Standardizable:** Create base payment router in `packages/shared-backend/payments/`:
```python
# packages/shared-backend/payments/router.py
class BasePaymentRouter:
    def __init__(self, app_name: str, settings):
        self.app_name = app_name
        self.settings = settings
    
    def create_checkout_endpoint(self): ...
    def create_webhook_endpoint(self): ...
```

**Files to Standardize:**
- `apps/ask/api/routes/payments.py` - Extract to base + app-specific logic
- `apps/sketch2bim/backend/app/routes/payments.py` - Extract to base + app-specific logic
- Reframe handles payments in frontend (different pattern)

**Benefit:** Backend payment setup reduces from ~500 lines to ~50 lines per app.

---

#### 2.3 Subscription Utilities (Already Standardized ✅)
**Current:** All apps use `shared_backend.subscription.utils`

**Status:** ✅ Already standardized

---

## 3. Database & Models (70% Standardizable)

### Current State
- ✅ Shared database connection utilities
- ✅ Similar User model structures
- ✅ Similar Payment model structures
- ❌ App-specific business logic models (QA pairs, Jobs, etc.)

### Standardization Opportunities

#### 3.1 Base User Model
**Create in `packages/shared-backend/database/models.py`:**
```python
class BaseUser(Base):
    """Standard user model with subscriptions"""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    google_id = Column(String, unique=True, index=True)
    
    # Subscription fields (standardized)
    subscription_tier = Column(String, default="trial")  # trial|week|monthly|yearly
    subscription_status = Column(String, default="inactive")
    subscription_expires_at = Column(DateTime)
    razorpay_customer_id = Column(String, unique=True)
    razorpay_subscription_id = Column(String)
    subscription_auto_renew = Column(Boolean, default=False)
    
    # Common metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)
```

**Usage:**
```python
# apps/ask/api/models_db.py
from shared_backend.database.models import BaseUser

class User(BaseUser):
    __tablename__ = "users"
    __table_args__ = {"schema": "ask_schema"}
    
    # Add app-specific fields
    credits = Column(Integer, default=0)
```

**Benefit:** Consistent user model across all apps.

---

#### 3.2 Base Payment Model
**Already partially in `packages/shared-backend/payments/models.py`**

**Enhancement:** Make it a concrete base class instead of abstract:
```python
class BasePayment(Base):
    """Standard payment model"""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    razorpay_payment_id = Column(String, unique=True)
    razorpay_order_id = Column(String)
    amount = Column(Integer)  # in paise
    currency = Column(String, default="INR")
    status = Column(String)
    product_type = Column(String)  # week|monthly|yearly|one_time
    processing_fee = Column(Integer)
    completed_at = Column(DateTime)
```

---

## 4. Frontend Layout & Structure (85% Standardizable)

### Current State
All three apps have nearly identical layouts:
- ✅ Same `layout.tsx` structure
- ✅ Same `ThemeProvider`, `AppFooter`, `HeaderWrapper`
- ✅ Same social links
- ✅ Same legal links
- ✅ Same accessibility patterns (skip links)

### Standardization Opportunities

#### 4.1 Standard App Layout Component
**Create in `packages/design-system/src/components/AppLayout.tsx`:**
```typescript
export function AppLayout({
  appName,
  appDescription,
  children,
  headerProps,
  footerProps,
  showCookieBanner = false,
  additionalProviders = []
}) {
  return (
    <html>
      <body>
        <ThemeProvider>
          <SessionProvider>
            {/* Standard skip link */}
            <HeaderWrapper {...headerProps} />
            <main id="main-content">{children}</main>
            <AppFooter {...footerProps} />
            {showCookieBanner && <CookieBanner />}
          </SessionProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
```

**Usage:**
```typescript
// apps/newproject/app/layout.tsx
export default function RootLayout({ children }) {
  return (
    <AppLayout
      appName="New Project"
      appDescription="Description"
      headerProps={{ productName: "New Project" }}
      footerProps={{ legalLinks, socialLinks, branding }}
      showCookieBanner={true}
    >
      {children}
    </AppLayout>
  );
}
```

**Benefit:** New projects get consistent layout in 10 lines.

---

#### 4.2 Settings Page Template
**Current:** Each app has similar settings pages showing:
- User profile
- Subscription status
- Payment history
- Account management

**Standardizable:** Create reusable SettingsPage component:
```typescript
export function SettingsPage({
  user,
  sections: [
    { title: "Profile", component: ProfileSection },
    { title: "Subscription", component: SubscriptionSection },
    { title: "Payment History", component: PaymentHistorySection },
    { title: "Account", component: AccountSection }
  ]
})
```

---

## 5. Configuration Management (80% Standardizable)

### Current State
All apps:
- ✅ Use `shared_backend.config.base.BaseSettings`
- ✅ Load from `{app}.env.production` files
- ✅ Use prefixed environment variables (`ASK_*`, `SKETCH2BIM_*`, etc.)
- ✅ Similar database URL override patterns
- ✅ Similar CORS configuration

### Standardization Opportunities

#### 5.1 Base Configuration Generator
**Create in `packages/shared-backend/config/generator.py`:**
```python
def create_app_settings(
    app_name: str,
    default_database_url: str,
    default_cors_origins: List[str],
    custom_fields: Dict = None
) -> Type[BaseSettings]:
    """Generate a Settings class for a new app"""
    
    class AppSettings(BaseSettings):
        APP_NAME: str = app_name
        DATABASE_URL: str = os.getenv(f"{app_name.upper()}_DATABASE_URL", default_database_url)
        CORS_ORIGINS: str = ",".join(default_cors_origins)
        # ... standard fields
        
        # Add custom fields
        if custom_fields:
            for key, value in custom_fields.items():
                setattr(AppSettings, key, value)
    
    return AppSettings
```

**Usage:**
```python
# apps/newproject/backend/config.py
from shared_backend.config.generator import create_app_settings

Settings = create_app_settings(
    app_name="NewProject",
    default_database_url="postgresql://...",
    default_cors_origins=["https://newproject.kvshvl.in"],
    custom_fields={
        "SPECIAL_FIELD": os.getenv("NEWPROJECT_SPECIAL_FIELD", "default")
    }
)
```

**Benefit:** Consistent configuration across all apps.

---

## 6. API Structure & FastAPI Setup (75% Standardizable)

### Current State
All backends:
- ✅ FastAPI with similar middleware (CORS, error handling)
- ✅ Similar route organization
- ✅ Similar authentication dependencies
- ✅ Similar health check endpoints
- ❌ App-specific routes (generate, qa_pairs, etc.)

### Standardization Opportunities

#### 6.1 Base FastAPI Application Factory
**Create in `packages/shared-backend/api/factory.py`:**
```python
def create_app(
    app_name: str,
    version: str,
    settings,
    routes: List[APIRouter],
    enable_monitoring: bool = True,
    enable_feasibility: bool = False
) -> FastAPI:
    """Create a standardized FastAPI application"""
    
    app = FastAPI(
        title=f"{app_name} API",
        version=version,
        description=f"API for {app_name}"
    )
    
    # Standard middleware
    app.add_middleware(CORSMiddleware, ...)
    app.add_middleware(ErrorHandlingMiddleware, ...)
    
    # Standard routes
    app.include_router(health_router, prefix="/health")
    if enable_monitoring:
        app.include_router(monitoring_router, prefix="/api/monitoring")
    
    # App-specific routes
    for route in routes:
        app.include_router(route)
    
    return app
```

**Usage:**
```python
# apps/newproject/backend/app/main.py
from shared_backend.api.factory import create_app
from .routes import my_routes

app = create_app(
    app_name="NewProject",
    version="1.0.0",
    settings=settings,
    routes=[my_routes.router],
    enable_monitoring=True
)
```

**Benefit:** Consistent API setup in ~20 lines.

---

## 7. Deployment Configuration (90% Standardizable)

### Current State
- ✅ Unified `render.yaml` with all services
- ✅ Standardized environment variable naming
- ✅ Similar health check paths
- ✅ Similar build/start commands

### Standardization Opportunities

#### 7.1 Render Blueprint Generator
**Create script in home site:**
```python
# scripts/generate_render_service.py
def generate_render_service(
    app_name: str,
    backend_path: str,
    database_schema: str,
    additional_env_vars: Dict = None
) -> Dict:
    """Generate Render service configuration"""
    
    return {
        "type": "web",
        "name": f"{app_name.lower()}-backend",
        "runtime": "python",
        "rootDir": backend_path,
        "buildCommand": "pip install -r requirements.txt",
        "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
        "healthCheckPath": "/health",
        "envVars": [
            # Standard env vars
            {"key": f"{app_name.upper()}_APP_NAME", "value": app_name},
            {"key": f"{app_name.upper()}_DATABASE_SCHEMA", "value": database_schema},
            # ... standard vars
            # Custom vars
            *(additional_env_vars or [])
        ]
    }
```

**Benefit:** New projects added to `render.yaml` in seconds.

---

## 8. Frontend Package Structure (80% Standardizable)

### Current State
All frontends:
- ✅ Next.js 14-15
- ✅ Same design system package (`@kushalsamant/design-template`)
- ✅ Similar folder structure (`app/`, `components/`, `lib/`)
- ✅ Similar API client patterns
- ❌ Different Next.js versions (14 vs 15)

### Standardization Opportunities

#### 8.1 Standard Next.js Template
**Create `templates/nextjs-app/` in home site:**
```
templates/nextjs-app/
├── app/
│   ├── layout.tsx          # Uses AppLayout component
│   ├── page.tsx            # Landing page template
│   ├── pricing/
│   │   └── page.tsx        # Uses PricingPage component
│   ├── settings/
│   │   └── page.tsx        # Uses SettingsPage component
│   └── api/
│       └── auth/
│           └── route.ts    # Redirects to central auth
├── components/
│   ├── HeaderWrapper.tsx   # Standard header
│   └── ...
├── lib/
│   ├── api.ts              # Standard API client
│   └── ...
├── auth.ts                 # Uses shared-frontend/auth
├── package.json            # Standard dependencies
├── next.config.js          # Standard config
└── tsconfig.json           # Standard config
```

**Usage:**
```bash
# Create new project from template
cp -r templates/nextjs-app apps/newproject/frontend
cd apps/newproject/frontend
npm install
# Customize app name, colors, etc.
```

**Benefit:** New frontend projects in 5 minutes.

---

## 9. Documentation & Scripts (70% Standardizable)

### Current State
- ✅ Standardized README structure
- ✅ Similar deployment checklists
- ✅ Similar environment variable docs
- ✅ Similar troubleshooting guides

### Standardization Opportunities

#### 9.1 Documentation Templates
**Create in `docs/templates/`:**
- `README.md.template` - App README with placeholders
- `DEPLOYMENT.md.template` - Deployment guide template
- `ENVIRONMENT_VARIABLES.md.template` - Env var documentation template
- `API_DOCUMENTATION.md.template` - API docs template

**Benefit:** Consistent documentation across projects.

---

## 10. Testing Infrastructure (60% Standardizable)

### Current State
- Sketch2BIM has comprehensive tests
- ASK and Reframe have minimal testing
- Similar test patterns where they exist

### Standardization Opportunities

#### 10.1 Base Test Utilities
**Create in `packages/shared-backend/tests/`:**
```python
# Base test fixtures
@pytest.fixture
def test_user(db):
    """Create a test user"""
    ...

@pytest.fixture
def authenticated_client(app, test_user):
    """Create authenticated test client"""
    ...

@pytest.fixture
def mock_razorpay():
    """Mock Razorpay responses"""
    ...
```

**Benefit:** New projects get testing infrastructure ready.

---

## Implementation Priority

### Phase 1: High-Value, Low-Effort (Week 1-2)
1. ✅ **Frontend Auth Module** - Extract identical `auth.ts` files
2. ✅ **App Layout Component** - Standardize layout.tsx structure
3. ✅ **Base User/Payment Models** - Extract common database models

### Phase 2: High-Value, Medium-Effort (Week 3-4)
4. ✅ **Pricing Components** - Reusable pricing page and checkout
5. ✅ **Settings Page Template** - Standard settings page
6. ✅ **FastAPI Application Factory** - Standard backend setup

### Phase 3: Medium-Value, High-Effort (Month 2)
7. ✅ **Next.js Template** - Complete frontend starter
8. ✅ **Configuration Generator** - Dynamic config creation
9. ✅ **Render Blueprint Generator** - Automated deployment config

### Phase 4: Nice-to-Have (Month 3+)
10. ✅ **Documentation Templates** - Standard docs
11. ✅ **Testing Utilities** - Base test infrastructure
12. ✅ **CLI Tool** - Project generator script

---

## Project Starter Template Structure

**Location:** `templates/project-starter/` in home site

```
templates/project-starter/
├── backend/
│   ├── app/
│   │   ├── main.py              # Uses FastAPI factory
│   │   ├── config.py            # Uses config generator
│   │   ├── models.py            # Extends BaseUser, BasePayment
│   │   ├── auth.py              # Standard auth dependencies
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── my_feature.py    # App-specific routes
│   ├── requirements.txt         # Standard dependencies
│   └── README.md
├── frontend/
│   ├── app/
│   │   ├── layout.tsx           # Uses AppLayout
│   │   ├── page.tsx
│   │   ├── pricing/
│   │   │   └── page.tsx         # Uses PricingPage
│   │   └── settings/
│   │       └── page.tsx         # Uses SettingsPage
│   ├── auth.ts                  # Uses shared-frontend/auth
│   ├── package.json
│   └── README.md
├── docs/
│   ├── README.md.template
│   ├── DEPLOYMENT.md.template
│   └── ENVIRONMENT_VARIABLES.md.template
├── {app_name}.env.production.template
└── README.md                    # Setup instructions
```

---

## Benefits Summary

### Time Savings
- **New Project Setup:** ~8 hours → ~30 minutes (16x faster)
- **Payment Integration:** ~4 hours → ~30 minutes (8x faster)
- **Auth Setup:** ~2 hours → ~5 minutes (24x faster)
- **Layout Setup:** ~2 hours → ~10 minutes (12x faster)

### Consistency
- ✅ Unified authentication experience
- ✅ Consistent payment flows
- ✅ Standardized database models
- ✅ Uniform API structure
- ✅ Consistent documentation

### Maintainability
- ✅ Single source of truth for common patterns
- ✅ Bug fixes benefit all projects
- ✅ Easier onboarding for new developers
- ✅ Reduced code duplication

### Quality
- ✅ Tested, proven patterns
- ✅ Built-in best practices
- ✅ Accessibility by default
- ✅ Security patterns included

---

## Next Steps

1. **Create standardization branch** in home site repo
2. **Start with Phase 1 items** (highest ROI)
3. **Migrate one existing project** to use new shared components
4. **Document usage patterns** in `docs/PROJECT_STARTER_GUIDE.md`
5. **Create project generator script** (`scripts/create-project.sh`)

---

## Estimated Effort

- **Phase 1:** 40-60 hours
- **Phase 2:** 60-80 hours
- **Phase 3:** 80-120 hours
- **Phase 4:** 40-60 hours
- **Total:** ~220-320 hours (~6-8 weeks for 1 developer)

**ROI:** Every new project saves ~16 hours of setup time, so ROI is positive after 2-3 projects.

