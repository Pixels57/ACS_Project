"""
CSRF Protection Middleware
Implements Double Submit Cookie pattern for CSRF protection
"""

import secrets
from fastapi import Request, status
from fastapi.responses import Response, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class CSRFMiddleware(BaseHTTPMiddleware):
    """
    CSRF Protection using Double Submit Cookie pattern
    
    - Generates CSRF token on GET requests and sets it in cookie
    - Validates CSRF token on state-changing methods (POST, PUT, DELETE, PATCH)
    - Requires token in both cookie and X-CSRF-Token header
    """
    
    def __init__(self, app):
        super().__init__(app)
        # State-changing HTTP methods that require CSRF protection
        self.protected_methods = {"POST", "PUT", "DELETE", "PATCH"}
        # Endpoints that don't require CSRF (e.g., auth endpoints)
        self.exempt_paths = {
            "/api/v1/auth/login",
            "/api/v1/auth/logout",
            "/api/v1/auth/token",
            "/api/v1/auth/reset-password",
        }
    
    async def dispatch(self, request: Request, call_next):
        # Skip CSRF for exempt paths
        if request.url.path in self.exempt_paths:
            return await call_next(request)
        
        # Generate CSRF token for GET requests and set it in cookie
        if request.method == "GET":
            response = await call_next(request)
            
            # Generate new CSRF token
            csrf_token = secrets.token_urlsafe(32)
            
            # Detect if request is over HTTPS
            is_https = request.url.scheme == "https"
            
            # Check if this is a cross-origin request (frontend on different origin)
            origin = request.headers.get("origin", "")
            allowed_origins = ["http://localhost:3000", "http://127.0.0.1:3000", "https://localhost:3000", "https://127.0.0.1:3000"]
            is_cross_origin = origin in allowed_origins  # If origin is from frontend, it's cross-origin
            
            # For cross-origin requests over HTTPS, use SameSite=None (requires Secure=True)
            # For same-origin or HTTP, use SameSite=Lax
            if is_cross_origin and is_https:
                samesite_value = "none"
                secure_value = True
            else:
                samesite_value = "lax"
                secure_value = is_https
            
            # Set CSRF token in cookie
            response.set_cookie(
                key="csrf_token",
                value=csrf_token,
                httponly=False,  # Must be accessible to JavaScript for Double Submit pattern
                secure=secure_value,  # True for HTTPS (required with SameSite=None), False for HTTP
                samesite=samesite_value,  # "none" for cross-origin HTTPS, "lax" for same-origin
                max_age=3600,  # 1 hour
                path="/",  # Make cookie available for all paths
            )
            
            # Also include token in response header for easy access
            response.headers["X-CSRF-Token"] = csrf_token
            
            return response
        
        # Validate CSRF token for state-changing methods
        if request.method in self.protected_methods:
            # Get token from cookie
            cookie_token = request.cookies.get("csrf_token")
            
            # Get token from header
            header_token = request.headers.get("X-CSRF-Token")
            
            # Get origin for CORS headers
            origin = request.headers.get("origin", "")
            allowed_origins = ["http://localhost:3000", "http://127.0.0.1:3000", "https://localhost:3000", "https://127.0.0.1:3000"]
            
            # Token must be present in cookie
            if not cookie_token:
                response = JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content={"detail": "CSRF token missing in cookie"}
                )
                if origin in allowed_origins:
                    response.headers["Access-Control-Allow-Origin"] = origin
                    response.headers["Access-Control-Allow-Credentials"] = "true"
                return response
            
            # Token must be present in header
            if not header_token:
                response = JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content={"detail": "CSRF token missing in X-CSRF-Token header"}
                )
                if origin in allowed_origins:
                    response.headers["Access-Control-Allow-Origin"] = origin
                    response.headers["Access-Control-Allow-Credentials"] = "true"
                return response
            
            # Token must match between cookie and header
            if cookie_token != header_token:
                response = JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content={"detail": "CSRF token mismatch"}
                )
                if origin in allowed_origins:
                    response.headers["Access-Control-Allow-Origin"] = origin
                    response.headers["Access-Control-Allow-Credentials"] = "true"
                return response
        
        # Continue with request
        return await call_next(request)


# CSRF token endpoint for frontend to fetch token
from fastapi import APIRouter
csrf_router = APIRouter()

@csrf_router.get("/api/v1/csrf-token")
async def get_csrf_token(request: Request, response: Response):
    """
    Get CSRF token endpoint
    Returns CSRF token that should be included in subsequent requests
    """
    # Generate new CSRF token
    csrf_token = secrets.token_urlsafe(32)
    
    # Detect if request is over HTTPS
    is_https = request.url.scheme == "https"
    
    # Check if this is a cross-origin request (frontend on different origin)
    origin = request.headers.get("origin", "")
    allowed_origins = ["http://localhost:3000", "http://127.0.0.1:3000", "https://localhost:3000", "https://127.0.0.1:3000"]
    is_cross_origin = origin in allowed_origins  # If origin is from frontend, it's cross-origin
    
    # Set CORS headers explicitly to ensure cookie can be set
    if origin in allowed_origins:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Expose-Headers"] = "X-CSRF-Token"
    
    # For cross-origin requests, always use SameSite=None with Secure=True for HTTPS
    # For HTTP cross-origin, we can't use SameSite=None (browsers reject it), so use Lax
    # For same-origin, use Lax
    if is_cross_origin and is_https:
        samesite_value = "none"
        secure_value = True
    elif is_cross_origin and not is_https:
        # Cross-origin HTTP: can't use SameSite=None, must use Lax (but won't work for POST)
        # This is a limitation - for HTTP cross-origin, cookies won't work properly
        samesite_value = "lax"
        secure_value = False
    else:
        samesite_value = "lax"
        secure_value = is_https
    
    # Set token in cookie
    response.set_cookie(
        key="csrf_token",
        value=csrf_token,
        httponly=False,  # Must be accessible to JavaScript
        secure=secure_value,  # True for HTTPS (required with SameSite=None), False for HTTP
        samesite=samesite_value.lower(),  # Convert to lowercase (required by some browsers)
        max_age=3600,  # 1 hour
        path="/",  # Make cookie available for all paths
        domain=None,  # Don't set domain - let browser use default
    )
    
    # Also include token in response header for easy access
    response.headers["X-CSRF-Token"] = csrf_token
    
    return {
        "csrf_token": csrf_token,
        "header_name": "X-CSRF-Token"
    }
