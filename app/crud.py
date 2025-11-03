from sqlalchemy.orm import Session
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app import models, schemas, auth
from app.exceptions import DatabaseException, NotFoundException, DuplicateException
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

# Doctor CRUD
def get_doctor_by_email(db: Session, email: str) -> Optional[models.Doctor]:
    """Get a doctor by email"""
    try:
        return db.query(models.Doctor).filter(models.Doctor.email == email).first()
    except SQLAlchemyError as e:
        logger.error(f"Database error getting doctor by email: {str(e)}")
        raise DatabaseException("Failed to retrieve doctor information")

def create_doctor(db: Session, doctor: schemas.DoctorCreate) -> models.Doctor:
    """Create a new doctor"""
    try:
        # Check if doctor already exists
        existing_doctor = get_doctor_by_email(db, doctor.email)
        if existing_doctor:
            raise DuplicateException(f"Doctor with email {doctor.email} already exists")

        print(0, f"here's the password {doctor.password}")
        
        hashed_password = auth.get_password_hash(doctor.password)
        db_doctor = models.Doctor(
            email=doctor.email,
            full_name=doctor.full_name,
            hashed_password=hashed_password
        )
        db.add(db_doctor)
        db.commit()
        db.refresh(db_doctor)
        return db_doctor
    except DuplicateException:
        db.rollback()
        raise
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error creating doctor: {str(e)}")
        raise DuplicateException(f"Doctor with email {doctor.email} already exists")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error creating doctor: {str(e)}")
        raise DatabaseException("Failed to create doctor account")

def authenticate_doctor(db: Session, email: str, password: str) -> Optional[models.Doctor]:
    """Authenticate a doctor with email and password"""
    try:
        doctor = get_doctor_by_email(db, email)
        if not doctor:
            return None
        if not auth.verify_password(password, doctor.hashed_password):
            return None
        if not doctor.is_active:
            return None
        return doctor
    except SQLAlchemyError as e:
        logger.error(f"Database error authenticating doctor: {str(e)}")
        raise DatabaseException("Authentication failed due to database error")

# Diagnosis CRUD
def search_diagnosis_codes(db: Session, search: str, limit: int = 50) -> List[models.DiagnosisCode]:
    """Search diagnosis codes by code or description"""
    try:
        if not search or not search.strip():
            return []
        
        search_pattern = f"%{search.strip()}%"
        results = db.query(models.DiagnosisCode).filter(
            or_(
                models.DiagnosisCode.code.ilike(search_pattern),
                models.DiagnosisCode.description.ilike(search_pattern)
            )
        ).limit(limit).all()
        
        return results
    except SQLAlchemyError as e:
        logger.error(f"Database error searching diagnosis codes: {str(e)}")
        raise DatabaseException("Failed to search diagnosis codes")

def get_diagnosis_code_by_code(db: Session, code: str) -> Optional[models.DiagnosisCode]:
    """Get a single diagnosis code by its code string"""
    try:
        if not code or not code.strip():
            return None
        
        return db.query(models.DiagnosisCode).filter(
            models.DiagnosisCode.code == code.strip().upper()
        ).first()
    except SQLAlchemyError as e:
        logger.error(f"Database error getting diagnosis code: {str(e)}")
        raise DatabaseException("Failed to retrieve diagnosis code")

# Consultation CRUD
def create_consultation(
    db: Session, 
    consultation: schemas.ConsultationCreate, 
    doctor_id: int
) -> models.Consultation:
    """Create a new consultation with associated diagnosis codes"""
    try:
        # Validate all diagnosis codes exist before creating consultation
        valid_codes = []
        invalid_codes = []
        
        for code in consultation.diagnosis_codes:
            diagnosis_code = get_diagnosis_code_by_code(db, code)
            if diagnosis_code:
                valid_codes.append(diagnosis_code)
            else:
                invalid_codes.append(code)
        
        if invalid_codes:
            raise NotFoundException(
                f"Invalid diagnosis codes: {', '.join(invalid_codes)}. "
                "Please ensure all codes exist in the system."
            )
        
        # Create consultation
        db_consultation = models.Consultation(
            doctor_id=doctor_id,
            patient_name=consultation.patient_name,
            consultation_date=consultation.consultation_date,
            notes=consultation.notes
        )
        db.add(db_consultation)
        db.flush()  # Get the consultation ID
        
        # Add diagnosis codes
        for diagnosis_code in valid_codes:
            consultation_diagnosis = models.ConsultationDiagnosis(
                consultation_id=db_consultation.id,
                diagnosis_code_id=diagnosis_code.id
            )
            db.add(consultation_diagnosis)
        
        db.commit()
        db.refresh(db_consultation)
        return db_consultation
        
    except NotFoundException:
        db.rollback()
        raise
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error creating consultation: {str(e)}")
        raise DatabaseException("Failed to create consultation due to data integrity issue")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error creating consultation: {str(e)}")
        raise DatabaseException("Failed to create consultation")

def get_consultations(
    db: Session, 
    doctor_id: Optional[int] = None,
    skip: int = 0, 
    limit: int = 100
) -> List[models.Consultation]:
    """Get consultations, optionally filtered by doctor"""
    try:
        query = db.query(models.Consultation)
        
        if doctor_id:
            query = query.filter(models.Consultation.doctor_id == doctor_id)
        
        consultations = query.order_by(
            models.Consultation.consultation_date.desc()
        ).offset(skip).limit(limit).all()
        
        return consultations
        
    except SQLAlchemyError as e:
        logger.error(f"Database error getting consultations: {str(e)}")
        raise DatabaseException("Failed to retrieve consultations")