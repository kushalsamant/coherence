# Fly.io Deployment

Deployment guide for Sketch-to-BIM on Fly.io.

## Overview

Fly.io is a modern PaaS (Platform as a Service) that provides:
- Global edge deployment
- Docker-based containers
- Auto-scaling
- Built-in load balancing
- Simple deployment process

## Advantages

- **Easier than VPS** - No server management required
- **Global Edge** - Deploy close to users worldwide
- **Auto-scaling** - Automatically scales based on traffic
- **Built-in SSL** - Automatic HTTPS certificates
- **Simple CLI** - Easy deployment and management

## Prerequisites

1. Install Fly CLI:
   ```bash
   # macOS/Linux
   curl -L https://fly.io/install.sh | sh
   
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   ```

2. Sign up at [fly.io](https://fly.io) and login:
   ```bash
   fly auth login
   ```

## Quick Start

### 1. Initialize Fly App

```bash
cd backend
fly launch
```

This will:
- Create a `fly.toml` configuration file
- Set up the app in your Fly.io account
- Ask for app name and region

### 2. Configure Environment Variables

```bash
# Set environment variables
fly secrets set DATABASE_URL="postgresql://..."
fly secrets set REDIS_URL="redis://..."
fly secrets set SECRET_KEY="..."
# ... add all required variables
```

### 3. Deploy

```bash
fly deploy
```

## Configuration

### fly.toml

Example `fly.toml` for backend:

```toml
app = "sketch2bim-backend"
primary_region = "iad"  # Washington, DC

[build]
  dockerfile = "Dockerfile"

[env]
  APP_ENV = "production"
  DEBUG = "false"

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 1
  processes = ["app"]

[[services]]
  protocol = "tcp"
  internal_port = 8000
  processes = ["app"]

  [[services.ports]]
    port = 80
    handlers = ["http"]
    force_https = true

  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]

[processes]
  app = "uvicorn app.main:app --host 0.0.0.0 --port 8000"
```

### Frontend Deployment

For Next.js frontend:

```bash
cd frontend
fly launch
```

Fly.io supports Next.js with automatic optimizations.

## Pricing

Fly.io uses pay-as-you-go pricing:

- **Free tier**: 3 shared-cpu VMs, 3GB persistent storage
- **Paid**: ~$1.94/month per VM (256MB RAM) + storage
- **Recommended**: 1-2 VMs for production (~$5-10/month)

## Scaling

```bash
# Scale up
fly scale count 2

# Scale to specific size
fly scale vm shared-cpu-1x --memory 512
```

## Database

Fly.io offers managed PostgreSQL:

```bash
# Create database
fly postgres create --name sketch2bim-db

# Attach to app
fly postgres attach sketch2bim-db
```

## Redis

Use Upstash Redis (as in current setup) or Fly.io Redis:

```bash
# Create Redis
fly redis create
```

## Monitoring

```bash
# View logs
fly logs

# View metrics
fly dashboard

# SSH into VM
fly ssh console
```

## Advantages over VPS

- **No server management** - Focus on application code
- **Auto-scaling** - Handles traffic spikes automatically
- **Global edge** - Low latency worldwide
- **Built-in SSL** - No certificate management
- **Simple deployment** - `fly deploy` and done

## Disadvantages

- **Less control** - Can't customize server as much
- **Vendor lock-in** - More tied to Fly.io platform
- **Cost** - Can be more expensive at scale vs VPS

## Migration from Render

If migrating from Render:

1. Export environment variables from Render
2. Set them in Fly.io: `fly secrets set KEY=value`
3. Update frontend API URL to Fly.io app URL
4. Deploy: `fly deploy`
5. Update DNS to point to Fly.io

## Resources

- [Fly.io Documentation](https://fly.io/docs/)
- [Fly.io Pricing](https://fly.io/docs/about/pricing/)
- [Fly.io CLI Reference](https://fly.io/docs/flyctl/)

