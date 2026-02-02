"""
Script to create Razorpay Plans for KVSHVL Platform subscriptions
Run this once to create Plans in your Razorpay account

Usage:
    python scripts/platform/create_razorpay_plans.py
    
This script will:
1. Check for existing plans to avoid duplicates
2. Create missing subscription plans (weekly, monthly, yearly)
3. Output the plan IDs to add to your .env.local file
"""
import os
import sys
from pathlib import Path

try:
    import razorpay
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Error: Missing required package: {e}")
    print("\nPlease install required dependencies:")
    print("  pip install razorpay python-dotenv")
    sys.exit(1)

# Load environment from .env.local
workspace_root = Path(__file__).resolve().parents[2]
env_path = workspace_root / ".env.local"
if env_path.exists():
    load_dotenv(env_path, override=False)
    print(f"Loaded environment from: {env_path}")
else:
    print(f"  Warning: .env.local not found at {env_path}")
    print("Please create .env.local with your Razorpay credentials")
    sys.exit(1)

# Get Razorpay credentials
RAZORPAY_KEY_ID = (
    os.getenv('PLATFORM_RAZORPAY_KEY_ID') or 
    os.getenv('RAZORPAY_KEY_ID')
)
RAZORPAY_KEY_SECRET = (
    os.getenv('PLATFORM_RAZORPAY_KEY_SECRET') or 
    os.getenv('RAZORPAY_KEY_SECRET')
)

if not RAZORPAY_KEY_ID or not RAZORPAY_KEY_SECRET:
    print("Error: Razorpay credentials not found!")
    print("\nPlease set in .env.local:")
    print("  PLATFORM_RAZORPAY_KEY_ID=rzp_test_xxxxx")
    print("  PLATFORM_RAZORPAY_KEY_SECRET=your_secret")
    sys.exit(1)

# Initialize Razorpay client
client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

# Plan definitions
PLANS = [
    {
        "period": "weekly",
        "interval": 1,
        "item": {
            "name": "Weekly Subscription",
            "description": "Weekly platform access",
            "amount": 29900,  # ₹299 in paise
            "currency": "INR"
        },
        "notes": {
            "tier": "weekly",
            "platform": "kvshvl"
        }
    },
    {
        "period": "monthly",
        "interval": 1,
        "item": {
            "name": "Monthly Subscription",
            "description": "Monthly platform access",
            "amount": 299900,  # ₹2,999 in paise
            "currency": "INR"
        },
        "notes": {
            "tier": "monthly",
            "platform": "kvshvl"
        }
    },
    {
        "period": "yearly",
        "interval": 1,
        "item": {
            "name": "Yearly Subscription",
            "description": "Yearly platform access",
            "amount": 2999900,  # ₹29,999 in paise
            "currency": "INR"
        },
        "notes": {
            "tier": "yearly",
            "platform": "kvshvl"
        }
    }
]

def create_plan(plan_data):
    """Create a Razorpay Plan"""
    try:
        print(f"\nCreating plan: {plan_data['item']['name']}")
        print(f"  Period: {plan_data['period']}, Interval: {plan_data['interval']}")
        print(f"  Amount: ₹{plan_data['item']['amount'] / 100:.2f}")
        
        plan = client.plan.create(data=plan_data)
        
        print(f" Created Plan: {plan['id']} - {plan['item']['name']}")
        return plan
    except razorpay.errors.BadRequestError as e:
        print(f" Bad Request Error for {plan_data['item']['name']}:")
        print(f"   Status: {e.status_code if hasattr(e, 'status_code') else 'N/A'}")
        print(f"   Error: {str(e)}")
        if hasattr(e, 'error') and isinstance(e.error, dict):
            print(f"   Error details: {e.error}")
        return None
    except Exception as e:
        print(f" Failed to create plan {plan_data['item']['name']}: {type(e).__name__}")
        print(f"   Error: {str(e)}")
        return None

def check_existing_plans():
    """Check if plans already exist with new names and amounts"""
    try:
        plans = client.plan.all()
        existing = {}
        if plans and 'items' in plans:
            for plan in plans['items']:
                item_name = plan.get('item', {}).get('name', '')
                item_amount = plan.get('item', {}).get('amount', 0)
                notes = plan.get('notes', {})
                
                # Match by exact new name, amount, and platform note
                if notes.get('platform') == 'kvshvl':
                    if item_name == 'Weekly Subscription' and item_amount == 29900:
                        existing['weekly'] = plan['id']
                    elif item_name == 'Monthly Subscription' and item_amount == 299900:
                        existing['monthly'] = plan['id']
                    elif item_name == 'Yearly Subscription' and item_amount == 2999900:
                        existing['yearly'] = plan['id']
        return existing
    except Exception as e:
        print(f"  Could not check existing plans: {e}")
        return {}

def main():
    print("=" * 70)
    print("KVSHVL Platform - Razorpay Subscription Plans Setup")
    print("=" * 70)
    print(f"Using Key ID: {RAZORPAY_KEY_ID[:15]}...")
    print(f"Mode: {'TEST' if 'test' in RAZORPAY_KEY_ID.lower() else 'LIVE'}")
    print("=" * 70)
    
    # Check for existing plans
    print("\nChecking for existing plans...")
    existing_plans = check_existing_plans()
    if existing_plans:
        print(f"Found {len(existing_plans)} existing plan(s):")
        for tier, plan_id in existing_plans.items():
            print(f"  ✓ {tier}: {plan_id}")
        print("\nSkipping creation of existing plans.")
    else:
        print("No existing KVSHVL platform plans found.")
    
    created_plans = existing_plans.copy()
    
    # Create missing plans
    print("\n Creating missing plans...")
    for plan_data in PLANS:
        tier_key = plan_data['notes']['tier']
        if tier_key in existing_plans:
            print(f"\n  Skipping {tier_key} - plan already exists: {existing_plans[tier_key]}")
            continue
            
        plan = create_plan(plan_data)
        if plan:
            created_plans[tier_key] = plan['id']
    
    print("\n" + "=" * 70)
    print(" Plan IDs for .env.local:")
    print("=" * 70)
    
    if not created_plans:
        print(" No plans created or found. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Verify your API keys are correct in .env.local")
        print("2. Check if your Razorpay account has subscription features enabled")
        print("3. Try creating plans manually in Razorpay Dashboard")
        return
    
    print("\n# Add these to your .env.local file:")
    for tier in ['weekly', 'monthly', 'yearly']:
        if tier in created_plans:
            print(f"PLATFORM_RAZORPAY_PLAN_{tier.upper()}={created_plans[tier]}")
        else:
            print(f"PLATFORM_RAZORPAY_PLAN_{tier.upper()}=  # MISSING - create manually")
    
    # Also output RAZORPAY_ prefixed versions for compatibility
    print("\n# Or use these (without PLATFORM_ prefix):")
    for tier in ['weekly', 'monthly', 'yearly']:
        if tier in created_plans:
            print(f"RAZORPAY_PLAN_{tier.upper()}={created_plans[tier]}")
    
    if len(created_plans) == 3:
        print("\n" + "=" * 70)
        print(" SUCCESS! All plans created successfully!")
        print("=" * 70)
        print("\n📝 Next steps:")
        print("1. Copy the plan IDs above to your .env.local file")
        print("2. Restart your development server (npm run dev)")
        print("3. Try the checkout again")
        print("\n Note: These are test plans. Create separate plans for production")
        print("   using your live Razorpay credentials.")
    else:
        print(f"\n  Only {len(created_plans)}/3 plans created. Please create the missing ones manually.")

if __name__ == "__main__":
    main()

