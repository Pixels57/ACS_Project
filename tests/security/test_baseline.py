import requests

BASE_URL = "http://localhost:8000"

def test_check_sql_injection_vulnerability():
    # Attempt an SQLi bypass. If successful, it returns 200 (Success).
    # In a secure app, this should return a 400 or 500 error.
    payload = "1=1 OR 1=1"
    response = requests.get(f"{BASE_URL}/api/v1/courses?filter={payload}")
    assert response.status_code == 200
    print("PHASE 1: SQL Injection verified as present.")

def test_check_unauthorized_audit_access():
    # Audit logs should be secret. If we can see them, it's a bug.
    response = requests.get(f"{BASE_URL}/api/v1/audit")
    assert response.status_code == 200
    print("PHASE 1: Unauthorized Audit Access verified.")