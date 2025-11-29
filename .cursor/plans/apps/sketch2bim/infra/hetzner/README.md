# Hetzner Cloud Infrastructure Setup

Automated server provisioning and configuration for Sketch-to-BIM deployment on Hetzner Cloud.

## Overview

This directory contains scripts to automate:
- Server provisioning via Hetzner Cloud API
- Base server configuration (Docker, security, firewall)
- Network and firewall setup

## Prerequisites

1. **Hetzner Cloud Account**
   - Sign up at https://www.hetzner.com/cloud
   - Create a project

2. **API Token**
   - Go to: https://console.hetzner.cloud/projects/YOUR_PROJECT/security/tokens
   - Create a new token with read/write permissions
   - Save the token securely

3. **SSH Key Pair**
   - Generate if you don't have one:
     ```bash
     ssh-keygen -t ed25519 -C "your_email@example.com"
     ```
   - Public key will be at: `~/.ssh/id_ed25519.pub` (or `id_rsa.pub`)

4. **Python Dependencies**
   ```bash
   pip install hcloud python-dotenv
   ```
   Or install from requirements:
   ```bash
   pip install -r infra/hetzner/requirements.txt
   ```

## Quick Start

### 1. Configure Environment Variables

```bash
cd infra/hetzner
cp .env.example .env
# Edit .env with your values
```

Required variables:
- `HETZNER_API_TOKEN` - Your Hetzner Cloud API token
- `HETZNER_PROJECT_NAME` - Project name (used for resource naming)
- `HETZNER_SSH_KEY_PATH` - Path to your SSH public key

Optional variables:
- `HETZNER_SERVER_TYPE` - Server type (default: `cx32`)
- `HETZNER_LOCATION` - Datacenter location (default: `nbg1`)

### 2. Run Setup Script

```bash
python setup.py
```

The script will:
- Create or reuse SSH key in Hetzner Cloud
- Create private network (10.0.0.0/24)
- Create firewall with rules (SSH, HTTP, HTTPS)
- Provision Ubuntu 22.04 server
- Output connection details

### 3. Bootstrap Server

After server is created, SSH into it and run the bootstrap script:

```bash
# SSH into server (use IP from setup.py output)
ssh root@YOUR_SERVER_IP

# Run bootstrap script
curl -fsSL https://raw.githubusercontent.com/YOUR_REPO/infra/hetzner/bootstrap.sh | bash
```

Or manually:
```bash
# Copy bootstrap.sh to server
scp infra/hetzner/bootstrap.sh root@YOUR_SERVER_IP:/tmp/

# SSH and run
ssh root@YOUR_SERVER_IP
bash /tmp/bootstrap.sh
```

## Server Types

Common server types and pricing (as of 2024):

| Type | vCPU | RAM | SSD | Price/month |
|------|------|-----|-----|-------------|
| cx11 | 1    | 2GB | 20GB | ~€3.29 |
| cx21 | 2    | 4GB | 40GB | ~€4.15 |
| cx31 | 2    | 8GB | 80GB | ~€7.29 |
| cx32 | 4    | 8GB | 160GB | ~€9.29 |
| cx33 | 4    | 8GB | 80GB | ~€5.49 |
| cx41 | 4    | 16GB | 160GB | ~€12.99 |

**Recommended:** `cx32` for production (4 vCPU, 8GB RAM, 160GB SSD)

## What Gets Created

### Resources Created

1. **SSH Key** (`{project}-ssh-key`)
   - Uploaded to Hetzner Cloud
   - Used for server access

2. **Private Network** (`{project}-network`)
   - IP Range: 10.0.0.0/24
   - For internal communication

3. **Firewall** (`{project}-firewall`)
   - Rules: SSH (22), HTTP (80), HTTPS (443)
   - Applied to server

4. **Server** (`{project}-server`)
   - Ubuntu 22.04
   - Configured server type
   - Connected to network and firewall
   - SSH key installed

### Bootstrap Script Configures

- System package updates
- Docker and Docker Compose
- UFW firewall (SSH, HTTP, HTTPS)
- SSH hardening (key-only, no password)
- fail2ban (brute-force protection)
- Unattended-upgrades (automatic security updates)
- Non-root user (optional)
- Application directories

## Cost Comparison

### Hetzner vs Render

