#!/usr/bin/env python3
"""
Render Environment Variables Preparation Script

This script reads your .env.production.backend file and generates:
1. A checklist for manual entry in Render dashboard
2. CLI commands for Render CLI
3. A JSON payload for Render API

Usage:
    python scripts/prepare_render_env.py
"""

import os
import json
from pathlib import Path


def read_env_file(file_path):
    """Read .env file and return dictionary of variables"""
    env_vars = {}
    
    if not os.path.exists(file_path):
        print(f"❌ Error: {file_path} not found!")
        print("Please ensure .env.production.backend exists in the project root.")
        print("If you haven't split your .env files yet, run: node scripts/split-env-files.js .env.production")
        return None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            # Parse KEY=VALUE
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # Remove quotes if present
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                
                env_vars[key] = value
    
    return env_vars


def filter_render_vars(env_vars):
    """Filter only variables needed for Render (backend)"""
    render_vars = {}
    
    # Required variables for Render
    required_keys = [
        # Platform configuration
        'PLATFORM_APP_NAME',
        'PLATFORM_ENVIRONMENT',
        'PLATFORM_DEBUG',
        'PLATFORM_CORS_ORIGINS',
        
        # Authentication
        'PLATFORM_AUTH_SECRET',
        'PLATFORM_NEXTAUTH_SECRET',
        'PLATFORM_ADMIN_EMAILS',
        
        # Redis
        'PLATFORM_UPSTASH_REDIS_REST_URL',
        'PLATFORM_UPSTASH_REDIS_REST_TOKEN',
        
        # Razorpay
        'PLATFORM_RAZORPAY_KEY_ID',
        'PLATFORM_RAZORPAY_KEY_SECRET',
        'PLATFORM_RAZORPAY_WEBHOOK_SECRET',
        'PLATFORM_RAZORPAY_PLAN_WEEKLY',
        'PLATFORM_RAZORPAY_PLAN_MONTHLY',
        'PLATFORM_RAZORPAY_PLAN_YEARLY',
        
        # Databases (CRITICAL)
        'SKETCH2BIM_DATABASE_URL',
        
        # AI Services
        'SKETCH2BIM_GROQ_API_KEY',
        
        # Supabase Storage (replaces BunnyCDN)
        'NEXT_PUBLIC_SUPABASE_URL',
        'NEXT_PUBLIC_SUPABASE_ANON_KEY',
        'SUPABASE_SERVICE_ROLE_KEY',
    ]
    
    for key in required_keys:
        if key in env_vars:
            render_vars[key] = env_vars[key]
        else:
            print(f"⚠️  Warning: {key} not found in environment file")
            render_vars[key] = "[NOT SET]"
    
    return render_vars


def mask_sensitive_value(value, show_chars=4):
    """Mask sensitive values for display"""
    if value == "[NOT SET]" or len(value) <= show_chars * 2:
        return value
    return f"{value[:show_chars]}...{value[-show_chars:]}"


def generate_checklist(render_vars):
    """Generate a markdown checklist for manual entry"""
    print("\n" + "="*80)
    print("📋 RENDER DASHBOARD CHECKLIST")
    print("="*80)
    print("\nCopy these values to Render Dashboard -> Environment Tab:\n")
    
    categories = {
        "🔧 Platform Configuration": [
            'PLATFORM_APP_NAME',
            'PLATFORM_ENVIRONMENT',
            'PLATFORM_DEBUG',
            'PLATFORM_CORS_ORIGINS',
        ],
        "🔐 Authentication & Security (Supabase)": [
            'NEXT_PUBLIC_SUPABASE_URL',
            'NEXT_PUBLIC_SUPABASE_ANON_KEY',
            'SUPABASE_SERVICE_ROLE_KEY',
            'PLATFORM_ADMIN_EMAILS',
        ],
        "🔐 Legacy Authentication (deprecated)": [
            'PLATFORM_AUTH_SECRET',
            'PLATFORM_NEXTAUTH_SECRET',
        ],
        "🗄️ Databases (CRITICAL - Fix deployment error)": [
            'SKETCH2BIM_DATABASE_URL',
        ],
        "📦 Redis": [
            'PLATFORM_UPSTASH_REDIS_REST_URL',
            'PLATFORM_UPSTASH_REDIS_REST_TOKEN',
        ],
        "💳 Razorpay": [
            'PLATFORM_RAZORPAY_KEY_ID',
            'PLATFORM_RAZORPAY_KEY_SECRET',
            'PLATFORM_RAZORPAY_WEBHOOK_SECRET',
            'PLATFORM_RAZORPAY_PLAN_WEEKLY',
            'PLATFORM_RAZORPAY_PLAN_MONTHLY',
            'PLATFORM_RAZORPAY_PLAN_YEARLY',
        ],
        "🤖 AI Services": [
            'SKETCH2BIM_GROQ_API_KEY',
        ],
        "☁️ Storage (Supabase - replaces BunnyCDN)": [
            'NEXT_PUBLIC_SUPABASE_URL',
            'NEXT_PUBLIC_SUPABASE_ANON_KEY',
            'SUPABASE_SERVICE_ROLE_KEY',
        ],
    }
    
    for category, keys in categories.items():
        print(f"\n{category}")
        print("-" * 80)
        for key in keys:
            value = render_vars.get(key, "[NOT SET]")
            masked = mask_sensitive_value(value)
            status = "✅" if value != "[NOT SET]" else "❌"
            print(f"  {status} {key}")
            print(f"     Value: {masked}")


