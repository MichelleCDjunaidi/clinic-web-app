from pydantic import field_validator, ConfigDict, BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import date, datetime

# Auth Schemas
class DoctorBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=255, description="Doctor's full name")

class DoctorCreate(DoctorBase):
    password: str = Field(..., min_length=8, max_length=72, description="Password must be 8-72 characters")
    
    @field_validator('password')
    @classmethod
    def password_strength(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isalpha() for char in v):
            raise ValueError('Password must contain at least one letter')
        return v
    
    @field_validator('full_name')
    @classmethod
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty or just whitespace')
        return v.strip()

class Doctor(DoctorBase):
    id: int
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1, description="Password is required")

# Diagnosis Schemas
class DiagnosisCodeBase(BaseModel):
    code: str = Field(..., min_length=2, max_length=10, description="ICD-10 code")
    description: str = Field(..., min_length=1, max_length=500, description="Diagnosis description")

class DiagnosisCode(DiagnosisCodeBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

# Consultation Schemas
class ConsultationDiagnosisResponse(BaseModel):
    code: str
    description: str
    model_config = ConfigDict(from_attributes=True)

class ConsultationCreate(BaseModel):
    patient_name: str = Field(
        ..., 
        min_length=2, 
        max_length=255, 
        description="Patient's full name"
    )
    consultation_date: date = Field(..., description="Date of consultation")
    notes: Optional[str] = Field(
        None, 
        max_length=5000, 
        description="Consultation notes"
    )
    diagnosis_codes: List[str] = Field(
        ..., 
        min_length=1, 
        max_length=20,
        description="List of ICD-10 diagnosis codes"
    )
    
    @field_validator('patient_name')
    @classmethod
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Patient name cannot be empty or just whitespace')
        return v.strip()
    
    @field_validator('consultation_date')
    @classmethod
    def date_not_future(cls, v):
        if v > date.today():
            raise ValueError('Consultation date cannot be in the future')
        return v
    
    @field_validator('diagnosis_codes')
    @classmethod
    def codes_must_be_valid_format(cls, v):
        for code in v:
            if not code or not code.strip():
                raise ValueError('Diagnosis codes cannot be empty')
            if len(code.strip()) < 2 or len(code.strip()) > 10:
                raise ValueError(f'Invalid diagnosis code format: {code}')
        # Remove duplicates while preserving order
        seen = set()
        unique_codes = []
        for code in v:
            code_upper = code.strip().upper()
            if code_upper not in seen:
                seen.add(code_upper)
                unique_codes.append(code_upper)
        return unique_codes

class ConsultationResponse(BaseModel):
    id: int
    patient_name: str
    consultation_date: date
    notes: Optional[str] = None
    doctor_name: str
    diagnoses: List[ConsultationDiagnosisResponse]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)