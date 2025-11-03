from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas, models
from app.database import get_db
from app.dependencies import get_current_doctor
from app.exceptions import NotFoundException, ValidationException
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/consultation", tags=["Consultation"])

@router.post("", response_model=schemas.ConsultationResponse, status_code=status.HTTP_201_CREATED)
def create_consultation(
    consultation: schemas.ConsultationCreate,
    current_doctor: models.Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """
    Create a new consultation note with diagnosis codes.
    
    Requirements:
    - Patient name: 2-255 characters
    - Consultation date: Cannot be in the future
    - Diagnosis codes: 1-20 valid ICD-10 codes
    - Notes: Optional, max 5000 characters
    
    Example request body:
    {
        "patient_name": "John Doe",
        "consultation_date": "2024-11-02",
        "notes": "Patient presents with fever and headache",
        "diagnosis_codes": ["A00", "A01"]
    }
    
    The consultation will be linked to the currently logged-in doctor.
    """
    try:
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
        
        logger.info(
            f"Consultation created: ID={db_consultation.id}, "
            f"Doctor={current_doctor.email}, Patient={consultation.patient_name}"
        )
        return response
        
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating consultation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create consultation"
        )

@router.get("", response_model=List[schemas.ConsultationResponse])
def list_consultations(
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return (1-100)"),
    current_doctor: models.Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """
    List all consultation notes for the current logged-in doctor.
    
    Returns consultations in reverse chronological order (newest first).
    Supports pagination with skip and limit parameters.
    
    Each consultation includes:
    - Patient information
    - Consultation date and notes
    - Doctor who created it
    - All associated diagnosis codes with descriptions
    
    Requires valid JWT token in Authorization header.
    """
    try:
        # Get consultations for current doctor only
        consultations = crud.get_consultations(
            db, 
            doctor_id=current_doctor.id, 
            skip=skip, 
            limit=limit
        )
        
        # Format response
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
        
        logger.info(f"Retrieved {len(response)} consultations for doctor {current_doctor.email}")
        return response
        
    except Exception as e:
        logger.error(f"Error retrieving consultations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve consultations"
        )