def generate_cli_commands(render_vars, service_name="platform-api"):
    """Generate Render CLI commands"""
    print("\n" + "="*80)
    print("💻 RENDER CLI COMMANDS")
    print("="*80)
    print(f"\n# Set these environment variables for service: {service_name}")
    print("# Run these commands after: render login\n")
    
    for key, value in render_vars.items():
        if value != "[NOT SET]":
            # Escape special characters in bash
            escaped_value = value.replace('"', '\\"')
            print(f'render env set {key}="{escaped_value}" --service {service_name}')


def generate_api_payload(render_vars):
    """Generate JSON payload for Render API"""
    print("\n" + "="*80)
    print("🔗 RENDER API PAYLOAD")
    print("="*80)
    print("\nUse this JSON payload with Render API:\n")
    
    # Filter out unset values
    api_vars = {k: v for k, v in render_vars.items() if v != "[NOT SET]"}
    
    print("```json")
    print(json.dumps(api_vars, indent=2))
    print("```")
    
    print("\nAPI Request Example:")
    print("```bash")
    print("curl -X PUT 'https://api.render.com/v1/services/[SERVICE_ID]/env-vars' \\")
    print("  -H 'Authorization: Bearer [YOUR_API_KEY]' \\")
    print("  -H 'Content-Type: application/json' \\")
    print("  -d '@payload.json'")
    print("```")


def generate_export_script(render_vars):
    """Generate shell script to export variables locally"""
    print("\n" + "="*80)
    print("📝 LOCAL TESTING SCRIPT")
    print("="*80)
    print("\nSave this as 'set_env.sh' for local testing:\n")
    
    print("```bash")
    print("#!/bin/bash")
    print("# Export Render environment variables for local testing\n")
    
    for key, value in render_vars.items():
        if value != "[NOT SET]":
            escaped_value = value.replace('"', '\\"')
            print(f'export {key}="{escaped_value}"')
    
    print("\necho '✅ Environment variables set!'")
    print("```")


def main():
    print("🚀 Render Environment Variables Preparation Tool")
    print("="*80)
    
    # Locate .env.production.backend (split file structure)
    project_root = Path(__file__).parent.parent
    env_file = project_root / '.env.production.backend'
    
    # Fallback to .env.production if split file doesn't exist
    if not env_file.exists():
        env_file = project_root / '.env.production'
        if env_file.exists():
            print(f"\n⚠️  Warning: Using .env.production (not split yet)")
            print("   Consider running: node scripts/split-env-files.js .env.production")
    
    print(f"\n📁 Looking for: {env_file}")
    
    # Read environment file
    env_vars = read_env_file(env_file)
    if not env_vars:
        return
    
    print(f"✅ Found {len(env_vars)} variables in {env_file.name}")
    
    # Filter for Render-specific variables
    render_vars = filter_render_vars(env_vars)
    print(f"✅ Filtered {len(render_vars)} variables needed for Render")
    
    # Generate outputs
    generate_checklist(render_vars)
    generate_cli_commands(render_vars)
    generate_api_payload(render_vars)
    generate_export_script(render_vars)
    
    # Summary
    print("\n" + "="*80)
    print("📊 SUMMARY")
    print("="*80)
    
    total = len(render_vars)
    set_count = sum(1 for v in render_vars.values() if v != "[NOT SET]")
    missing = total - set_count
    
    print(f"\nTotal variables required: {total}")
    print(f"✅ Set: {set_count}")
    print(f"❌ Missing: {missing}")
    
    if missing > 0:
        print("\n⚠️  Warning: Some variables are missing in the environment file")
        print("Please add them before deploying to Render.")
    else:
        print("\n✅ All required variables are set!")
        print("You can now proceed with Render configuration.")
    
    print("\n" + "="*80)
    print("NEXT STEPS:")
    print("="*80)
    print("1. Go to https://dashboard.render.com")
    print("2. Navigate to your 'platform-api' service")
    print("3. Go to Environment tab")
    print("4. Copy values from the checklist above")
    print("5. Save and wait for automatic redeployment")
    print("6. Test: curl https://kushalsamant-github-io.onrender.com/health")
    print("="*80 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
