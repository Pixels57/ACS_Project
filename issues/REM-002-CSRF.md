# Remediation Ticket: REM-002 (Cross-Site Request Forgery)

## Vulnerability Description
**Cross-Site Request Forgery (CSRF):** The enrollment endpoint (`/api/v1/enrollments` POST) and other state-changing operations lacked CSRF token validation. This allowed attackers to create malicious websites that could force authenticated users to perform unauthorized actions (e.g., enroll in courses) without their consent. The application relied solely on session cookies for authentication, which browsers automatically include in cross-origin requests.

**Attack Vector:**
- Attacker hosts a malicious website with a hidden form targeting the enrollment endpoint
- Victim visits the malicious site while authenticated
- Browser automatically sends session cookies with the cross-origin POST request
- Backend processes the request without validating the request origin

## Root Cause Analysis
- **Backend:** No CSRF protection middleware. State-changing operations (POST, PUT, DELETE, PATCH) accepted requests without validating a CSRF token.
- **Frontend:** No CSRF token generation or inclusion in requests. API calls did not include anti-CSRF tokens.
- **Cookie Configuration:** Cookies lacked proper `SameSite` attributes to prevent cross-site cookie transmission.

## Implemented Fix

### Backend (`middleware/csrf.py`)
- Implemented **Double Submit Cookie pattern** for CSRF protection:
  - Generates cryptographically secure CSRF tokens using `secrets.token_urlsafe(32)`
  - Sets CSRF token in HTTP-only accessible cookie on GET requests
  - Validates CSRF token on all state-changing methods (POST, PUT, DELETE, PATCH)
  - Requires token to be present in both cookie and `X-CSRF-Token` header
  - Tokens must match between cookie and header (prevents token theft attacks)
- Added CSRF token endpoint (`/api/v1/csrf-token`) for frontend token retrieval
- Configured cookie attributes based on request context:
  - Cross-origin HTTPS: `SameSite=None; Secure=True`
  - Same-origin/HTTP: `SameSite=Lax; Secure=False` (development)
- Exempted authentication endpoints from CSRF (login, logout, token generation)

### Frontend (`api.ts`)
- Added CSRF token management:
  - Automatic token fetching on app initialization (`App.tsx`)
  - Token retrieval from cookie or server endpoint
  - Request interceptor automatically adds `X-CSRF-Token` header to state-changing requests
  - Response interceptor handles token refresh on 403 errors
- Switched to Vite proxy (`/api`) to make requests same-origin, ensuring cookies work correctly
- Updated all API endpoints to use relative paths through proxy

### Frontend (`App.tsx`)
- Added CSRF token initialization on app load
- Ensures token is available before any POST requests

## Verification
- **Manual Test:** `attacker_site.html` - Cross-site form submission should be blocked (403)
- **Browser Test:** Enrollment works normally with valid token, fails without token
- **Network Inspection:** Verify `X-CSRF-Token` header and `csrf_token` cookie are present in POST requests

## Security Improvements
- ✅ All state-changing operations now require CSRF token validation
- ✅ Double Submit Cookie pattern prevents token theft via XSS
- ✅ Token mismatch detection blocks forged requests
- ✅ Proper cookie attributes configured for cross-origin scenarios
- ✅ Automatic token refresh on validation failures

