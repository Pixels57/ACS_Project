# Remediation Ticket: REM-001 (SQL Injection & Reflected XSS)

## Vulnerability Description
1. **SQL Injection:** The course search endpoint (`/courses?filter=`) accepted raw user input and concatenated it directly into a SQL query string (`f"SELECT... LIKE {filter}"`). This allowed attackers to manipulate database queries.
2. **Reflected XSS:** The frontend displayed the search query using `dangerouslySetInnerHTML`, allowing malicious JavaScript scripts injected via the URL to execute in the user's browser.

## Root Cause Analysis
- **Backend:** Lack of input sanitization and use of raw SQL execution instead of parameterized queries.
- **Frontend:** Unsafe rendering of user-controlled data using dangerous React properties.

## Implemented Fix
- **Backend (`courses.py`):** Replaced raw SQL execution with **SQLAlchemy ORM**. The ORM automatically handles input escaping and parameterization.
- **Frontend (`Courses.tsx`):** Removed `dangerouslySetInnerHTML`. React now escapes all output by default.
- **Frontend (`api.ts`):** Stopped sending SQL fragments from the client. The client now sends raw text, and the backend handles the query logic.

## Verification
- **Test:** `tests/security/test_vuln_sqli_only.py` (Should PASS)
- **Test:** `tests/security/reflected_xss.py` (Should PASS)