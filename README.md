# Dark Souls Forums BE Setup

## Prerequisites

1. Docker desktop

## Setup

1. Setup environmental variables:  
```cp .env.placeholder .env```
2. Launch the containers:  
`docker-compose up --build -d`

---

## Available Services (after startup)
- **FastAPI app** → http://localhost:8000  
- **Swagger UI** → http://localhost:8000/docs  
- **pgAdmin** → http://localhost:8080  

---

## pgAdmin Credentials
- Username: admin@admin.com  
- Password: admin  
