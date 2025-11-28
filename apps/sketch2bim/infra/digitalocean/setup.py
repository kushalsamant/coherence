#!/usr/bin/env python3
"""
DigitalOcean Droplet provisioning automation
Creates and configures droplets for Sketch-to-BIM deployment
"""
import os
import sys
import time
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

try:
    import digitalocean
except ImportError:
    print("Error: python-digitalocean package not installed")
    print("Install with: pip install python-digitalocean")
    sys.exit(1)

# Load app-specific production environment first (if available)
workspace_root = Path(__file__).resolve().parents[3]
app_env_path = workspace_root / "sketch2bim.env.production"
if app_env_path.exists():
    load_dotenv(app_env_path, override=False)

# Load local .env overrides
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    load_dotenv(env_file, override=True)
else:
    print("Warning: .env file not found. Using environment variables.")

# Required environment variables
DO_API_TOKEN = os.getenv("DIGITALOCEAN_API_TOKEN") or os.getenv("DO_API_TOKEN")
DO_PROJECT_NAME = os.getenv("DO_PROJECT_NAME", "sketch2bim")
DO_DROPLET_SIZE = os.getenv("DO_DROPLET_SIZE", "s-1vcpu-2gb")  # $12/month
DO_REGION = os.getenv("DO_REGION", "nyc1")  # New York
DO_SSH_KEY_ID = os.getenv("DO_SSH_KEY_ID")  # SSH key ID from DigitalOcean

if not DO_API_TOKEN:
    print("Error: DIGITALOCEAN_API_TOKEN or DO_API_TOKEN environment variable is required")
    sys.exit(1)

if not DO_SSH_KEY_ID:
    print("Warning: DO_SSH_KEY_ID not set. Droplet will be created without SSH key.")
    print("You'll need to use root password authentication.")


def get_ssh_keys(manager: digitalocean.Manager) -> list:
    """Get SSH key IDs from DigitalOcean"""
    if DO_SSH_KEY_ID:
        # Use provided SSH key ID
        return [int(DO_SSH_KEY_ID)]
    
    # List available SSH keys
    keys = manager.get_all_sshkeys()
    if not keys:
        print("No SSH keys found in DigitalOcean account")
        print("Create one at: https://cloud.digitalocean.com/account/security")
        return []
    
    print("Available SSH keys:")
    for key in keys:
        print(f"  ID: {key.id}, Name: {key.name}, Fingerprint: {key.fingerprint}")
    
    if keys:
        return [keys[0].id]  # Use first key
    
    return []


def create_droplet(manager: digitalocean.Manager) -> Optional[digitalocean.Droplet]:
    """Create a new droplet"""
    print(f"\nCreating droplet: {DO_PROJECT_NAME}-server")
    print(f"  Size: {DO_DROPLET_SIZE}")
    print(f"  Region: {DO_REGION}")
    print(f"  Image: ubuntu-22-04-x64")
    
    ssh_keys = get_ssh_keys(manager)
    
    try:
        droplet = digitalocean.Droplet(
            token=DO_API_TOKEN,
            name=f"{DO_PROJECT_NAME}-server",
            region=DO_REGION,
            image="ubuntu-22-04-x64",
            size_slug=DO_DROPLET_SIZE,
            ssh_keys=ssh_keys,
            backups=False,
            ipv6=True,
            monitoring=True,
            tags=[DO_PROJECT_NAME]
        )
        droplet.create()
        
        print(f"\n✅ Droplet created: {droplet.id}")
        print("Waiting for droplet to become active...")
        
        # Wait for droplet to be active
        actions = droplet.get_actions()
        for action in actions:
            action.wait()
            if action.status == "completed":
                break
        
        # Refresh droplet to get IP
        droplet.load()
        
        print(f"\n✅ Droplet is active!")
        print(f"  ID: {droplet.id}")
        print(f"  IP: {droplet.ip_address}")
        print(f"  IPv6: {droplet.ip_v6_address}")
        print(f"  Status: {droplet.status}")
        
        return droplet
        
    except Exception as e:
        print(f"❌ Failed to create droplet: {e}")
        return None


def main():
    print("=" * 60)
    print("DigitalOcean Droplet Provisioning")
    print("=" * 60)
    print(f"Project: {DO_PROJECT_NAME}")
    print(f"Region: {DO_REGION}")
    print(f"Size: {DO_DROPLET_SIZE}")
    print("=" * 60)
    
    # Initialize manager
    manager = digitalocean.Manager(token=DO_API_TOKEN)
    
    # Check for existing droplets
    existing_droplets = manager.get_all_droplets(tag_name=DO_PROJECT_NAME)
    if existing_droplets:
        print(f"\n⚠️  Found {len(existing_droplets)} existing droplet(s) with tag '{DO_PROJECT_NAME}':")
        for droplet in existing_droplets:
            print(f"  - {droplet.name} (ID: {droplet.id}, IP: {droplet.ip_address})")
        
        response = input("\nCreate new droplet anyway? (y/N): ")
        if response.lower() != 'y':
            print("Aborted.")
            return
    
    # Create droplet
    droplet = create_droplet(manager)
    
    if droplet:
        print("\n" + "=" * 60)
        print("Next Steps:")
        print("=" * 60)
        print(f"1. SSH into droplet:")
        print(f"   ssh root@{droplet.ip_address}")
        print(f"\n2. Run bootstrap script:")
        print(f"   curl -fsSL https://raw.githubusercontent.com/YOUR_REPO/infra/vps/bootstrap.sh | bash")
        print(f"\n3. Deploy application:")
        print(f"   git clone https://github.com/YOUR_REPO/sketch2bim.git")
        print(f"   cd sketch2bim")
        print(f"   docker compose -f infra/docker-compose.prod.yml up -d")
        print("=" * 60)


if __name__ == "__main__":
    main()

