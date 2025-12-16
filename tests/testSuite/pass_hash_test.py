import sqlite3
import pytest
import os

# UPDATE THIS to match your actual database filename
DB_PATH = "../../backend/course_registration.db" 

def test_passwords_use_strong_hashing():
    """
    Verify that passwords are using STRONG hashing (Bcrypt).
    Fails if Plaintext OR Weak Hashing (MD5/SHA1) is detected.
    """
    if not os.path.exists(DB_PATH):
        pytest.skip(f"Database not found at {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT password_hash FROM users WHERE email = 'student@university.edu'")
        result = cursor.fetchone()

        if not result:
            pytest.fail("Test user not found.")

        stored_password = result[0]
        print(f"DEBUG: Stored Hash: {stored_password}")

        # 1. Check for Plaintext
        if stored_password == "student123":
            pytest.fail("VULNERABILITY: Password is stored in Plaintext.")

        # 2. Check for MD5 (Weak)
        # MD5 hashes are exactly 32 hex characters long and have no $ prefix
        if len(stored_password) == 32 and "$" not in stored_password:
             pytest.fail(f"VULNERABILITY: Weak Hashing (MD5) detected! Hash: {stored_password}")

        # 3. Verify it is Bcrypt (The Goal)
        assert stored_password.startswith("$2b$") or stored_password.startswith("$2a$"), \
            f"Password is not securely hashed with Bcrypt. Found: {stored_password}"

    finally:
        conn.close()