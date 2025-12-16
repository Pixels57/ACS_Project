from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from database import get_db
from models.enrollment import Enrollment, EnrollmentStatus
from models.course import Course
from typing import Optional

router = APIRouter()

"""
Enrollment routes
PROTECTED: CSRF token validation via middleware
"""

@router.post("")
async def create_enrollment(
    course_id: int = Form(...),
    student_id: int = Form(...),
    db: Session = Depends(get_db)
):
    """
    Create enrollment
    Protected by CSRF middleware - requires valid CSRF token in header
    """
    # Verify course exists
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Check if already enrolled
    existing = db.query(Enrollment).filter(
        Enrollment.course_id == course_id,
        Enrollment.user_id == student_id
    ).first()
    
    if existing and existing.status == EnrollmentStatus.ENROLLED:
         return {"message": "Already enrolled"}

    # Create Enrollment
    enrollment = Enrollment(
        course_id=course_id,
        user_id=student_id,
        status=EnrollmentStatus.ENROLLED
    )
    db.add(enrollment)
    db.commit()
    return {"message": "Enrollment successful"}

@router.delete("/{enrollment_id}")
async def drop_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db)
):
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