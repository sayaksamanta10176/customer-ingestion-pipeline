# Customer Data Pipeline

A data pipeline with 3 Docker services that fetches customer data from a Flask mock server and stores it in a PostgreSQL database via a FastAPI pipeline.

## Architecture

```
Flask Mock Server (port 5000) → FastAPI Pipeline (port 8000) → PostgreSQL (port 5432)
```

## Prerequisites

- Docker Desktop (running)
- Git

## Project Structure

```
project-root/
├── docker-compose.yml
├── README.md
├── mock-server/
│   ├── app.py
│   ├── data/customers.json
│   ├── Dockerfile
│   └── requirements.txt
└── pipeline-service/
    ├── main.py
    ├── models/customer.py
    ├── services/ingestion.py
    ├── database.py
    ├── Dockerfile
    └── requirements.txt
```

## Services

### Flask Mock Server (port 5000)
Serves customer data from a JSON file with pagination support.

### FastAPI Pipeline (port 8000)
Fetches customer data from Flask and ingests it into PostgreSQL using upsert logic.

### PostgreSQL (port 5432)
Stores customer data in the `customers` table.

## Getting Started

### 1. Clone the repository
```bash
git clone <repository-url>
cd project-root
```

### 2. Start all services
```bash
docker-compose up --build
```

### 3. Verify all services are running
```bash
docker-compose ps
```

## API Endpoints

### Flask Mock Server

| Method | Endpoint | Description |
|---|---|---|
| GET | /api/health | Health check |
| GET | /api/customers | Paginated list of customers |
| GET | /api/customers/{id} | Single customer by ID |

### FastAPI Pipeline

| Method | Endpoint | Description |
|---|---|---|
| GET | /api/health | Health check |
| POST | /api/ingest | Ingest data from Flask into PostgreSQL |
| GET | /api/customers | Paginated list from database |
| GET | /api/customers/{id} | Single customer from database |

## Testing

### Test Flask Mock Server
```bash
# Health check
curl http://localhost:5000/api/health

# Get paginated customers
curl "http://localhost:5000/api/customers?page=1&limit=5"

# Get single customer
curl http://localhost:5000/api/customers/<customer_id>
```

### Test FastAPI Pipeline
```bash
# Health check
curl http://localhost:8000/api/health

# Ingest data from Flask into PostgreSQL
curl -X POST http://localhost:8000/api/ingest

# Get paginated customers from database
curl "http://localhost:8000/api/customers?page=1&limit=5"

# Get single customer from database
curl http://localhost:8000/api/customers/<customer_id>
```

## Stopping Services
```bash
docker-compose down
```

## Environment Variables

The pipeline service uses encrypted environment variables stored in `pipeline-service/.env`:

| Variable | Description |
|---|---|
| SECRET_KEY | Fernet encryption key |
| DB_USER | PostgreSQL username (encrypted) |
| DB_PASS | PostgreSQL password (encrypted) |
| DB_HOST | PostgreSQL host (encrypted) |
| DB_NAME | PostgreSQL database name (encrypted) |
