#!/usr/bin/env python3
"""
Check database migration status
Verifies which migrations have been applied to the database
"""
import os
import sys
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from alembic.config import Config
from alembic import command
from alembic.script import ScriptDirectory
from alembic.runtime.migration import MigrationContext
from sqlalchemy import create_engine, inspect
from app.config import settings


def get_current_revision(engine):
    """Get current database revision"""
    with engine.connect() as connection:
        context = MigrationContext.configure(connection)
        return context.get_current_revision()


def get_head_revision(alembic_cfg):
    """Get head revision from Alembic"""
    script = ScriptDirectory.from_config(alembic_cfg)
    return script.get_current_head()


def check_tables_exist(engine):
    """Check if required tables exist"""
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    required_tables = [
        'users',
        'jobs',
        'payments',
        'api_keys',
        'organizations',
        'organization_members'
    ]
    
    missing_tables = [table for table in required_tables if table not in existing_tables]
    
    return {
        'existing': [t for t in required_tables if t in existing_tables],
        'missing': missing_tables,
        'all_exist': len(missing_tables) == 0
    }


def main():
    parser = argparse.ArgumentParser(
        description='Check database migration status'
    )
    parser.add_argument(
        '--database-url',
        type=str,
        help='Database URL (or set DATABASE_URL env var)',
        default=os.getenv('DATABASE_URL') or settings.database_url
    )
    
    args = parser.parse_args()
    
    if not args.database_url:
        print("❌ Error: Database URL required")
        print("   Provide via --database-url argument or DATABASE_URL environment variable")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("Database Migration Status Check")
    print("="*60)
    print(f"Database: {args.database_url.split('@')[-1] if '@' in args.database_url else args.database_url}")
    print("="*60)
    
    try:
        # Create engine
        engine = create_engine(args.database_url)
        
        # Check if alembic_version table exists
        inspector = inspect(engine)
        has_alembic_table = 'alembic_version' in inspector.get_table_names()
        
        if not has_alembic_table:
            print("\n⚠️  Alembic version table does not exist")
            print("   Database has not been initialized with migrations")
            print("   Run: alembic upgrade head")
            sys.exit(1)
        
        # Get current revision
        current_rev = get_current_revision(engine)
        
        # Get head revision
        alembic_cfg = Config(str(Path(__file__).parent.parent / "alembic.ini"))
        head_rev = get_head_revision(alembic_cfg)
        
        print(f"\nCurrent revision: {current_rev or 'None (uninitialized)'}")
        print(f"Head revision: {head_rev}")
        
        if current_rev == head_rev:
            print("\n✅ Database is up to date!")
        elif current_rev is None:
            print("\n⚠️  Database is not initialized")
            print("   Run: alembic upgrade head")
        else:
            print("\n⚠️  Database is behind head revision")
            print("   Run: alembic upgrade head")
        
        # Check tables
        print("\n" + "="*60)
        print("Table Status")
        print("="*60)
        table_status = check_tables_exist(engine)
        
        if table_status['all_exist']:
            print("✅ All required tables exist")
        else:
            print("⚠️  Missing tables:")
            for table in table_status['missing']:
                print(f"   - {table}")
        
        print("\nExisting tables:")
        for table in table_status['existing']:
            print(f"   ✅ {table}")
        
        print("\n" + "="*60)
        if current_rev == head_rev and table_status['all_exist']:
            print("✅ Database is ready for production!")
            return 0
        else:
            print("⚠️  Database needs migration")
            return 1
        
    except Exception as e:
        print(f"\n❌ Error checking migration status: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())

