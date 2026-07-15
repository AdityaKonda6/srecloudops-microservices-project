# Microservices Practice App

A simple Python microservices project with PostgreSQL for practicing DevOps workflows.

## Services

- `catalog-service`: FastAPI service with product catalog (PostgreSQL-backed)
- `orders-service`: FastAPI service for managing orders (PostgreSQL-backed)
- `ui`: FastAPI web interface with Jinja2 templates (no Streamlit)
- `postgres`: PostgreSQL database with two separate databases (catalog, orders)

## Local run

1. Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the services in separate terminals (requires PostgreSQL running locally on 5432):

```bash
# Terminal 1
uvicorn catalog_service.app.main:app --host 0.0.0.0 --port 8001 --reload

# Terminal 2
uvicorn orders_service.app.main:app --host 0.0.0.0 --port 8002 --reload

# Terminal 3
uvicorn ui.app:app --host 0.0.0.0 --port 8000 --reload
```

3. Open the UI at http://localhost:8000

## Docker Compose

Easiest way to run everything with PostgreSQL:

```bash
docker compose up --build
```

Then open the UI at http://localhost:8000

**Note:** PostgreSQL persists data in a named volume `postgres-data`. To reset:

```bash
docker compose down -v
docker compose up --build
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   UI (FastAPI + Jinja2)                 │
│                    http://localhost:8000                │
└────────────────┬──────────────────────────┬─────────────┘
                 │                          │
         ┌───────▼─────────┐       ┌───────▼──────────┐
         │  Catalog API    │       │   Orders API     │
         │  :8001          │       │   :8002          │
         └────────┬────────┘       └────────┬─────────┘
                  │                         │
                  └─────────────┬───────────┘
                                │
                    ┌───────────▼──────────┐
                    │  PostgreSQL (5432)   │
                    │  ├── catalog DB      │
                    │  └── orders DB       │
                    └──────────────────────┘
```

## Database

- **Engine:** PostgreSQL 16 (Alpine)
- **Credentials:** user=`microservices`, password=`password`
- **Databases:**
  - `catalog` - used by catalog-service
  - `orders` - used by orders-service
- **Data Volume:** `postgres-data` (persists across restarts)

Tables are automatically created on service startup.

## Tech Stack

- **Services:** FastAPI, Uvicorn, SQLAlchemy, Pydantic
- **Database:** PostgreSQL 16
- **UI:** FastAPI with Jinja2 templates
- **Orchestration:** Docker Compose
- **Python:** 3.11

## Suggested practice ideas

- Add Kubernetes manifests (Deployment, Service, PVC for DB)
- Set up database backups and restore procedures
- Add database migrations with Alembic
- Add API gateway or ingress routing
- Implement database connection pooling
- Add monitoring (Prometheus, Grafana)
- Create a CI/CD pipeline with GitHub Actions
- Add API authentication with JWT
- Add comprehensive logging and tracing


