# Shared Components Reference

Complete reference for all shared components and utilities available across KVSHVL platform projects.

## Frontend Components

### Authentication (`@kvshvl/shared-frontend/auth`)

Centralized authentication module for all apps.

#### `createAuthFunctions(config)`

Creates authentication functions for an app.

**Parameters:**
- `config.appName` - App identifier (e.g., "ask")
- `config.frontendUrlEnvVar` - Environment variable name for frontend URL
- `config.defaultFrontendUrl` - Default frontend URL

**Returns:**
- `signIn()` - Redirect to sign in
- `signOut()` - Redirect to sign out
- `auth()` - Get current auth session
- `handlers` - API route handlers

**Example:**
\`\`\`typescript
import { createAuthFunctions } from "@kvshvl/shared-frontend/auth";

const auth = createAuthFunctions({
  appName: "myapp",
  frontendUrlEnvVar: "MYAPP_FRONTEND_URL",
  defaultFrontendUrl: "https://myapp.kvshvl.in",
});
\`\`\`

### Payments (`@kvshvl/shared-frontend/payments`)

Shared payment utilities for Razorpay integration.

#### Types

\`\`\`typescript
type SubscriptionTier = "trial" | "week" | "monthly" | "yearly";
type PaymentType = "one_time" | "subscription";

interface PricingTier {
  tier: SubscriptionTier;
  name: string;
  price: string;
  period: string;
  description: string;
  features: string[];
  cta: string;
}
\`\`\`

#### `loadRazorpayScript()`

Dynamically loads Razorpay checkout script.

**Returns:** Promise<void>

#### `createCheckoutSession(tier, paymentType, apiEndpoint)`

Creates a checkout session with the backend.

**Parameters:**
- `tier` - Subscription tier
- `paymentType` - Payment type
- `apiEndpoint` - Backend API endpoint

**Returns:** Promise<CheckoutSessionResponse>

#### `openRazorpayCheckout(options, onError)`

Opens Razorpay checkout modal.

**Parameters:**
- `options` - Razorpay checkout options
- `onError` - Error callback

**Returns:** Promise<void>

### Settings (`@kvshvl/shared-frontend/settings`)

Reusable settings page components.

#### `SettingsPage`

Main settings page layout component.

**Props:**
- `user` - User metadata
- `showProfile` - Show profile section
- `showSubscription` - Show subscription section
- `showPaymentHistory` - Show payment history
- `apiEndpoints` - API endpoint URLs
- `onSignOut` - Sign out callback

#### `ProfileSection`

Displays user profile information.

**Props:**
- `user` - User metadata
- `showUserId` - Show user ID
- `additionalFields` - Extra fields to display

#### `SubscriptionSection`

Displays subscription status and management.

**Props:**
- `user` - User metadata
- `onManageSubscription` - Manage subscription callback
- `onCancelSubscription` - Cancel subscription callback

#### `PaymentHistorySection`

Displays payment history.

**Props:**
- `userId` - User ID
- `apiEndpoint` - Payment history API endpoint
- `maxItems` - Maximum items to display

### Design System (`@kushalsamant/design-template`)

Shared design system components.

#### `AppLayout`

Standard application layout component.

**Props:**
- `appName` - Application name
- `header` - Header component
- `LinkComponent` - Next.js Link component
- `legalLinks` - Legal links array
- `socialLinks` - Social links array
- `branding` - Footer branding text

**Example:**
\`\`\`typescript
import { AppLayout } from "@kushalsamant/design-template";

<AppLayout
  appName="My App"
  header={<HeaderWrapper />}
  LinkComponent={Link}
>
  {children}
</AppLayout>
\`\`\`

## Backend Components

### Database Models (`shared_backend.database.models`)

Base database models to extend.

#### `BaseUser`

Base user model with common fields.

**Fields:**
- `id`, `email`, `name`, `google_id`
- `subscription_tier`, `subscription_status`, `subscription_expires_at`
- `razorpay_customer_id`, `razorpay_subscription_id`
- `created_at`, `updated_at`, `last_login`, `is_active`

**Usage:**
\`\`\`python
from shared_backend.database.models import BaseUser

class User(BaseUser, Base):
    __tablename__ = "users"
    # Add app-specific fields here
\`\`\`

#### `BasePayment`

Base payment model with common fields.

**Fields:**
- `id`, `user_id`
- `razorpay_payment_id`, `razorpay_order_id`
- `amount`, `currency`, `status`
- `product_type`, `credits_added`
- `processing_fee`, `created_at`, `completed_at`

**Usage:**
\`\`\`python
from shared_backend.database.models import BasePayment

class Payment(BasePayment, Base):
    __tablename__ = "payments"
    # Add app-specific fields here
\`\`\`

### API Factory (`shared_backend.api.factory`)

FastAPI application factory.

#### `create_app(...)`

Creates a standardized FastAPI application.

**Parameters:**
- `app_name` - Application name
- `version` - API version
- `cors_origins` - List of CORS origins
- `lifespan` - Startup/shutdown lifecycle
- `enable_docs` - Enable OpenAPI docs
- `enable_error_handlers` - Enable error handlers
- `debug` - Debug mode

**Returns:** FastAPI application instance

**Example:**
\`\`\`python
from shared_backend.api.factory import create_app

app = create_app(
    app_name="My App",
    cors_origins=["https://myapp.kvshvl.in"],
    enable_docs=True,
    debug=False
)
\`\`\`

### Middleware (`shared_backend.api.middleware`)

Common FastAPI middleware.

#### `setup_cors_middleware(app, cors_origins)`

Sets up CORS middleware.

#### `setup_standard_error_handlers(app, include_correlation, debug)`

Sets up standard error handlers.

### Configuration (`shared_backend.config.base`)

Base configuration settings.

#### `BaseSettings`

Base Pydantic settings class.

**Common Fields:**
- `APP_NAME`, `APP_ENV`, `DEBUG`
- `AUTH_URL`, `NEXTAUTH_SECRET`

**Usage:**
\`\`\`python
from shared_backend.config.base import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "My App"
    # Add app-specific fields
\`\`\`

#### `get_env_with_fallback(prefixed_key, unprefixed_key, default)`

Get environment variable with fallback chain.

#### `get_env_int_with_fallback(prefixed_key, unprefixed_key, default)`

Get integer environment variable with fallback.

### Configuration Generator (`shared_backend.config.generator`)

Generate Settings classes dynamically.

#### `generate_settings_class(app_name, app_display_name, app_prefix, custom_fields)`

Generates a Settings class configuration file.

## Test Utilities (`shared_backend.tests`)

Shared test fixtures and helpers.

### Fixtures

#### `db_engine`

In-memory SQLite database engine.

#### `db_session`

Database session for testing.

#### `test_user`

Test user fixture.

#### `test_payment`

Test payment fixture.

### Helpers

#### `create_razorpay_webhook_payload(event, payload_data)`

Create mock Razorpay webhook payload.

#### `create_mock_razorpay_checkout_response(order_id, amount, currency)`

Create mock Razorpay checkout response.

#### `assert_success_response(response, expected_data)`

Assert successful API response.

#### `assert_error_response(response, expected_status, expected_code)`

Assert error API response.

## Usage Examples

### Complete Frontend Setup

\`\`\`typescript
// auth.ts
import { createAuthFunctions } from "@kvshvl/shared-frontend/auth";
export const { signIn, signOut, auth, handlers } = createAuthFunctions({
  appName: "myapp",
  frontendUrlEnvVar: "MYAPP_FRONTEND_URL",
  defaultFrontendUrl: "https://myapp.kvshvl.in",
});

// app/layout.tsx
import { AppLayout } from "@kushalsamant/design-template";
import HeaderWrapper from "@/components/HeaderWrapper";

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <AppLayout appName="My App" header={<HeaderWrapper />} LinkComponent={Link}>
          {children}
        </AppLayout>
      </body>
    </html>
  );
}
\`\`\`

### Complete Backend Setup

\`\`\`python
# app/config.py
from shared_backend.config.base import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "My App"

# app/models.py
from shared_backend.database.models import BaseUser, BasePayment

class User(BaseUser, Base):
    __tablename__ = "users"

class Payment(BasePayment, Base):
    __tablename__ = "payments"

# app/main.py
from shared_backend.api.factory import create_app
from .config import settings

app = create_app(
    app_name=settings.APP_NAME,
    cors_origins=settings.cors_origins_list,
)
\`\`\`

## Best Practices

1. **Always use shared components** when available
2. **Extend base classes** instead of recreating
3. **Follow naming conventions** for consistency
4. **Use environment variables** for configuration
5. **Test with shared fixtures** for consistency

## Related Documentation

- [Project Starter Guide](PROJECT_STARTER_GUIDE.md)
- [API Documentation Template](templates/API_DOCUMENTATION.md.template)
- [Environment Variables Reference](templates/ENVIRONMENT_VARIABLES.md.template)

