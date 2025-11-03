# clinic-web-app

### Pre-Requisites

- Have Docker installed

### Build and Start All Containers

To standardize setup for this project (so you can install all the libraries without issue e.g. Pydantic has some issues installing in Windows) I decided to Dockerize the backend, the database, and the Vue frontend.

```bash
# Build and start all services
docker-compose up --build
```

This single command will:

1. Build the PostgreSQL database
2. Build the FastAPI backend
3. Build the Vue frontend
4. Start all three containers
5. Initialize the database with 100 ICD-10 codes and a doctor account

See `/docs` for fastAPI documentation and schema requirements.
