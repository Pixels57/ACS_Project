"""
Test script to verify the trusted certificate is working correctly
"""
import requests
import ssl
import socket
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from datetime import datetime

def test_certificate():
    """Test the certificate in various ways"""
    import os
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cert_path = os.path.join(script_dir, "cert.pem")
    
    print("=" * 60)
    print("Certificate Trust Test")
    print("=" * 60)
    print()
    
    # Test 1: Read and display certificate details
    print("[1] Certificate Details:")
    print("-" * 60)
    try:
        with open(cert_path, "rb") as f:
            cert = x509.load_pem_x509_certificate(f.read(), default_backend())
            
        print(f"Subject: {cert.subject}")
        print(f"Issuer: {cert.issuer}")
        print(f"Valid from: {cert.not_valid_before}")
        print(f"Valid until: {cert.not_valid_after}")
        print(f"Serial number: {cert.serial_number}")
        
        # Check if certificate is currently valid
        now = datetime.now(cert.not_valid_before.tzinfo)
        if cert.not_valid_before <= now <= cert.not_valid_after:
            print("[OK] Certificate is currently valid")
        else:
            print("[FAIL] Certificate is NOT valid (expired or not yet valid)")
            
        # Check Common Name
        cn = None
        for attr in cert.subject:
            if attr.oid == x509.oid.NameOID.COMMON_NAME:
                cn = attr.value
                break
        
        if cn == "localhost":
            print("[OK] Common Name is correct (localhost)")
        else:
            print(f"[FAIL] Common Name is incorrect: {cn}")
            
    except Exception as e:
        print(f"[ERROR] Error reading certificate: {e}")
    
    print()
    
    # Test 2: Test HTTPS connection with requests (should work if trusted)
    print("[2] HTTPS Connection Test:")
    print("-" * 60)
    try:
        # First try without verify=False (should work if trusted)
        response = requests.get('https://localhost:8000', timeout=5)
        print(f"[OK] HTTPS connection successful!")
        print(f"  Status code: {response.status_code}")
        print(f"  Certificate validation: PASSED (certificate is trusted)")
    except requests.exceptions.SSLError as e:
        print(f"[FAIL] SSL Error: {e}")
        print("  Certificate may not be trusted. Check certificate store.")
    except requests.exceptions.ConnectionError:
        print("[WARNING] Connection refused - Backend server is not running")
        print("  Start the server with: python main.py")
    except Exception as e:
        print(f"[ERROR] Error: {e}")
    
    print()
    
    # Test 3: Test with SSL context
    print("[3] SSL Context Test:")
    print("-" * 60)
    try:
        context = ssl.create_default_context()
        with socket.create_connection(('localhost', 8000), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname='localhost') as ssock:
                cert = ssock.getpeercert()
                print(f"[OK] SSL handshake successful!")
                print(f"  Server certificate verified")
                print(f"  Protocol: {ssock.version()}")
    except ssl.SSLError as e:
        print(f"[FAIL] SSL Error: {e}")
        print("  Certificate validation failed")
    except ConnectionRefusedError:
        print("[WARNING] Connection refused - Backend server is not running")
    except Exception as e:
        print(f"[ERROR] Error: {e}")
    
    print()
    print("=" * 60)
    print("Test Complete")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Start the backend: python main.py")
    print("2. Visit https://localhost:8000 in your browser")
    print("3. Should see secure connection (green lock) with no warnings")

if __name__ == "__main__":
    test_certificate()

