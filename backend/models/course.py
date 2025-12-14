"""
Course model
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    capacity = Column(Integer, nullable=False)
    prereq_ids = Column(JSON, nullable=True)  # Array of course IDs
    schedule = Column(JSON, nullable=True)  # {days: [], time: "", room: ""}
    instructor_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    instructor = relationship("User", back_populates="courses_taught")
    enrollments = relationship("Enrollment", back_populates="course")

