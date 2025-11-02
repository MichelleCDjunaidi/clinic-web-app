from sqlalchemy.orm import Session
from sqlalchemy import or_
from app import models, schemas, auth
from typing import List, Optional

# Doctor CRUD
def get_doctor_by_email(db: Session, email: str) -> Optional[models.Doctor]:
    """Get a doctor by email"""
    return db.query(models.Doctor).filter(models.Doctor.email == email).first()

def create_doctor(db: Session, doctor: schemas.DoctorCreate) -> models.Doctor:
    """Create a new doctor"""
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

# well, we haven't implemented auth yet. this thing is just here for dreams
def authenticate_doctor(db: Session, email: str, password: str) -> Optional[models.Doctor]:
    """Authenticate a doctor with email and password"""
    doctor = get_doctor_by_email(db, email)
    if not doctor:
        return None
    if not auth.verify_password(password, doctor.hashed_password):
        return None
    return doctor

# Diagnosis CRUD
def search_diagnosis_codes(db: Session, search: str, limit: int = 50):
    """Search diagnosis codes by code or description"""
    search_pattern = f"%{search}%"
    return db.query(models.DiagnosisCode).filter(
        or_(
            models.DiagnosisCode.code.ilike(search_pattern),
            models.DiagnosisCode.description.ilike(search_pattern)
        )
    ).limit(limit).all()

def get_diagnosis_code_by_code(db: Session, code: str):
    """Get a single diagnosis code by its code string"""
    return db.query(models.DiagnosisCode).filter(
        models.DiagnosisCode.code == code
    ).first()

# Consultation CRUD
def create_consultation(
    db: Session, 
    consultation: schemas.ConsultationCreate, 
    doctor_id: int
) -> models.Consultation:
    """Create a new consultation with associated diagnosis codes"""
    db_consultation = models.Consultation(
        doctor_id=doctor_id,
        patient_name=consultation.patient_name,
        consultation_date=consultation.consultation_date,
        notes=consultation.notes
    )
    db.add(db_consultation)
    db.flush()  # write to the database to get the consultation ID
    
    # Add diagnosis codes
    # note that the Pydantic schemas map frontend input essentially
    for code_str in consultation.diagnosis_codes:
        diagnosis_code = get_diagnosis_code_by_code(db, code_str)
        if diagnosis_code:
            consultation_diagnosis = models.ConsultationDiagnosis(
                consultation_id=db_consultation.id,
                diagnosis_code_id=diagnosis_code.id
            )
            db.add(consultation_diagnosis)
    
    db.commit()
    db.refresh(db_consultation)
    return db_consultation

def get_consultations(
    db: Session, 
    doctor_id: Optional[int] = None,
    skip: int = 0, 
    limit: int = 100
) -> List[models.Consultation]:
    """Get consultations, optionally filtered by doctor"""
    query = db.query(models.Consultation)
    if doctor_id:
        query = query.filter(models.Consultation.doctor_id == doctor_id)
    return query.order_by(models.Consultation.consultation_date.desc()).offset(skip).limit(limit).all()