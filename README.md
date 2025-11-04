# clinic-web-app

### Pre-Requisites

- Have Docker installed
- Have a web browser to see the frontend

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

## Features

### Backend

The backend implements FastAPI using input validation with Pydantic. Authentication uses JWT.

#### All Available Endpoints

| Method | Endpoint                   | Auth Required | Description            |
| ------ | -------------------------- | ------------- | ---------------------- |
| GET    | `/`                        | No            | API info               |
| GET    | `/health`                  | No            | Health check           |
| POST   | `/auth/register`           | No            | Register new doctor    |
| POST   | `/auth/login`              | No            | Login and get token    |
| GET    | `/auth/me`                 | Yes           | Get current doctor     |
| GET    | `/diagnosis?search=<term>` | Yes           | Search diagnosis codes |
| POST   | `/consultation`            | Yes           | Create consultation    |
| GET    | `/consultation`            | Yes           | List consultations     |

### Database

I decided to use PotgreSQL because it scales better. The database consists of 4 tables:

- `doctors`, used to store doctor accounts
- `diagnosis_codes`, diagnosis codes and their descriptions
- `consultations`, tracks consultations, contains patient name, date, notes,and which doctor saw them
- `consultation_diagnoses`, junction table to connect consultations to their respective diagnoses

This is structured to allow future queries such as "all consultations with diagnosis A00" to be easy. We can also add and remove diagnoses without string manipulation, and can get statistics e.g. on the most common diagnoses.
