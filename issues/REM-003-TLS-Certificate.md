# Remediation Ticket: REM-003 (TLS Certificate Misconfiguration)

## Vulnerability Description
**TLS Certificate Misconfiguration:** The backend was using a misconfigured self-signed certificate with multiple security issues:
1. **Expired Certificate** - Certificate validity expired 6 months ago, making it invalid
2. **Wrong Common Name** - Certificate CN was `wrong-domain.example.com` instead of `localhost`
3. **Self-Signed Certificate** - No proper certificate authority validation
4. **Missing Subject Alternative Names** - Certificate didn't include SANs for `127.0.0.1` and `::1`

This caused browsers to display security warnings, prevented proper hostname verification, and could allow man-in-the-middle attacks if users bypassed warnings. The misconfigured certificate also prevented proper TLS validation in automated tools and clients.

## Root Cause Analysis
- **Backend:** Certificate generation script (`generate_misconfigured_cert.py`) intentionally created certificates with security misconfigurations for vulnerability demonstration
- **Certificate Attributes:** Expired validity dates, incorrect Common Name, and missing SANs
- **No Certificate Trust:** Certificate was not trusted in system certificate stores, causing browser warnings

## Implemented Fix

### Backend (`generate_trusted_cert.py`)
- Created new certificate generation script with proper configuration:
  - **Valid Certificate** - Valid from current date to 1 year in the future
  - **Correct Common Name** - CN set to `localhost` (matches server hostname)
  - **Subject Alternative Names (SAN)** - Includes `localhost`, `127.0.0.1`, and `::1` for IPv4 and IPv6
  - **Strong Key Size** - 2048-bit RSA key (secure)
  - **Secure Signature Algorithm** - SHA256 (cryptographically secure)
  - **Proper Key Usage** - Server authentication extensions configured correctly
- Certificate now properly validates hostname and works with all localhost variants

### Backend (`main.py`)
- Updated to use `generate_trusted_cert.py` instead of misconfigured certificate generator
- Automatic certificate generation if files don't exist
- Clear messaging indicating secure certificate configuration

### Frontend (`vite.config.js`)
- Added HTTPS support for frontend when using `npm run dev:https`
- Automatically uses backend certificate files for frontend HTTPS
- Proper certificate loading with file system checks

## Verification
- **Test:** `backend/test_certificate_trust.py` (Should PASS - SSL handshake successful)
- **Browser Test:** Visit `https://localhost:8000` - Should show green lock (secure) with no warnings
- **Frontend Test:** Run `npm run dev:https` - Frontend should also show secure connection
- **Certificate Details:** Verify certificate has correct CN, valid dates, and SANs
- **Hostname Verification:** Certificate validates correctly for `localhost`, `127.0.0.1`, and `::1`

