from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas, models
from app.database import get_db
from app.dependencies import get_current_doctor
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/diagnosis", tags=["Diagnosis"])

@router.get("", response_model=List[schemas.DiagnosisCode])
def search_diagnosis(
    search: str = Query(
        ..., 
        min_length=1, 
        max_length=100,
        description="Search term for diagnosis codes (minimum 1 character)"
    ),
    current_doctor: models.Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """
    Search diagnosis codes by code or description.
    
    The search is case-insensitive and matches partial strings.
    Returns up to 50 matching results.
    
    Examples:
    - Search by code: "A00" → returns codes starting with A00
    - Search by description: "cholera" → returns all cholera-related codes
    - Search by partial: "fever" → returns all fever-related diagnoses
    
    Requires authentication with valid JWT token.
    """
    try:
        # Validate search term
        search_term = search.strip()
        if not search_term:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Search term cannot be empty"
            )
        
        if len(search_term) > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Search term too long (maximum 100 characters)"
            )
        
        results = crud.search_diagnosis_codes(db, search_term)
        
        logger.info(
            f"Diagnosis search by {current_doctor.email}: "
            f"'{search_term}' returned {len(results)} results"
        )
        
        return results
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching diagnosis codes: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search diagnosis codes"
        )