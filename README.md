# Dark souls forums BE setup

## Prerequisites

1. Docker desktop

## Setup

1. `cp .env.example .env`
2. `docker-compose up --build -d`

This will open necessary servers on these ports:

FastAPI app → http://localhost:8000

Swagger UI → http://localhost:8000/docs

pgAdmin → http://localhost:8080

pg admin logins

username -> admin@admin.com
password -> admin
