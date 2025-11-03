from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, diagnosis, consultation

# todo: put in validation error handling
# rn it's very naive

app = FastAPI(
    title="ClinicCare Medical Consultation API",
    description="API for managing medical consultation notes",
    version="1.0.0"
)

# CORS middleware for our Vue frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:80",
        "http://localhost:5173",
        "http://localhost:8080",
        "http://frontend",
        "*"  # Allow all origins in development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# if we have time.
# app.include_router(auth.router)
app.include_router(diagnosis.router)
app.include_router(consultation.router)

@app.get("/")
def read_root():
    return {
        "message": "ClinicCare Medical Consultation API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}