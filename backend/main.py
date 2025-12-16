"""
Course Registration System - Main Application
Monolithic FastAPI backend with intentional security vulnerabilities
"""

import asyncio
import sys
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Import routes
from routes import auth, courses, enrollments, admin, audit

# Import CSRF middleware
from middleware.csrf import CSRFMiddleware, csrf_router

# Import database setup
from database import init_db

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
app = FastAPI(
    title="Course Registration System API",
    description="Vulnerable course registration system for security assessment",
    version="1.0.0"
)

# CORS configuration - intentionally permissive for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "https://localhost:3000", "https://127.0.0.1:3000"],  # VULNERABLE: Allows specific origins (can't use "*" with credentials)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "X-CSRF-Token"],  # Allow CSRF token header
)

# CSRF Protection Middleware
# Note: Must be added after CORS middleware
app.add_middleware(CSRFMiddleware)

# Include routers
app.include_router(csrf_router)  # CSRF token endpoint
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(courses.router, prefix="/api/v1/courses", tags=["Courses"])
app.include_router(enrollments.router, prefix="/api/v1/enrollments", tags=["Enrollments"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])
app.include_router(audit.router, prefix="/api/v1/audit", tags=["Audit"])

# VULNERABLE: Debug routes that expose sensitive information
from routes import debug
app.include_router(debug.router, prefix="/api/v1/debug", tags=["Debug"])


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
    import os
    import sys
    
    # Check if HTTP mode is requested (for network analysis/testing)
    use_http = os.getenv("USE_HTTP", "false").lower() == "true" or "--http" in sys.argv
    
    if use_http:
        # VULNERABLE: Running on HTTP (unencrypted) for network analysis
        # This makes it easy to demonstrate data exposure with Wireshark
        print("[!] VULNERABLE: Running on HTTP (unencrypted)")
        print("    All data transmitted in plaintext - visible in network traffic")
        print("    Use this mode for network analysis with Wireshark/Burp Suite")
        print()
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,  # HTTP port (unencrypted)
            reload=True
        )
    else:
        # SECURE: HTTPS with trusted certificate
        # Certificate is properly configured:
        # 1. Valid certificate (valid for 1 year)
        # 2. Correct Common Name (localhost)
        # 3. Subject Alternative Names (localhost, 127.0.0.1, ::1)
        # 4. Strong key size (2048-bit RSA)
        # 5. Secure signature algorithm (SHA256)
        cert_path = os.path.join(os.path.dirname(__file__), "cert.pem")
        key_path = os.path.join(os.path.dirname(__file__), "key.pem")
        
        # Check if certificates exist, if not, generate trusted certificate
        if not os.path.exists(cert_path) or not os.path.exists(key_path):
            print("[!] Certificate files not found. Generating trusted certificate...")
            from generate_trusted_cert import generate_trusted_cert
            generate_trusted_cert()
        
        # Run with HTTPS using trusted certificate
        print("[+] SECURE: Running on HTTPS with trusted certificate")
        print("    Certificate is valid, correct CN, and properly configured")
        print("    Note: If browser shows warning, add cert.pem to trusted root CAs")
        print("    For network analysis, use: USE_HTTP=true python main.py")
        print()
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,  # HTTPS port
            ssl_keyfile=key_path,
            ssl_certfile=cert_path,
            reload=True  # Auto-reload on code changes
        )

