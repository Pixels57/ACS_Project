Endpoint  Method  Expected Vulnerability
/api/v1/auth/login  POST   Broken Auth (Predictable Session IDs)
/api/v1/courses   GET    SQL Injection (via filter parameter)
/api/v1/enrollments   POST   CSRF (Missing Token)
/api/v1/audit     GET      Broken Access Control (Unauthorized data access)