**Hetzner (cx32):**
- ~€9.29/month (~$10.50/month)
- Full server control
- 4 vCPU, 8GB RAM, 160GB SSD
- 20TB traffic included

**Render (4GB RAM):**
- ~$45/month
- Managed service
- Less control
- Auto-scaling included

**Savings:** ~$34-35/month (~$400-420/year)

### Additional Costs

- Domain name: ~$10-15/year
- DNS: Free (Hetzner DNS or Cloudflare)
- SSL: Free (Let's Encrypt)
- Backups: ~€0.04/GB/month (optional)

## Deployment Options

After bootstrap, you can deploy using:

### Option 1: Docker Compose

```bash
# On server
cd /opt/sketch2bim
# Copy docker-compose.yml
docker compose up -d
```

### Option 2: Coolify/CapRover

- Install Coolify or CapRover
- Deploy via web interface
- Automatic SSL and reverse proxy

### Option 3: Manual Setup

- Install nginx/traefik for reverse proxy
- Set up SSL with Certbot
- Deploy application manually

## Security Considerations

### Firewall

- UFW configured with SSH, HTTP, HTTPS only
- Hetzner Cloud firewall provides additional layer
- Consider restricting SSH to specific IPs in production

### SSH Hardening

- Password authentication disabled
- Key-only access
- Root login restricted (key-only)

### Updates

- Automatic security updates enabled
- fail2ban protects against brute-force attacks
- Regular system updates recommended

## Troubleshooting

### Setup Script Issues

**"API token invalid"**
- Verify token is correct
- Check token has read/write permissions
- Ensure token hasn't expired

**"SSH key file not found"**
- Verify `HETZNER_SSH_KEY_PATH` is correct
- Use absolute path or `~/.ssh/id_rsa.pub`
- Check file permissions

**"Server creation failed"**
- Check server type is available in location
- Verify account has sufficient quota
- Check Hetzner Cloud status page

### Bootstrap Script Issues

**"Permission denied"**
- Run as root: `sudo bash bootstrap.sh`
- Or: `sudo -i` then run script

**"Docker installation failed"**
- Check internet connectivity
- Verify Ubuntu version (22.04 recommended)
- Check for conflicting Docker installations

**"UFW blocks SSH"**
- Ensure SSH rule is added before enabling UFW
- If locked out, use Hetzner Cloud console to access server

### Server Access Issues

**"Connection refused"**
- Check server is running in Hetzner dashboard
- Verify firewall allows SSH (port 22)
- Check server IP is correct

**"Permission denied (publickey)"**
- Verify SSH key is correct
- Check key is added to Hetzner Cloud
- Try: `ssh -v root@SERVER_IP` for debug info

## Maintenance

### Regular Tasks

1. **System Updates**
   ```bash
   apt update && apt upgrade -y
   ```

2. **Docker Updates**
   ```bash
   apt update && apt upgrade docker-ce docker-ce-cli containerd.io
   ```

3. **Check Logs**
   ```bash
   journalctl -u docker
   docker logs CONTAINER_NAME
   ```

4. **Monitor Resources**
   ```bash
   htop
   df -h
   docker stats
   ```

### Backup Strategy

1. **Application Data**
   - Backup `/opt/sketch2bim/data`
   - Use Hetzner Cloud snapshots or external backup

2. **Database**
   - Regular database dumps
   - Store off-server

3. **Configuration**
   - Version control for config files
   - Document custom changes

## Next Steps

After server is set up:

1. **Deploy Application**
   - Copy application files
   - Set up environment variables
   - Start services

2. **Configure SSL**
   - Install Certbot
   - Set up Let's Encrypt certificates
   - Configure auto-renewal

3. **Set Up Monitoring**
   - Install monitoring tools (Prometheus, Grafana)
   - Set up log aggregation
   - Configure alerts

4. **Set Up Backups**
   - Configure automated backups
   - Test restore procedures
   - Document backup schedule

## Support

For issues:
- Check Hetzner Cloud documentation: https://docs.hetzner.com/
- Review server logs: `journalctl -xe`
- Check application logs: `docker logs CONTAINER_NAME`
- Review troubleshooting section above

## References

- Hetzner Cloud API: https://docs.hetzner.com/cloud/
- hcloud Python SDK: https://github.com/hetznercloud/hcloud-python
- Docker Documentation: https://docs.docker.com/
- Ubuntu Server Guide: https://ubuntu.com/server/docs

