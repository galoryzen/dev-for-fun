# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastAPI-based email blacklist management service that allows applications to maintain a global blacklist of email addresses with bearer token authentication. The application uses PostgreSQL for persistence and is deployed on AWS Elastic Beanstalk.

## Development Commands

### Local Development with Docker

Start all services (PostgreSQL + FastAPI):
```bash
docker-compose up -d
```

View application logs:
```bash
docker-compose logs -f app
```

Stop services:
```bash
docker-compose down
```

Access points when running locally:
- API: http://localhost:8000
- Health Check: http://localhost:8000/health
- Interactive API Docs: http://localhost:8000/docs
- Swagger UI: http://localhost:8000/redoc

### AWS Elastic Beanstalk Deployment

Deploy changes to EB:
```bash
eb deploy
```

View EB application logs:
```bash
eb logs
```

Check environment status:
```bash
eb status
```

SSH into EC2 instance:
```bash
eb ssh
```

When SSH'd into the EC2 instance, view application logs:
```bash
# Follow real-time logs
sudo tail -f /var/log/web.stdout.log

# Check last 20 lines
sudo tail -20 /var/log/web.stdout.log

# Check service status
sudo systemctl status web.service
```

## Architecture

### Application Structure

The application follows a layered FastAPI architecture:

1. **Entry Point (`app/main.py`)**:
   - Initializes FastAPI app
   - Creates database tables on startup via SQLAlchemy's `Base.metadata.create_all()`
   - Includes router from `app/routers/blacklist.py`
   - Provides testing endpoints: `/health`, `/reset`, `/all`, `/error`, `/env`
   - Global exception handler returns generic 500 errors

2. **Database Layer (`app/database.py`)**:
   - Constructs PostgreSQL connection string from environment variables with `RDS_*` prefix
   - Provides `get_db()` dependency for request-scoped database sessions
   - Uses SQLAlchemy's declarative base

3. **Models (`app/models.py`)**:
   - Single table: `blacklist_entries` with `email` as primary key
   - Tracks `app_uuid`, `blocked_reason`, `ip_address`, and `created_at` timestamp

4. **Schemas (`app/schemas.py`)**:
   - Pydantic models for validation
   - `BlacklistCreate`: validates email format and UUID
   - `BlacklistCheckResponse`: returns blacklist status with metadata

5. **Router (`app/routers/blacklist.py`)**:
   - All endpoints require Bearer token authentication (verified against `AUTH_TOKEN` env var)
   - `POST /blacklists`: Add email to blacklist (captures request IP automatically)
   - `GET /blacklists/{email}`: Check if email is blacklisted
   - Returns 409 Conflict if email already exists, 403 for invalid auth

### Environment Configuration

The application uses environment variables with RDS naming convention for database config:
- `RDS_HOSTNAME`: Database host
- `RDS_PORT`: Database port
- `RDS_USERNAME`: Database user
- `RDS_PASSWORD`: Database password
- `RDS_DB_NAME`: Database name
- `AUTH_TOKEN`: Static bearer token for API authentication

See `.env.example` for local development defaults.

### Deployment Architecture

Two deployment modes:

1. **Local (Docker Compose)**:
   - PostgreSQL container with healthcheck
   - App container with hot-reload enabled (volume mount for `./app`)
   - App runs on port 8000 internally and externally

2. **AWS Elastic Beanstalk**:
   - Uses `Procfile` to define web process
   - Custom healthcheck path configured in `.ebextensions/01_healthcheck.config`
   - Database credentials injected via EB environment variables
   - Application runs on port 8000

### Key Technical Decisions

- **No Alembic migrations in practice**: Tables are created via `Base.metadata.create_all()` on startup despite alembic being in requirements
- **Email as primary key**: Enforces uniqueness at database level
- **IP address auto-capture**: Client IP is extracted from `request.client.host` and stored with each entry
- **Static token auth**: Simple bearer token authentication (not OAuth or JWT)
- **Testing endpoints exposed**: `/reset`, `/all`, `/error`, `/env` endpoints remain in production code