# DigitalOcean Deployment

Deployment guide for Sketch-to-BIM on DigitalOcean Droplets.

## Overview

DigitalOcean is a popular VPS provider with excellent documentation, good US/EU presence, and competitive pricing ($6-12/month for basic droplets).

## Quick Start

### 1. Create Droplet

1. Go to [DigitalOcean Dashboard](https://cloud.digitalocean.com/droplets/new)
2. Choose:
   - **Image**: Ubuntu 22.04 LTS
   - **Plan**: Basic ($6/month - 1GB RAM) or Regular ($12/month - 2GB RAM)
   - **Datacenter**: Choose closest to your users
   - **Authentication**: SSH keys (recommended) or root password
3. Click "Create Droplet"

### 2. Bootstrap Server

Once droplet is created, SSH into it:

```bash
ssh root@YOUR_DROPLET_IP
```

Then run the bootstrap script:

```bash
# Download and run
curl -fsSL https://raw.githubusercontent.com/YOUR_REPO/infra/vps/bootstrap.sh | bash

# Or manually
wget https://raw.githubusercontent.com/YOUR_REPO/infra/vps/bootstrap.sh
chmod +x bootstrap.sh
sudo ./bootstrap.sh
```

### 3. Deploy Application

```bash
# Clone repository
git clone https://github.com/YOUR_REPO/sketch2bim.git
cd sketch2bim

# Environment Variables
# Production environment variables are in sketch2bim.env.production at the repository root
# For local development overrides, create infra/digitalocean/.env (gitignored)
# The setup scripts automatically load sketch2bim.env.production first, then local .env overrides

# Deploy
docker compose -f infra/docker-compose.prod.yml up -d
```

## Automation with DigitalOcean API

### Prerequisites

```bash
pip install python-digitalocean
```

### Create Droplet via API

```python
import digitalocean

manager = digitalocean.Manager(token="YOUR_DIGITALOCEAN_TOKEN")

# Create droplet
droplet = digitalocean.Droplet(
    token="YOUR_DIGITALOCEAN_TOKEN",
    name="sketch2bim-server",
    region="nyc1",  # New York
    image="ubuntu-22-04-x64",
    size_slug="s-1vcpu-1gb",  # $6/month
    ssh_keys=[YOUR_SSH_KEY_ID],
    backups=False
)
droplet.create()
```

## Pricing

| Plan | vCPU | RAM | SSD | Price/Month |
|------|------|-----|-----|-------------|
| Basic $6 | 1 | 1GB | 25GB | $6 |
| Basic $12 | 1 | 2GB | 50GB | $12 |
| Regular $18 | 2 | 2GB | 50GB | $18 |
| Regular $24 | 2 | 4GB | 80GB | $24 |

**Recommended**: Basic $12 (1 vCPU, 2GB RAM) for production.

## Features

- **Excellent Documentation** - Comprehensive guides and tutorials
- **Global Presence** - Datacenters in US, EU, Asia
- **Simple API** - Easy automation
- **Managed Databases** - Optional PostgreSQL/Redis hosting
- **Load Balancers** - Built-in load balancing
- **Spaces (S3-compatible)** - Object storage option

## Advantages over Hetzner

- Better US presence (more datacenter options)
- Excellent documentation and tutorials
- More managed services (databases, load balancers)
- Better for beginners

## Disadvantages

- Slightly more expensive than Hetzner
- Less EU-focused (if that's your target)

## Next Steps

1. Set up domain DNS (point to droplet IP)
2. Configure SSL (Let's Encrypt with Certbot)
3. Set up firewall rules
4. Configure backups (DigitalOcean snapshots)
5. Set up monitoring (optional)

## Resources

- [DigitalOcean Documentation](https://docs.digitalocean.com/)
- [DigitalOcean API Reference](https://docs.digitalocean.com/reference/api/)
- [Python DigitalOcean Library](https://github.com/koalalorenzo/python-digitalocean)

