import requests
import pytest
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "http://localhost:8000/api/v1"

def test_search_is_secure_against_xss_injection():
    """
    Test that the search filter treats input as text, not executable code.
    Passes if: The XSS payload is NOT reflected in the response.
    Fails if: The XSS payload IS found in the response (Vulnerable).
    """
    xss_payload = "<img src=x onerror=alert(1)>"

    # FIX: We use exactly 9 columns (8 NULLs + our payload) to match your DB.
    # The payload is in the 3rd column (index 2) to hit the 'title' field.
    sql_attack = f"' UNION SELECT NULL, NULL, '{xss_payload}', NULL, NULL, NULL, NULL, NULL, NULL --"

    print(f"DEBUG: Sending payload: {sql_attack}")

    response = requests.get(
        f"{BASE_URL}/courses",
        params={"filter": sql_attack},
        verify=False
    )

    # 1. The server should NOT crash (we expect a 200 OK now that columns match)
    assert response.status_code != 500, "Server crashed (500). Column count mismatch likely."
    
    # 2. The security assertion:
    # If the app is VULNERABLE, the payload WILL be there, and this assertion will FAIL.
    assert xss_payload not in response.text, "VULNERABILITY DETECTED: XSS Payload was reflected!"