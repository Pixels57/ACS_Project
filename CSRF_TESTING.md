# CSRF Protection Testing Guide

This guide explains how to test the CSRF protection implementation.

## Quick Test (Recommended)

### 1. Normal Operation Test (Should Work)

1. **Start the backend:**
   ```powershell
   cd backend
   python main.py
   ```

2. **Start the frontend:**
   ```powershell
   cd frontend
   npm run dev
   ```

3. **Test in browser:**
   - Open `http://localhost:3000`
   - Login to the application
   - Navigate to a course
   - Click "Enroll in this Course"
   - **Expected**: Enrollment succeeds ✅

4. **Verify CSRF token in browser:**
   - Open Developer Tools (F12) → Network tab
   - Find the POST request to `/api/v1/enrollments`
   - Check Request Headers: Should include `X-CSRF-Token: <token>`
   - Check Request Cookies: Should include `csrf_token=<token>`
   - Response should be `200 OK`

---

## Automated PowerShell Test

Run the test script:

```powershell
.\test_csrf_protection.ps1
```

This will test:
- ✅ POST without CSRF token (should fail with 403)
- ✅ POST with valid CSRF token (should succeed)
- ✅ POST with mismatched CSRF token (should fail with 403)
- ✅ POST with token but no cookie (should fail with 403)

---

## Manual Testing Methods

### Test 1: Missing CSRF Token (Should Fail)

**Using PowerShell:**
```powershell
# Try to enroll without CSRF token
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/v1/enrollments" `
    -Method POST `
    -ContentType "application/json" `
    -Body '{"course_id": 1, "student_id": 1}'
```

**Expected Result:** `403 Forbidden` with error: "CSRF token missing in X-CSRF-Token header"

---

### Test 2: Valid CSRF Token (Should Work)

**Using PowerShell:**
```powershell
# Step 1: Get CSRF token
$tokenResponse = Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/v1/csrf-token" `
    -SessionVariable session

$token = ($tokenResponse.Content | ConvertFrom-Json).csrf_token
Write-Host "CSRF Token: $token"

# Step 2: Use the token in enrollment request
$formData = "course_id=1&student_id=1"

Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/v1/enrollments" `
    -Method POST `
    -ContentType "application/x-www-form-urlencoded" `
    -Body $formData `
    -WebSession $session `
    -Headers @{"X-CSRF-Token" = $token}
```

**Expected Result:** `200 OK` with enrollment success message

---

### Test 3: Mismatched CSRF Token (Should Fail)

**Using PowerShell:**
```powershell
# Get a valid token
$tokenResponse = Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/v1/csrf-token" `
    -SessionVariable session

# Try to use a WRONG token
$formData = "course_id=1&student_id=1"

Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/v1/enrollments" `
    -Method POST `
    -ContentType "application/x-www-form-urlencoded" `
    -Body $formData `
    -WebSession $session `
    -Headers @{"X-CSRF-Token" = "wrong-token-12345"}
```

**Expected Result:** `403 Forbidden` with error: "CSRF token mismatch"

---

### Test 4: Browser Console Test

1. Open `http://localhost:3000` in browser
2. Login and open Developer Tools (F12) → Console tab
3. Run this JavaScript:

```javascript
// Test without CSRF token (should fail)
fetch('http://127.0.0.1:8000/api/v1/enrollments', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  credentials: 'include',
  body: JSON.stringify({
    course_id: 1,
    student_id: 1
  })
})
.then(r => r.json())
.then(data => console.log('Response:', data))
.catch(err => console.error('Error:', err));

// Expected: 403 Forbidden - "CSRF token missing in X-CSRF-Token header"
```

4. Test with valid token:

```javascript
// Get CSRF token from cookie
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

const csrfToken = getCookie('csrf_token');
console.log('CSRF Token:', csrfToken);

// Make request with token
if (csrfToken) {
  fetch('http://127.0.0.1:8000/api/v1/enrollments', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'X-CSRF-Token': csrfToken
    },
    credentials: 'include',
    body: 'course_id=1&student_id=1'
  })
  .then(r => r.json())
  .then(data => console.log('Success:', data))
  .catch(err => console.error('Error:', err));
}

// Expected: 200 OK (if not already enrolled)
```

---

### Test 5: Cross-Site CSRF Attack Simulation

1. Open `attacker_site_csrf.html` in your browser (double-click the file)
2. Click "Claim Prize Now!" button
3. **Expected Result:** Request should fail with 403 Forbidden

The attack should be blocked because:
- The CSRF token cookie is not accessible from a different origin
- Even if the cookie was sent, there's no `X-CSRF-Token` header
- The server validates that cookie and header tokens match

---

## Expected Test Results Summary

| Test | Expected Result | Status Code |
|------|----------------|-------------|
| Normal enrollment (browser) | ✅ Success | 200 |
| POST without CSRF token | ❌ Blocked | 403 |
| POST with mismatched token | ❌ Blocked | 403 |
| POST with valid token | ✅ Success | 200 |
| Cross-site form submission | ❌ Blocked | 403 |
| Browser console (no token) | ❌ Blocked | 403 |
| Browser console (with token) | ✅ Success | 200 |

---

## Troubleshooting

### Issue: Getting 500 Internal Server Error
- **Cause**: Backend error, not CSRF validation
- **Fix**: Check backend console logs for actual error

### Issue: CORS errors in browser
- **Cause**: CORS middleware not configured correctly
- **Fix**: Ensure backend is running and CORS is configured in `main.py`

### Issue: Token not being set in cookie
- **Cause**: Cookie attributes blocking cookie
- **Fix**: Check browser console for cookie-related errors. For development, ensure `secure=False` in middleware

### Issue: "CSRF token not available" error
- **Cause**: Token not fetched on app load
- **Fix**: Check browser console. The app should fetch token automatically on load via `App.tsx`

---

## Verification Checklist

- [ ] Normal enrollment works in browser
- [ ] POST without token returns 403
- [ ] POST with wrong token returns 403
- [ ] POST with correct token works
- [ ] Cross-site form submission is blocked
- [ ] Token is set in cookie on GET requests
- [ ] Token is included in header on POST requests
- [ ] CORS headers are present in error responses

---

## Quick Verification Commands

**Check if CSRF endpoint works:**
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/v1/csrf-token" | Select-Object -ExpandProperty Content
```

**Check enrollment without token (should fail):**
```powershell
try {
    Invoke-WebRequest -Uri "http://127.0.0.1:8000/api/v1/enrollments" -Method POST -ContentType "application/json" -Body '{"course_id": 1, "student_id": 1}'
} catch {
    Write-Host "Status: $($_.Exception.Response.StatusCode)"
    Write-Host "Expected: 403 Forbidden"
}
```

---

## Notes

- **Development Mode**: CSRF middleware uses `secure=False` and `samesite="lax"` for testing
- **Production**: Change to `secure=True` and `samesite="strict"` for better security
- **Token Expiry**: Tokens expire after 1 hour (3600 seconds)
- **Exempt Paths**: Auth endpoints (`/api/v1/auth/*`) are exempt from CSRF protection
