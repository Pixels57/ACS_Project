"""
Course Registration System - Main Application
Monolithic FastAPI backend with intentional security vulnerabilities
"""

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Import routes
from routes import auth, courses, enrollments, admin, audit

# Import database setup
from database import init_db

app = FastAPI(
    title="Course Registration System API",
    description="Vulnerable course registration system for security assessment",
    version="1.0.0"
)

# CORS configuration - intentionally permissive for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # VULNERABLE: Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(courses.router, prefix="/api/v1/courses", tags=["Courses"])
app.include_router(enrollments.router, prefix="/api/v1/enrollments", tags=["Enrollments"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])
app.include_router(audit.router, prefix="/api/v1/audit", tags=["Audit"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Course Registration System API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Database initialization
@app.on_event("startup")
async def startup_event():
    init_db()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload on code changes
    )

