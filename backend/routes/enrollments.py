"""
Enrollment routes
VULNERABLE: CSRF - No token validation
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.enrollment import Enrollment, EnrollmentStatus
from models.course import Course
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class EnrollmentRequest(BaseModel):
    course_id: int
    student_id: int


@router.post("")
async def create_enrollment(
    enrollment_data: EnrollmentRequest,
    db: Session = Depends(get_db)
    # VULNERABLE: No CSRF token parameter or validation
):
    """
    Create enrollment
    VULNERABLE: CSRF - Missing CSRF token check
    Attack: Malicious website can make POST requests to enroll users
    """
    # Check if course exists
    course = db.query(Course).filter(Course.id == enrollment_data.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Check capacity
    current_enrollments = db.query(Enrollment).filter(
        Enrollment.course_id == enrollment_data.course_id,
        Enrollment.status == EnrollmentStatus.ENROLLED
    ).count()
    
    if current_enrollments >= course.capacity:
        raise HTTPException(status_code=400, detail="Course is full")
    
    # Check if already enrolled
    existing = db.query(Enrollment).filter(
        Enrollment.course_id == enrollment_data.course_id,
        Enrollment.user_id == enrollment_data.student_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Already enrolled")
    
    # Create enrollment
    enrollment = Enrollment(
        course_id=enrollment_data.course_id,
        user_id=enrollment_data.student_id,
        status=EnrollmentStatus.ENROLLED
    )
    
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    
    return {
        "id": enrollment.id,
        "course_id": enrollment.course_id,
        "user_id": enrollment.user_id,
        "status": enrollment.status.value,
        "message": "Enrollment successful"
    }


@router.delete("/{enrollment_id}")
async def drop_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db)
):
    """Drop enrollment"""
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    enrollment.status = EnrollmentStatus.DROPPED
    db.commit()
    
    return {"message": "Enrollment dropped successfully"}


@router.get("")
async def get_enrollments(
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get enrollments"""
    query = db.query(Enrollment)
    
    if user_id:
        query = query.filter(Enrollment.user_id == user_id)
    
    enrollments = query.all()
    
    return [
        {
            "id": e.id,
            "course_id": e.course_id,
            "user_id": e.user_id,
            "status": e.status.value,
            "timestamp": e.timestamp.isoformat()
        }
        for e in enrollments
    ]

