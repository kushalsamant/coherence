"""
Script to delete a Razorpay Plan
Run this to remove the unused Day Pass subscription plan
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

# Day Pass plan ID to delete
DAY_PASS_PLAN_ID = "plan_Rha6hD20i2gj8W"

def delete_plan(plan_id):
    """Delete a Razorpay Plan"""
    try:
        print(f"\nDeleting plan: {plan_id}")
        
        # First, check if plan exists
        try:
            plan = client.plan.fetch(plan_id)
            print(f"Found plan: {plan.get('item', {}).get('name', 'Unknown')}")
        except Exception as e:
            print(f"⚠️  Plan not found or already deleted: {e}")
            return False
        
        # Razorpay doesn't support deleting plans via API
        # Plans must be deleted manually from the dashboard
        print("⚠️  Razorpay doesn't allow deleting plans via API")
        print("   Plans must be deleted manually from the dashboard")
        return False
            
    except Exception as e:
        print(f"❌ Failed to delete plan: {type(e).__name__}")
        print(f"   {str(e)}")
        return False

def main():
    print("Deleting unused Day Pass subscription plan...")
    print("=" * 60)
    print(f"Using Key ID: {RAZORPAY_KEY_ID[:10]}...")
    print(f"Mode: {'TEST' if 'test' in RAZORPAY_KEY_ID.lower() else 'LIVE'}")
    print("=" * 60)
    
    success = delete_plan(DAY_PASS_PLAN_ID)
    
    if success:
        print("\n" + "=" * 60)
        print("✅ Plan deleted successfully!")
        print("\nNote: Remove RAZORPAY_PLAN_DAY from sketch2bim.env.production if present")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("⚠️  Could not delete plan via API")
        print("\nTo delete manually:")
        print("1. Go to Razorpay Dashboard → Subscriptions → Plans")
        print("2. Find 'Day Pass Subscription' (plan_Rha6hD20i2gj8W)")
        print("3. Click on it and delete")
        print("=" * 60)

if __name__ == "__main__":
    main()

