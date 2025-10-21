# Blacklist API - Email Blacklist Management Service

Grupo DevForFun

## Features

- Add emails to a global blacklist
- Check if an email is blacklisted
- Bearer token authentication
- IP address and timestamp tracking
- PostgreSQL database backend
- Docker support for local development

## Local Development with Docker

### Prerequisites

- Docker Desktop or Docker Engine + Docker Compose
- Git

### Quick Start

1. **Clone the repository** (if not already done)

2. **Start the services**
   ```bash
   docker-compose up -d
   ```

   This will start:
   - PostgreSQL database on port 5432
   - FastAPI application on port 8000

3. **Check the services are running**
   ```bash
   docker-compose ps
   ```

4. **View logs**
   ```bash
   docker-compose logs -f app
   ```

5. **Access the API**
   - API Base URL: http://localhost:8000
   - Health Check: http://localhost:8000/health
   - Interactive API Docs: http://localhost:8000/docs
   - Alternative API Docs: http://localhost:8000/redoc

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application entry point
│   ├── database.py       # Database configuration
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   └── routers/
│       ├── __init__.py
│       └── blacklist.py  # Blacklist endpoints
├── tests/
|  ├── test.py
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── requirements.txt
├── Procfile              # For AWS Elastic Beanstalk
└── README.md
```

## Database Schema

**Table:** `blacklist_entries`

| Column         | Type         | Constraints             |
| -------------- | ------------ | ----------------------- |
| email          | VARCHAR(255) | PRIMARY KEY             |
| app_uuid       | VARCHAR(255) | NOT NULL                |
| blocked_reason | VARCHAR(255) | NULL                    |
| ip_address     | VARCHAR(45)  | NOT NULL                |
| created_at     | TIMESTAMP    | NOT NULL, DEFAULT NOW() |


## Ejecución tests:
Se implementaron pruebas con Pytest para validar el correcto funcionamiento de los endpoints de la API.

Estas pruebas validan los principales endpoints:
- /health → Verifica el estado del servicio.
- /blacklists → Agrega y consulta correos bloqueados.
- /reset → Restablece la base de datos (opcional para entorno de pruebas).

**Ejecución**
``` bash
pytest -v tests/test.py
```