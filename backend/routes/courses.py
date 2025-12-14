"""
Course routes
VULNERABLE: SQL Injection in filter parameter
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text  # VULNERABLE: Using raw SQL
from database import get_db
from models.course import Course
from typing import Optional

router = APIRouter()


@router.get("")
async def get_courses(
    filter: Optional[str] = Query(None, description="Filter courses - VULNERABLE: SQL Injection"),
    db: Session = Depends(get_db)
):
    """
    Get courses with optional filter
    VULNERABLE: SQL Injection - filter parameter is unsanitized
    Example attack: ?filter=1=1 OR 1=1--
    """
    if filter:
        # VULNERABLE: Direct SQL injection - no parameterization
        query = f"SELECT * FROM courses WHERE {filter}"
        result = db.execute(text(query))
        courses = result.fetchall()
        
        # Convert to dict format
        return [
            {
                "id": c[0],
                "code": c[1],
                "title": c[2],
                "description": c[3],
                "capacity": c[4],
                "prereq_ids": c[5],
                "schedule": c[6],
                "instructor_id": c[7]
            }
            for c in courses
        ]
    else:
        # Safe query when no filter
        courses = db.query(Course).all()
        return [
            {
                "id": c.id,
                "code": c.code,
                "title": c.title,
                "description": c.description,
                "capacity": c.capacity,
                "prereq_ids": c.prereq_ids,
                "schedule": c.schedule,
                "instructor_id": c.instructor_id
            }
            for c in courses
        ]


@router.get("/{course_id}")
async def get_course(
    course_id: int,
    db: Session = Depends(get_db)
):
    """Get course details"""
    course = db.query(Course).filter(Course.id == course_id).first()
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    return {
        "id": course.id,
        "code": course.code,
        "title": course.title,
        "description": course.description,
        "capacity": course.capacity,
        "prereq_ids": course.prereq_ids,
        "schedule": course.schedule,
        "instructor_id": course.instructor_id
    }

