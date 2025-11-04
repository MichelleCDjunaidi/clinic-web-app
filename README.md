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

## Backend

The backend implements FastAPI using input validation with Pydantic. Authentication uses JWT.

### All Available FastAPI Endpoints

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

### Pydantic Validation

Each schema defines field constraints, type safety, and custom validators to ensure consistent and secure API behavior. They come each with relevant error messages e.g. giving a password that doesn't contain a digit would throw a `ValueError` `Password must contain at least one digit`.

#### 1. Authentication Schemas

#### `DoctorCreate`

Handles user registration validation.

**Fields:**

- `email`: Must be a valid email address (`EmailStr`).
- `full_name`: 2–255 characters, cannot be empty or whitespace.
- `password`: 8–72 characters, must contain **at least one letter** and **one digit**.

**Custom Validators:**

- `password_strength`: Ensures password complexity (letters and digits required).
- `name_must_not_be_empty`: Strips whitespace and rejects empty names.

#### `Doctor`

Returned after registration or login.

- Includes `id`, `is_active`, and `created_at`.
- Uses `ConfigDict(from_attributes=True)` for ORM compatibility.

#### `LoginRequest`

Used for login requests.

- `email`: Must be a valid email.
- `password`: Required, non-empty string.

#### `Token` / `TokenData`

- `Token`: Represents JWT tokens returned after successful authentication.
- `TokenData`: Holds token payload data (e.g., user email).

---

#### 2. Diagnosis Schemas

#### `DiagnosisCodeBase`

- `code`: ICD-10 code, 2–10 characters.
- `description`: Diagnosis text, up to 500 characters.

#### `DiagnosisCode`

Extends `DiagnosisCodeBase` with:

- `id`
- ORM support via `ConfigDict(from_attributes=True)`

---

#### 3. Consultation Schemas

#### `ConsultationCreate`

Used for creating a new consultation.

**Fields:**

- `patient_name`: 2–255 characters, cannot be blank.
- `consultation_date`: Must not be a future date.
- `notes`: Optional, up to 5000 characters.
- `diagnosis_codes`: List of 1–20 ICD-10 codes.

**Custom Validators:**

- `name_must_not_be_empty`: Ensures non-empty, trimmed patient names.
- `date_not_future`: Rejects consultation dates after today.
- `codes_must_be_valid_format`:

  - Ensures all codes are non-empty and between 2–10 characters.
  - Automatically normalizes codes to uppercase.
  - Removes duplicates while preserving order.

#### `ConsultationResponse`

Returned on successful retrieval or creation of consultations.

- Includes `id`, `patient_name`, `consultation_date`, `notes`, `doctor_name`, and `diagnoses`.
- Uses ORM compatibility via `ConfigDict(from_attributes=True)`.

## Database

I decided to use PotgreSQL because it scales better. The database consists of 4 tables:

- `doctors`, used to store doctor accounts
- `diagnosis_codes`, diagnosis codes and their descriptions
- `consultations`, tracks consultations, contains patient name, date, notes,and which doctor saw them
- `consultation_diagnoses`, junction table to connect consultations to their respective diagnoses

This is structured to allow future queries such as "all consultations with diagnosis A00" to be easy. We can also add and remove diagnoses without string manipulation, and can get statistics e.g. on the most common diagnoses.

Say, for example, patient John Doe visits on Nov 2, 2024, and was seen by Dr. Tan Lee. Then the main relevant parts (`doctor`, `diagnoses` table and creation times omitted for simplicity) are as following:

`consultations` table:
| id | doctor_id | patient_name | consultation_date | notes |
|----|-----------|--------------|-------------------|--------------------|
| 1 | 1 (links to Dr. Tan Lee on `doctor` table) | John Doe | 2024-11-02 | Fever and nausea |

`consultation_diagnoses` table:
| id | consultation_id | diagnosis_code_id |
|----|-----------------|-------------------|
| 1 | 1 | 5 (links to A00 - Cholera) |
| 2 | 1 | 6 (links to A01 - Typhoid) |

## Frontend

I used Vue with scoped style CSS as standard for Vue development.
