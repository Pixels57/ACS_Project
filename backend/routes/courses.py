from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models.course import Course
from pydantic import BaseModel

router = APIRouter()

# --- SECURE & ROBUST MODEL ---
# We mark fields as Optional to handle NULL values in the database
# without crashing the API.
class CourseResponse(BaseModel):
    id: int
    title: str
    # Make these Optional so the API doesn't crash if they are NULL in DB
    code: Optional[str] = None
    description: Optional[str] = None
    capacity: Optional[int] = None
    prereq_ids: Optional[str] = None
    schedule: Optional[str] = None
    instructor_id: Optional[int] = None

    class Config:
        orm_mode = True

@router.get("/", response_model=List[CourseResponse])
async def get_courses(
    filter: Optional[str] = Query(None, description="Filter courses by title"),
    db: Session = Depends(get_db)
):
    """
    Get courses with secure filtering.
    PATCHED: Uses SQLAlchemy ORM to prevent SQL Injection.
    """
    try:
        # Start with a secure ORM query builder
        query = db.query(Course)
        
        if filter:
            # SECURITY FIX: .contains() handles escaping automatically
            query = query.filter(Course.title.contains(filter))
        
        return query.all()
    except Exception as e:
        # Debugging: Print the error to the terminal so we know exactly what's wrong
        print(f"ERROR Fetching Courses: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course