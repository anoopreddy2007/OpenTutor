# Database Layer

The OpenTutor database layer uses PostgreSQL with SQLAlchemy.

## Architecture

```text
FastAPI
   ↓
SQLAlchemy
   ↓
Psycopg
   ↓
PostgreSQL