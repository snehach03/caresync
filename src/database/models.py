from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, DateTime, Time, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from .connection import Base

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String, nullable=False)
    role = Column(String, nullable=False) # 'patient' or 'caregiver'
    timezone = Column(String, nullable=False, default="UTC")
    created_at = Column(DateTime(timezone=True), server_default="CURRENT_TIMESTAMP")

class Medication(Base):
    __tablename__ = "medications"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    name = Column(String, nullable=False)
    dosage = Column(String, nullable=False)
    frequency = Column(String)
    instructions = Column(Text)
    is_active = Column(Boolean, default=True)

class Schedule(Base):
    __tablename__ = "schedules"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    medication_id = Column(UUID(as_uuid=True), ForeignKey("medications.id", ondelete="CASCADE"))
    scheduled_time = Column(Time, nullable=False)
    day_of_week = Column(Integer)

class DoseLog(Base):
    __tablename__ = "dose_logs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    schedule_id = Column(UUID(as_uuid=True), ForeignKey("schedules.id", ondelete="CASCADE"))
    taken_at = Column(DateTime(timezone=True), nullable=False)
    status = Column(String) # 'taken', 'missed', 'skipped'
    notes = Column(Text)

class Checkin(Base):
    __tablename__ = "checkins"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    mood_score = Column(Integer)
    notes = Column(Text)
    recorded_at = Column(DateTime(timezone=True), server_default="CURRENT_TIMESTAMP")

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    title = Column(String, nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    location = Column(Text)

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    caregiver_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    type = Column(String) # 'missed_dose', 'health_warning'
    message = Column(Text, nullable=False)
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default="CURRENT_TIMESTAMP")
