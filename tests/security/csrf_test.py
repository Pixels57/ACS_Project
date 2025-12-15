import pytest
import requests
import urllib3
import sqlite3
import os
from passlib.context import CryptContext

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
BASE_URL = "http://localhost:8000/api/v1"


@pytest.fixture
def authenticated_session():
    """Helper: Logs in and returns a session with cookies."""

    session = requests.Session()
    # Login credentials
    login_payload = {"email": "student@university.edu", "password": "password123"}
    
    # Note: ensure this matches your API (json vs data)
    resp = session.post(f"{BASE_URL}/auth/login", json=login_payload, verify=False)
    
    if resp.status_code != 200:
        pytest.fail(f"Setup Failed: Could not login. Status: {resp.status_code}. Response: {resp.text}")
        
    return session

def test_csrf_protection_on_enrollment(authenticated_session):
    """
    Test: Attempt a state-changing action (POST) without a CSRF token.
    
    VULNERABLE: Server accepts request (200).
    SECURE: Server rejects request (403/401) due to missing CSRF token.
    """
    # Attempt to enroll in Course ID 1
    # We send the session cookie (automatic), but NO custom CSRF headers.
    payload = {"course_id": 1}
    
    response = authenticated_session.post(
        f"{BASE_URL}/enrollments/", 
        json=payload, 
        verify=False
    )
    
    # Assert that the server BLOCKS this insecure request
    # NOTE: Since we haven't patched CSRF yet, this assertion will FAIL (you will get 200)
    # This proves the vulnerability exists.
    assert response.status_code == 403, \
        f"VULNERABILITY DETECTED: CSRF Attack Succeeded! Expected 403, got {response.status_code}."