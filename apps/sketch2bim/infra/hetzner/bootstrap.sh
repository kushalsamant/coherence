#!/bin/bash
#
# Server bootstrap script for Sketch-to-BIM
# Configures Ubuntu 22.04 server with Docker, security, and base tools
# Safe to run multiple times (idempotent)
#

set -e  # Exit on error

echo "=========================================="
echo "Sketch-to-BIM Server Bootstrap"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Please run as root${NC}"
    exit 1
fi

# Update system packages
echo -e "${GREEN}[1/10] Updating system packages...${NC}"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get upgrade -y -qq

# Install base packages
echo -e "${GREEN}[2/10] Installing base packages...${NC}"
apt-get install -y -qq \
    curl \
    wget \
    git \
    vim \
    htop \
    ufw \
    fail2ban \
    unattended-upgrades \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release

# Install Docker
if ! command -v docker &> /dev/null; then
    echo -e "${GREEN}[3/10] Installing Docker...${NC}"
    # Add Docker's official GPG key
    install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    chmod a+r /etc/apt/keyrings/docker.gpg
    
    # Set up Docker repository
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    apt-get update -qq
    apt-get install -y -qq docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
else
    echo -e "${YELLOW}[3/10] Docker already installed, skipping...${NC}"
fi

# Verify Docker installation
docker --version
docker compose version

# Configure UFW firewall
echo -e "${GREEN}[4/10] Configuring UFW firewall...${NC}"
# Allow SSH (important - do this first!)
ufw allow 22/tcp comment 'SSH'
# Allow HTTP/HTTPS
ufw allow 80/tcp comment 'HTTP'
ufw allow 443/tcp comment 'HTTPS'
# Enable firewall (non-interactive)
ufw --force enable
ufw status

# Harden SSH configuration
echo -e "${GREEN}[5/10] Hardening SSH configuration...${NC}"
SSH_CONFIG="/etc/ssh/sshd_config"

# Backup original config
if [ ! -f "${SSH_CONFIG}.backup" ]; then
    cp "${SSH_CONFIG}" "${SSH_CONFIG}.backup"
fi

# Disable password authentication (key-only)
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' "${SSH_CONFIG}"
sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/' "${SSH_CONFIG}"

# Disable root login via password (key-only)
sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin prohibit-password/' "${SSH_CONFIG}"
sed -i 's/PermitRootLogin yes/PermitRootLogin prohibit-password/' "${SSH_CONFIG}"

# Restart SSH service
systemctl restart sshd
echo -e "${GREEN}SSH hardened (password auth disabled, key-only)${NC}"

# Configure fail2ban
echo -e "${GREEN}[6/10] Configuring fail2ban...${NC}"
systemctl enable fail2ban
systemctl start fail2ban
fail2ban-client status

# Configure unattended-upgrades
echo -e "${GREEN}[7/10] Configuring automatic security updates...${NC}"
cat > /etc/apt/apt.conf.d/50unattended-upgrades << EOF
Unattended-Upgrade::Allowed-Origins {
    "\${distro_id}:\${distro_codename}-security";
    "\${distro_id}ESMApps:\${distro_codename}-apps-security";
    "\${distro_id}ESM:\${distro_codename}-infra-security";
};
Unattended-Upgrade::AutoFixInterruptedDpkg "true";
Unattended-Upgrade::MinimalSteps "true";
Unattended-Upgrade::Remove-Unused-Kernel-Packages "true";
Unattended-Upgrade::Remove-Unused-Dependencies "true";
Unattended-Upgrade::Automatic-Reboot "false";
EOF

cat > /etc/apt/apt.conf.d/20auto-upgrades << EOF
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Download-Upgradeable-Packages "1";
APT::Periodic::AutocleanInterval "7";
APT::Periodic::Unattended-Upgrade "1";
EOF

systemctl enable unattended-upgrades
systemctl start unattended-upgrades

# Create non-root user with sudo (optional - comment out if not needed)
echo -e "${GREEN}[8/10] Creating non-root user (sketch2bim)...${NC}"
if ! id "sketch2bim" &>/dev/null; then
    useradd -m -s /bin/bash sketch2bim
    usermod -aG sudo sketch2bim
    usermod -aG docker sketch2bim
    echo -e "${YELLOW}User 'sketch2bim' created. Set password with: passwd sketch2bim${NC}"
    echo -e "${YELLOW}Or copy SSH key: mkdir -p /home/sketch2bim/.ssh && cp ~/.ssh/authorized_keys /home/sketch2bim/.ssh/ && chown -R sketch2bim:sketch2bim /home/sketch2bim/.ssh${NC}"
else
    echo -e "${YELLOW}User 'sketch2bim' already exists${NC}"
fi

# Set up Docker for non-root user
if id "sketch2bim" &>/dev/null; then
    usermod -aG docker sketch2bim
fi

# Create application directory
echo -e "${GREEN}[9/10] Creating application directories...${NC}"
mkdir -p /opt/sketch2bim
mkdir -p /opt/sketch2bim/data
mkdir -p /opt/sketch2bim/logs
chmod 755 /opt/sketch2bim

# Install useful tools
echo -e "${GREEN}[10/10] Installing additional tools...${NC}"
apt-get install -y -qq \
    jq \
    net-tools \
    tcpdump \
    iotop \
    ncdu

# Final system information
echo ""
echo "=========================================="
echo "Bootstrap Complete!"
echo "=========================================="
echo -e "${GREEN}System Information:${NC}"
echo "  OS: $(lsb_release -ds)"
echo "  Kernel: $(uname -r)"
echo "  Docker: $(docker --version | cut -d' ' -f3 | tr -d ',')"
echo "  Docker Compose: $(docker compose version --short)"
echo ""
echo -e "${GREEN}Security Status:${NC}"
echo "  UFW: $(ufw status | head -n1)"
echo "  Fail2ban: $(systemctl is-active fail2ban)"
echo "  Unattended-upgrades: $(systemctl is-active unattended-upgrades)"
echo ""
echo -e "${GREEN}Next Steps:${NC}"
echo "  1. Deploy application using Docker Compose"
echo "  2. Set up SSL certificates (Let's Encrypt with Certbot)"
echo "  3. Configure reverse proxy (nginx/traefik)"
echo "  4. Set up monitoring and logging"
echo ""
echo "=========================================="

