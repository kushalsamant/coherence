#!/usr/bin/env python3
"""
Hetzner Cloud server provisioning automation
Creates and configures servers for Sketch-to-BIM deployment
"""
import os
import sys
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

try:
    from hcloud import HetznerCloud
    from hcloud.servers import Server
    from hcloud.networks import Network
    from hcloud.firewalls import Firewall
    from hcloud.ssh_keys import SSHKey
except ImportError:
    print("Error: hcloud package not installed")
    print("Install with: pip install hcloud")
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
HETZNER_API_TOKEN = os.getenv("HETZNER_API_TOKEN")
HETZNER_PROJECT_NAME = os.getenv("HETZNER_PROJECT_NAME", "sketch2bim")
HETZNER_SERVER_TYPE = os.getenv("HETZNER_SERVER_TYPE", "cx32")
HETZNER_SSH_KEY_PATH = os.getenv("HETZNER_SSH_KEY_PATH")
HETZNER_LOCATION = os.getenv("HETZNER_LOCATION", "nbg1")  # Nuremberg

if not HETZNER_API_TOKEN:
    print("Error: HETZNER_API_TOKEN environment variable is required")
    sys.exit(1)

if not HETZNER_SSH_KEY_PATH:
    print("Error: HETZNER_SSH_KEY_PATH environment variable is required")
    sys.exit(1)


def get_ssh_key_content(key_path: str) -> str:
    """Read SSH public key from file"""
    key_file = Path(key_path).expanduser()
    if not key_file.exists():
        raise FileNotFoundError(f"SSH key file not found: {key_path}")
    
    with open(key_file, 'r') as f:
        return f.read().strip()


def get_or_create_ssh_key(client: HetznerCloud, key_name: str, public_key: str) -> SSHKey:
    """Get existing SSH key or create new one"""
    # Check if key already exists
    ssh_keys = client.ssh_keys.get_all(name=key_name)
    if ssh_keys:
        print(f"Using existing SSH key: {ssh_keys[0].name} (ID: {ssh_keys[0].id})")
        return ssh_keys[0]
    
    # Create new SSH key
    print(f"Creating new SSH key: {key_name}")
    ssh_key = client.ssh_keys.create(name=key_name, public_key=public_key)
    print(f"Created SSH key: {ssh_key.name} (ID: {ssh_key.id})")
    return ssh_key


def get_or_create_network(client: HetznerCloud, network_name: str) -> Network:
    """Get existing network or create new one"""
    # Check if network already exists
    networks = client.networks.get_all(name=network_name)
    if networks:
        print(f"Using existing network: {networks[0].name} (ID: {networks[0].id})")
        return networks[0]
    
    # Create new private network
    print(f"Creating private network: {network_name}")
    network = client.networks.create(
        name=network_name,
        ip_range="10.0.0.0/24"
    )
    print(f"Created network: {network.name} (ID: {network.id}, IP Range: {network.ip_range})")
    return network


def get_or_create_firewall(client: HetznerCloud, firewall_name: str) -> Firewall:
    """Get existing firewall or create new one"""
    # Check if firewall already exists
    firewalls = client.firewalls.get_all(name=firewall_name)
    if firewalls:
        print(f"Using existing firewall: {firewalls[0].name} (ID: {firewalls[0].id})")
        return firewalls[0]
    
    # Create firewall with rules
    print(f"Creating firewall: {firewall_name}")
    firewall = client.firewalls.create(
        name=firewall_name,
        rules=[
            {
                "direction": "in",
                "protocol": "tcp",
                "port": "22",
                "source_ips": ["0.0.0.0/0", "::/0"],
                "description": "SSH"
            },
            {
                "direction": "in",
                "protocol": "tcp",
                "port": "80",
                "source_ips": ["0.0.0.0/0", "::/0"],
                "description": "HTTP"
            },
            {
                "direction": "in",
                "protocol": "tcp",
                "port": "443",
                "source_ips": ["0.0.0.0/0", "::/0"],
                "description": "HTTPS"
            }
        ]
    )
    print(f"Created firewall: {firewall.name} (ID: {firewall.id})")
    return firewall


