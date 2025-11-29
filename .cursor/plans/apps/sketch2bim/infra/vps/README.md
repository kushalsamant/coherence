# Provider-Agnostic VPS Setup

This directory contains scripts and configurations that work across multiple VPS providers (Hetzner, DigitalOcean, Vultr, Linode, etc.).

## Overview

These scripts provide a standardized way to set up and deploy Sketch-to-BIM on any VPS provider, regardless of the specific provider's API or tools.

## Bootstrap Script

The `bootstrap.sh` script can be used on any Ubuntu/Debian-based VPS to set up the server with:
- Docker and Docker Compose
- Security hardening (UFW, fail2ban)
- System updates
- Application directories

## Usage

### 1. Provision a VPS

Choose any VPS provider:
- **Hetzner** - See `../hetzner/` for Hetzner-specific automation
- **DigitalOcean** - See `../digitalocean/` for DigitalOcean-specific automation
- **Vultr** - Manual provisioning via web interface
- **Linode** - Manual provisioning via web interface
- **Any other provider** - Manual provisioning

### 2. Bootstrap the Server

Once you have SSH access to your VPS:

```bash
# Download and run bootstrap script
curl -fsSL https://raw.githubusercontent.com/YOUR_REPO/infra/vps/bootstrap.sh | bash

# Or manually
wget https://raw.githubusercontent.com/YOUR_REPO/infra/vps/bootstrap.sh
chmod +x bootstrap.sh
sudo ./bootstrap.sh
```

### 3. Deploy Application

After bootstrapping, deploy using Docker Compose:

```bash
# Clone repository
git clone https://github.com/YOUR_REPO/sketch2bim.git
cd sketch2bim

# Environment Variables
# Production environment variables are in sketch2bim.env.production at the repository root
# For local development overrides, create infra/vps/.env (gitignored)
# The setup scripts automatically load sketch2bim.env.production first, then local .env overrides

# Deploy
docker compose -f infra/docker-compose.prod.yml up -d
```

## What Gets Installed

- **Docker** - Container runtime
- **Docker Compose** - Multi-container orchestration
- **UFW Firewall** - Network security (SSH, HTTP, HTTPS)
- **fail2ban** - Brute-force protection
- **Unattended-upgrades** - Automatic security updates
- **Base tools** - curl, wget, git, vim, htop

## Security Features

- SSH key-only authentication (password auth disabled)
- Firewall rules (only SSH, HTTP, HTTPS open)
- fail2ban for brute-force protection
- Automatic security updates
- Non-root user setup (optional)

## Provider-Specific Guides

- **Hetzner**: See `../hetzner/README.md`
- **DigitalOcean**: See `../digitalocean/README.md`
- **Vultr**: Manual setup (use bootstrap.sh)
- **Linode**: Manual setup (use bootstrap.sh)

## Cost Comparison

| Provider | Type | Cost/Month | Notes |
|----------|------|------------|-------|
| Hetzner | VPS | €9-12 | EU-focused, cost-effective |
| DigitalOcean | VPS | $6-12 | Good docs, US/EU presence |
| Vultr | VPS | $2.50-6 | Budget-friendly, global |
| Linode | VPS | $5-12 | Strong performance |
| Contabo | VPS | €4-9 | Very affordable, EU-based |

## Next Steps

After bootstrapping:
1. Set up SSL certificates (Let's Encrypt)
2. Configure domain DNS
3. Set up monitoring (optional)
4. Configure backups (optional)

