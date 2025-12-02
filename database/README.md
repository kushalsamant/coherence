# Database System

This directory contains the database schema definitions and migration system for the KVSHVL platform.

## Overview

The platform uses **Upstash Postgres** with two separate databases:
- **ASK Database** - For the ASK Research Tool
- **Sketch2BIM Database** - For the Sketch2BIM conversion service

**Note**: Reframe uses Redis (Upstash Redis), not PostgreSQL.

## Structure

```
database/
├── migrations/
│   ├── ask/                    # ASK database Alembic migrations
│   │   ├── alembic.ini
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   │       └── 001_initial_schema.py
│   ├── sketch2bim/             # Sketch2BIM database Alembic migrations
│   │   ├── alembic.ini
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   │       ├── 001_initial_schema.py
│   │       ├── 002_add_legend_to_jobs.py
│   │       └── ... (10 total migrations)
│   └── README.md
├── schemas/
│   ├── ask_schema.sql          # Reference SQL schema for ASK
│   └── sketch2bim_schema.sql   # Reference SQL schema for Sketch2BIM
├── MIGRATION_SYSTEMS.md        # Detailed migration system documentation
└── README.md                   # This file
```

## Migration System

We use **Alembic** for all database migrations. Alembic provides:
- Version control for schema changes
- Rollback capability
- Automatic migration on application startup
- Data migration support

### Running Migrations

**Automatic (Recommended)**:
Migrations run automatically on application startup via:
- ASK: `apps/platform-api/utils/ask/migrations.py`
- Sketch2BIM: `apps/platform-api/utils/sketch2bim/migrations.py`

**Manual**:

For ASK database:
```bash
cd database/migrations/ask
alembic upgrade head          # Apply all pending migrations
alembic downgrade -1          # Rollback one migration
alembic current               # Show current migration version
alembic history               # Show migration history
```

For Sketch2BIM database:
```bash
cd database/migrations/sketch2bim
alembic upgrade head          # Apply all pending migrations
alembic downgrade -1          # Rollback one migration
alembic current               # Show current migration version
alembic history               # Show migration history
```

### Creating New Migrations

**ASK database**:
```bash
cd database/migrations/ask
alembic revision --autogenerate -m "description of change"
```

**Sketch2BIM database**:
```bash
cd database/migrations/sketch2bim
alembic revision --autogenerate -m "description of change"
```

After creating a migration:
1. Review the generated migration file
2. Test locally
3. Commit to version control
4. Migration will run automatically on next deployment

## Environment Variables

Each database requires its own connection string:

```bash
# ASK Database
ASK_DATABASE_URL=postgresql://user:password@host:5432/ask

# Sketch2BIM Database
SKETCH2BIM_DATABASE_URL=postgresql://user:password@host:5432/sketch2bim
```

## Schema Reference Files

The `schemas/` directory contains SQL files that show the complete current schema. These are:
- **Reference only** - Not for execution
- Generated from SQLAlchemy models
- Updated when schema changes
- Useful for understanding the complete database structure

## Migration Workflow

### For New Databases

1. Create the database in Upstash Postgres
2. Set the environment variable (`ASK_DATABASE_URL` or `SKETCH2BIM_DATABASE_URL`)
3. Run `alembic upgrade head` in the appropriate migration directory
4. Verify tables were created correctly

### For Schema Changes

1. Update the SQLAlchemy model in `apps/platform-api/models/`
2. Generate migration: `alembic revision --autogenerate -m "description"`
3. Review and test the generated migration
4. Commit the migration file
5. Migration runs automatically on next deployment

## Rollback Procedure

If a migration fails or causes issues:

```bash
# Rollback one migration
cd database/migrations/[ask|sketch2bim]
alembic downgrade -1

# Rollback to specific version
alembic downgrade <revision_id>

# Check current version
alembic current
```

## Documentation

- See [MIGRATION_SYSTEMS.md](MIGRATION_SYSTEMS.md) for detailed migration system documentation
- See [migrations/README.md](migrations/README.md) for migration-specific documentation
- See [docs/migrations/](../docs/migrations/) for application-specific migration guides

## Notes

- Upstash Postgres uses **separate databases** (not schemas)
- Each database has its own independent migration history
- Migrations are tracked in the `alembic_version` table
- Auto-run migrations can be disabled with `AUTO_RUN_MIGRATIONS=false` environment variable