def create_server(
    client: HetznerCloud,
    server_name: str,
    server_type: str,
    location: str,
    ssh_key: SSHKey,
    network: Network,
    firewall: Firewall,
    image: str = "ubuntu-22.04"
) -> Server:
    """Create a new server"""
    # Check if server already exists
    servers = client.servers.get_all(name=server_name)
    if servers:
        print(f"Server already exists: {servers[0].name} (ID: {servers[0].id})")
        print(f"IP: {servers[0].public_net.ipv4.ip}")
        return servers[0]
    
    print(f"Creating server: {server_name}")
    print(f"  Type: {server_type}")
    print(f"  Location: {location}")
    print(f"  Image: {image}")
    
    # Create server
    response = client.servers.create(
        name=server_name,
        server_type=server_type,
        image=image,
        location=location,
        ssh_keys=[ssh_key],
        networks=[network],
        firewalls=[firewall],
        labels={
            "project": HETZNER_PROJECT_NAME,
            "managed-by": "sketch2bim-setup"
        }
    )
    
    server = response.server
    print(f"\n✅ Server created successfully!")
    print(f"  Name: {server.name}")
    print(f"  ID: {server.id}")
    print(f"  Public IP: {server.public_net.ipv4.ip}")
    print(f"  Private IP: {server.private_net[0].ip if server.private_net else 'N/A'}")
    print(f"  Status: {server.status}")
    
    return server


def main():
    """Main provisioning function"""
    print("=" * 60)
    print("Hetzner Cloud Server Provisioning")
    print("=" * 60)
    print(f"Project: {HETZNER_PROJECT_NAME}")
    print(f"Server Type: {HETZNER_SERVER_TYPE}")
    print(f"Location: {HETZNER_LOCATION}")
    print("=" * 60)
    
    # Initialize Hetzner Cloud client
    client = HetznerCloud(token=HETZNER_API_TOKEN)
    
    # Read SSH key
    try:
        ssh_key_content = get_ssh_key_content(HETZNER_SSH_KEY_PATH)
        print(f"\n✅ SSH key loaded from: {HETZNER_SSH_KEY_PATH}")
    except Exception as e:
        print(f"❌ Error reading SSH key: {e}")
        sys.exit(1)
    
    # Get or create resources
    ssh_key_name = f"{HETZNER_PROJECT_NAME}-ssh-key"
    ssh_key = get_or_create_ssh_key(client, ssh_key_name, ssh_key_content)
    
    network_name = f"{HETZNER_PROJECT_NAME}-network"
    network = get_or_create_network(client, network_name)
    
    firewall_name = f"{HETZNER_PROJECT_NAME}-firewall"
    firewall = get_or_create_firewall(client, firewall_name)
    
    # Create server
    server_name = f"{HETZNER_PROJECT_NAME}-server"
    server = create_server(
        client=client,
        server_name=server_name,
        server_type=HETZNER_SERVER_TYPE,
        location=HETZNER_LOCATION,
        ssh_key=ssh_key,
        network=network,
        firewall=firewall
    )
    
    # Output connection details
    print("\n" + "=" * 60)
    print("Connection Details")
    print("=" * 60)
    print(f"SSH Command:")
    print(f"  ssh root@{server.public_net.ipv4.ip}")
    print(f"\nServer IP: {server.public_net.ipv4.ip}")
    print(f"Private IP: {server.private_net[0].ip if server.private_net else 'N/A'}")
    print(f"\nNext Steps:")
    print(f"  1. Wait for server to be ready (usually 1-2 minutes)")
    print(f"  2. SSH into server: ssh root@{server.public_net.ipv4.ip}")
    print(f"  3. Run bootstrap script: curl -fsSL https://raw.githubusercontent.com/your-repo/infra/hetzner/bootstrap.sh | bash")
    print(f"     Or manually copy and run: infra/hetzner/bootstrap.sh")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

