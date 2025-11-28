# Shared Frontend Package

Shared TypeScript/Next.js utilities for KVSHVL platform applications.

## Packages

- **auth**: NextAuth configuration
- **payments**: Razorpay client utilities
- **cost-monitoring**: Cost monitoring UI components

## Installation

```bash
# From monorepo root
npm install

# Or install in development mode
cd packages/shared-frontend
npm install
```

## Usage

```typescript
import { getAuthConfig } from '@kvshvl/shared-frontend/auth';
import { createRazorpayCheckout } from '@kvshvl/shared-frontend/payments';
```

