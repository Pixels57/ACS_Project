from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from database import get_db
from models.enrollment import Enrollment, EnrollmentStatus
from models.course import Course
# from pydantic import BaseModel # Not used in vulnerable version

router = APIRouter()

# --- VULNERABLE STATE: No CSRF Check, Accepts Form Data ---

@router.post("")
async def create_enrollment(
    course_id: int = Form(...),    # VULNERABLE: Accepts simple Form Data
    student_id: int = Form(...),   # VULNERABLE: Accepts simple Form Data
    db: Session = Depends(get_db)
    # MISSING: No csrf_check dependency here!
):
    """
    VULNERABLE ENROLLMENT
    - App (Frontend) sends Form Data -> WORKS
    - Attacker (HTML Form) sends Form Data -> WORKS (CSRF)
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
    user_id: int = None,
    db: Session = Depends(get_db)
):
    query = db.query(Enrollment)
    if user_id:
        query = query.filter(Enrollment.user_id == user_id)
    return query.all()