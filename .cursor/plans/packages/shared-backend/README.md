# Shared Backend Package

Shared Python utilities for KVSHVL platform applications.

## Packages

- **auth**: Authentication utilities (JWT, user dependencies)
- **payments**: Razorpay integration and webhook handling
- **database**: Database models and schema utilities
- **subscription**: Subscription management
- **cost-monitoring**: Cost tracking and alerts
- **config**: Shared configuration

## Installation

```bash
# From monorepo root
poetry add --path ../packages/shared-backend

# Or install in development mode
cd packages/shared-backend
poetry install
```

## Usage

```python
from shared_backend.auth import get_current_user
from shared_backend.payments import verify_razorpay_webhook
from shared_backend.database import get_db
```

