from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date, datetime

# Auth Schemas
class DoctorBase(BaseModel):
    email: EmailStr
    full_name: str

class DoctorCreate(DoctorBase):
    password: str

class Doctor(DoctorBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Diagnosis Schemas
class DiagnosisCodeBase(BaseModel):
    code: str
    description: str

class DiagnosisCode(DiagnosisCodeBase):
    id: int
    
    class Config:
        from_attributes = True

# Consultation Schemas
class ConsultationDiagnosisResponse(BaseModel):
    code: str
    description: str
    
    class Config:
        from_attributes = True

class ConsultationCreate(BaseModel):
    patient_name: str
    consultation_date: date
    notes: Optional[str] = None
    diagnosis_codes: List[str]  # List of diagnosis code strings like ["A00", "A01"]

class ConsultationResponse(BaseModel):
    id: int
    patient_name: str
    consultation_date: date
    notes: Optional[str]
    doctor_name: str
    diagnoses: List[ConsultationDiagnosisResponse]
    created_at: datetime
    
    class Config:
        from_attributes = True