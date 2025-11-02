from sqlalchemy import Column, Integer, String, Text, Date, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

# for our database.

# todo: implement doctor login when able
# otherwise start with default doctor
class Doctor(Base):
    __tablename__ = "doctors"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    consultations = relationship("Consultation", back_populates="doctor")

# 1 A00 "Desc here" 473847
class DiagnosisCode(Base):
    __tablename__ = "diagnosis_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # parent is ConsultationDiagnosis
    consultation_diagnoses = relationship("ConsultationDiagnosis", back_populates="diagnosis_code")

class Consultation(Base):
    __tablename__ = "consultations"
    
    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id", ondelete="CASCADE"))
    patient_name = Column(String(255), nullable=False)
    consultation_date = Column(Date, nullable=False)
    notes = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    doctor = relationship("Doctor", back_populates="consultations")
    # if consultation is deleted, delete all related consultationdiagnosis to it
    diagnoses = relationship("ConsultationDiagnosis", back_populates="consultation", cascade="all, delete-orphan")

class ConsultationDiagnosis(Base):
    __tablename__ = "consultation_diagnoses"
    
    id = Column(Integer, primary_key=True, index=True)
    consultation_id = Column(Integer, ForeignKey("consultations.id", ondelete="CASCADE"))
    diagnosis_code_id = Column(Integer, ForeignKey("diagnosis_codes.id", ondelete="CASCADE"))
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    consultation = relationship("Consultation", back_populates="diagnoses")
    diagnosis_code = relationship("DiagnosisCode", back_populates="consultation_diagnoses")