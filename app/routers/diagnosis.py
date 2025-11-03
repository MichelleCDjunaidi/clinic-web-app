from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas, models
from app.database import get_db
from app.dependencies import get_current_doctor

router = APIRouter(prefix="/diagnosis", tags=["Diagnosis"])

@router.get("", response_model=List[schemas.DiagnosisCode])
def search_diagnosis(
    search: str = Query(..., min_length=1, description="Search term for diagnosis codes"),
    current_doctor: models.Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """
    Search diagnosis codes by code or description.
    Requires authentication.
    
    Example: /diagnosis?search=cholera
    """
    results = crud.search_diagnosis_codes(db, search)
    return results