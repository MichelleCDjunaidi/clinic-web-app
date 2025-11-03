from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas, models
from app.database import get_db
from app.dependencies import get_current_doctor

router = APIRouter(prefix="/consultation", tags=["Consultation"])

# once we implement auth, this all should be behind auth

@router.post("", response_model=schemas.ConsultationResponse, status_code=201)
def create_consultation(
    consultation: schemas.ConsultationCreate,
    current_doctor: models.Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """
    Create a new consultation note with diagnosis codes.
    
    Example request body:
    {
        "patient_name": "John Doe",
        "consultation_date": "2024-11-02",
        "notes": "Patient presents with fever and headache",
        "diagnosis_codes": ["A00", "A01"]
    }
    """
    # Validate that all diagnosis codes exist
    invalid_codes = []
    for code in consultation.diagnosis_codes:
        if not crud.get_diagnosis_code_by_code(db, code):
            invalid_codes.append(code)
    
    if invalid_codes:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid diagnosis codes: {', '.join(invalid_codes)}"
        )
    
    db_consultation = crud.create_consultation(db, consultation, current_doctor.id)
    
    # Format response with diagnosis details
    response = schemas.ConsultationResponse(
        id=db_consultation.id,
        patient_name=db_consultation.patient_name,
        consultation_date=db_consultation.consultation_date,
        notes=db_consultation.notes,
        doctor_name=current_doctor.full_name,
        created_at=db_consultation.created_at,
        diagnoses=[
            schemas.ConsultationDiagnosisResponse(
                code=cd.diagnosis_code.code,
                description=cd.diagnosis_code.description
            )
            for cd in db_consultation.diagnoses
        ]
    )
    
    return response

@router.get("", response_model=List[schemas.ConsultationResponse])
def list_consultations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_doctor: models.Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """
    List all consultation notes for the current doctor.
    Supports pagination with skip and limit parameters.
    """
    consultations = crud.get_consultations(
        db, 
        doctor_id=current_doctor.id, 
        skip=skip, 
        limit=limit
    )
    
    response = []
    for consultation in consultations:
        response.append(schemas.ConsultationResponse(
            id=consultation.id,
            patient_name=consultation.patient_name,
            consultation_date=consultation.consultation_date,
            notes=consultation.notes,
            doctor_name=consultation.doctor.full_name,
            created_at=consultation.created_at,
            diagnoses=[
                schemas.ConsultationDiagnosisResponse(
                    code=cd.diagnosis_code.code,
                    description=cd.diagnosis_code.description
                )
                for cd in consultation.diagnoses
            ]
        ))
    
    return response