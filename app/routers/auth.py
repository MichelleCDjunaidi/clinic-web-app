from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas, auth, models
from app.database import get_db
from app.dependencies import get_current_doctor

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=schemas.Doctor, status_code=status.HTTP_201_CREATED)
def register_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    """
    Register a new doctor account
    """
    # Check if doctor already exists
    db_doctor = crud.get_doctor_by_email(db, email=doctor.email)
    if db_doctor:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    return crud.create_doctor(db=db, doctor=doctor)

@router.post("/login", response_model=schemas.Token)
def login(login_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    """
    Login with email and password to receive JWT token
    """
    doctor = crud.authenticate_doctor(db, login_data.email, login_data.password)
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": doctor.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.Doctor)
def read_current_doctor(current_doctor: models.Doctor = Depends(get_current_doctor)):
    """
    Get current logged-in doctor information
    """
    return current_doctor