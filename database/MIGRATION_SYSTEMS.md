# Database Migration Systems Documentation

## Overview

This repository uses **Alembic** for all database migrations. The migration system is unified and located in `database/migrations/` with separate directories for each database:

1. **ASK Migrations** (`database/migrations/ask/`) - Alembic migrations for ASK database
2. **Sketch2BIM Migrations** (`database/migrations/sketch2bim/`) - Alembic migrations for Sketch2BIM database

## Alembic Migration Structure

```
database/migrations/
├── ask/
│   ├── alembic.ini                 # ASK Alembic configuration
│   ├── env.py                      # ASK migration environment
│   ├── script.py.mako              # Migration template
│   └── versions/
│       └── 001_initial_schema.py   # Initial ASK schema
├── sketch2bim/
│   ├── alembic.ini                 # Sketch2BIM Alembic configuration
│   ├── env.py                      # Sketch2BIM migration environment
│   ├── script.py.mako              # Migration template
│   └── versions/
│       ├── 001_initial_schema.py
│       ├── 002_add_legend_to_jobs.py
│       └── ... (10 total migrations)
└── README.md
```

## Usage

### Automatic (Recommended)

Migrations run automatically on application startup:
- **ASK**: Via `apps/platform-api/utils/ask/migrations.py`
- **Sketch2BIM**: Via `apps/platform-api/utils/sketch2bim/migrations.py`
- Controlled by `AUTO_RUN_MIGRATIONS` setting (default: `true`)

### Manual Migration Commands

**ASK database**:
```bash
cd database/migrations/ask
alembic upgrade head          # Apply all pending migrations
alembic downgrade -1          # Rollback one migration
alembic current               # Show current migration version
alembic history               # Show migration history
alembic revision --autogenerate -m "description"  # Create new migration
```

**Sketch2BIM database**:
```bash
cd database/migrations/sketch2bim
alembic upgrade head          # Apply all pending migrations
alembic downgrade -1          # Rollback one migration
alembic current               # Show current migration version
alembic history               # Show migration history
alembic revision --autogenerate -m "description"  # Create new migration
```

## Schema Reference Files

The `database/schemas/` directory contains SQL files showing the complete current schema:
- `ask_schema.sql` - Complete ASK database schema
- `sketch2bim_schema.sql` - Complete Sketch2BIM database schema

These files are:
- **Reference only** - Not for execution
- Generated from SQLAlchemy models
- Useful for understanding the complete structure
- Updated when schema changes significantly

## Migration Workflow

### Initial Setup (New Database)
1. Create Upstash Postgres database
2. Set environment variable (`ASK_DATABASE_URL` or `SKETCH2BIM_DATABASE_URL`)
3. Run `alembic upgrade head` in the appropriate migration directory
4. Verify tables were created

### Making Schema Changes
1. Update SQLAlchemy model in `apps/platform-api/models/`
2. Create new migration: `alembic revision --autogenerate -m "description"`
3. Review generated migration file
4. Test migration locally
5. Commit migration file
6. Deploy - migration runs automatically on startup

## Environment Variables

Required environment variables:
```bash
ASK_DATABASE_URL=postgresql://user:password@host:5432/ask
SKETCH2BIM_DATABASE_URL=postgresql://user:password@host:5432/sketch2bim
AUTO_RUN_MIGRATIONS=true  # Optional, defaults to true
```

## Notes

- **ASK Database**: Uses Alembic migrations in `database/migrations/ask/`
- **Sketch2BIM Database**: Uses Alembic migrations in `database/migrations/sketch2bim/`
- **Reframe**: Uses Redis only, no SQL database migrations
- **Upstash Postgres**: Uses separate databases (not schemas)
- All legacy SQL migration files have been removed
- Migration history is tracked in `alembic_version` table in each database

