from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, auth

security = HTTPBearer()

async def get_current_doctor(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> models.Doctor:
    """
    Dependency to get the currently authenticated doctor from JWT token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    payload = auth.decode_access_token(token)
    
    if payload is None:
        raise credentials_exception
    
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    
    doctor = db.query(models.Doctor).filter(models.Doctor.email == email).first()
    if doctor is None:
        raise credentials_exception
    
    if not doctor.is_active:
        raise HTTPException(status_code=400, detail="Inactive doctor account")
    
    return doctor
    # return db.query(models.Doctor).first()