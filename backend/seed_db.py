# seed_db.py
from database import SessionLocal, engine
from models.user import User, UserRole
from models.course import Course
import hashlib

def seed():
    db = SessionLocal()
    # 1. Add an Admin/Registrar
    admin = User(
        email="admin@university.edu",
        password_hash=hashlib.md5("admin123".encode()).hexdigest(),
        role=UserRole.ADMIN
    )
    # 2. Add a Student
    student = User(
        email="student@university.edu",
        password_hash=hashlib.md5("password".encode()).hexdigest(),
        role=UserRole.STUDENT
    )
    # 3. Add some Courses
    c1 = Course(code="CS101", title="Intro to Cyber", capacity=30, prereq_ids=[])
    c2 = Course(code="CS102", title="Advanced Hacking", capacity=2, prereq_ids=[])

    db.add_all([admin, student, c1, c2])
    db.commit()
    print("Database Seeded!")

if __name__ == "__main__":
    seed()