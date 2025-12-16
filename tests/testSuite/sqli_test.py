import requests
import pytest
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "http://localhost:8000/api/v1"

def test_sql_injection_logic_bypass():
    """
    Test for SQL Injection logic bypass.
    
    VULNERABLE Behavior: Returns ALL courses (logic is True).
    SECURE Behavior: Returns 0 results (text search finds nothing).
    """
    
    # 1. Get baseline count (e.g., 5 courses)
    initial_resp = requests.get(f"{BASE_URL}/courses", verify=False)
    total_courses_count = len(initial_resp.json())
    
    if total_courses_count == 0:
        pytest.skip("Database is empty. Add courses to test SQLi.")

    # 2. The Corrected Payload
    # The backend is: LIKE '%{filter}%'
    # We inject: XYZ' OR '1'='1' --
    # Result: ... LIKE '%XYZ' OR '1'='1' --%'
    # The -- comments out the trailing %' so the logic holds valid.
    sqli_payload = "XYZ' OR '1'='1' --"
    
    attack_resp = requests.get(
        f"{BASE_URL}/courses", 
        params={"filter": sqli_payload},
        verify=False
    )
    
    results = attack_resp.json()
    
    # 3. Security Assertion
    # If vulnerable, we get ALL courses back.
    # The test fails if len(results) > 0.
    assert len(results) == 0, (
        f"VULNERABILITY DETECTED: SQL Injection successful. "
        f"Expected 0 results, but got {len(results)}. "
        "The database logic was bypassed."
    )