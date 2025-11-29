"""
Script to create Razorpay Plans for subscription payments
Run this once to create Plans in your Razorpay account

Usage:
    # Option 1: Run from project root (if backend dependencies are installed globally)
    python scripts/create_razorpay_plans.py
    
    # Option 2: Run from backend directory (recommended)
    cd backend
    python ../scripts/create_razorpay_plans.py
    
    # Option 3: Run with virtual environment activated
    # source venv/bin/activate  # or `venv\Scripts\activate` on Windows
    python scripts/create_razorpay_plans.py
"""
import os
import sys
from pathlib import Path

# Add backend directory to path to import backend dependencies
backend_dir = Path(__file__).parent.parent / "backend"
if backend_dir.exists():
    sys.path.insert(0, str(backend_dir))

try:
    import razorpay
    from dotenv import load_dotenv
except ImportError as e:
    print(f"Error: Missing required package: {e}")
    print("\nPlease install backend dependencies:")
    print("  cd backend")
    print("  pip install -r requirements.txt")
    print("\nOr run this script from the backend directory:")
    print("  cd backend")
    print("  python ../scripts/create_razorpay_plans.py")
    sys.exit(1)

# Load app-specific production env
workspace_root = Path(__file__).resolve().parents[2]
app_env_path = workspace_root / "sketch2bim.env.production"
if app_env_path.exists():
    load_dotenv(app_env_path, override=False)
    print(f"Loaded environment from: {app_env_path}")
else:
    print(f"⚠️  Warning: sketch2bim.env.production not found at {app_env_path}")

RAZORPAY_KEY_ID = os.getenv('SKETCH2BIM_RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = os.getenv('SKETCH2BIM_RAZORPAY_KEY_SECRET')

if not RAZORPAY_KEY_ID or not RAZORPAY_KEY_SECRET:
    print("Error: SKETCH2BIM_RAZORPAY_KEY_ID and SKETCH2BIM_RAZORPAY_KEY_SECRET must be set")
    sys.exit(1)

# Initialize Razorpay client
client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

# Plan definitions
# Razorpay Plan structure: https://razorpay.com/docs/api/subscriptions/#create-a-plan
PLANS = [
    {
        "period": "weekly",
        "interval": 1,
        "item": {
            "name": "Week Pass Subscription",
            "description": "7-day access to Sketch-to-BIM",
            "amount": 129900,  # ₹1,299 in paise
            "currency": "INR"
        },
        "notes": {
            "tier": "week"
        }
    },
    {
        "period": "monthly",
        "interval": 1,
        "item": {
            "name": "Month Subscription",
            "description": "30-day access to Sketch-to-BIM",
            "amount": 349900,  # ₹3,499 in paise
            "currency": "INR"
        },
        "notes": {
            "tier": "month"
        }
    },
    {
        "period": "yearly",
        "interval": 1,
        "item": {
            "name": "Year Subscription",
            "description": "365-day access to Sketch-to-BIM",
            "amount": 2999900,  # ₹29,999 in paise
            "currency": "INR"
        },
        "notes": {
            "tier": "year"
        }
    }
]

def create_plan(plan_data):
    """Create a Razorpay Plan"""
    try:
        print(f"\nCreating plan: {plan_data['item']['name']}")
        print(f"  Period: {plan_data['period']}, Interval: {plan_data['interval']}")
        print(f"  Amount: ₹{plan_data['item']['amount'] / 100}")
        
        # Try creating the plan
        plan = client.plan.create(data=plan_data)
        
        print(f"✅ Created Plan: {plan['id']} - {plan['item']['name']}")
        return plan
    except razorpay.errors.BadRequestError as e:
        print(f"❌ Bad Request Error for {plan_data['item']['name']}:")
        print(f"   Status: {e.status_code if hasattr(e, 'status_code') else 'N/A'}")
        print(f"   Error: {str(e)}")
        if hasattr(e, 'error') and isinstance(e.error, dict):
            print(f"   Error details: {e.error}")
        return None
    except razorpay.errors.ServerError as e:
        print(f"❌ Server Error for {plan_data['item']['name']}: {str(e)}")
        return None
    except Exception as e:
        print(f"❌ Failed to create plan {plan_data['item']['name']}: {type(e).__name__}")
        print(f"   Error: {str(e)}")
        if hasattr(e, 'error'):
            print(f"   Error details: {e.error}")
        if hasattr(e, 'status_code'):
            print(f"   Status code: {e.status_code}")
        return None

def check_existing_plans():
    """Check if plans already exist"""
    try:
        plans = client.plan.all()
        existing = {}
        if plans and 'items' in plans:
            for plan in plans['items']:
                item_name = plan.get('item', {}).get('name', '')
                if 'Week Pass' in item_name:
                    existing['week'] = plan['id']
                elif 'Month Subscription' in item_name:
                    existing['month'] = plan['id']
                elif 'Year Subscription' in item_name:
                    existing['year'] = plan['id']
        return existing
    except Exception as e:
        print(f"⚠️  Could not check existing plans: {e}")
        return {}

def main():
    print("Creating Razorpay Plans for subscriptions...")
    print("=" * 60)
    print(f"Using Key ID: {RAZORPAY_KEY_ID[:10]}...")
    print(f"Mode: {'TEST' if 'test' in RAZORPAY_KEY_ID.lower() else 'LIVE'}")
    print("=" * 60)
    
    # Check for existing plans
    print("\nChecking for existing plans...")
    existing_plans = check_existing_plans()
    if existing_plans:
        print(f"Found {len(existing_plans)} existing plan(s):")
        for tier, plan_id in existing_plans.items():
            print(f"  {tier}: {plan_id}")
        print("\nSkipping creation of existing plans.")
    
    created_plans = existing_plans.copy()
    
    # Create missing plans
    for plan_data in PLANS:
        tier_key = plan_data['notes']['tier']
        if tier_key in existing_plans:
            print(f"\n⏭️  Skipping {tier_key} - plan already exists: {existing_plans[tier_key]}")
            continue
            
        plan = create_plan(plan_data)
        if plan:
            created_plans[tier_key] = plan['id']
    
    print("\n" + "=" * 60)
    print("Plan IDs (for environment variables):")
    print("=" * 60)
    
    if not created_plans:
        print("❌ No plans created or found. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Verify your API keys are correct")
        print("2. Check if your Razorpay account has subscription features enabled")
        print("3. Try creating plans manually in Razorpay Dashboard")
        return
    
    for tier in ['week', 'month', 'year']:
        if tier in created_plans:
            print(f"RAZORPAY_PLAN_{tier.upper()}={created_plans[tier]}")
        else:
            print(f"RAZORPAY_PLAN_{tier.upper()}=  # MISSING - create manually")
    
    print("\n" + "=" * 60)
    print("Copy these to your Render environment variables:")
    print("=" * 60)
    for tier in ['week', 'month', 'year']:
        if tier in created_plans:
            print(f"RAZORPAY_PLAN_{tier.upper()}={created_plans[tier]}")
    
    if len(created_plans) == 3:
        print("\n✅ All plans created successfully!")
    else:
        print(f"\n⚠️  Only {len(created_plans)}/3 plans created. Please create the missing ones manually.")

if __name__ == "__main__":
    main()

