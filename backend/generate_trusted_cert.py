"""
Generate trusted HTTPS certificate for secure local development
SECURE: Properly configured certificate with correct CN, valid dates, and proper key size
"""
from cryptography import x509
from cryptography.x509.oid import NameOID, ExtendedKeyUsageOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime
import os
import ipaddress

def generate_trusted_cert():
    """
    Generate a properly configured certificate for localhost:
    1. Valid certificate (not expired, valid for 1 year)
    2. Correct Common Name (localhost and 127.0.0.1)
    3. Self-signed certificate (can be trusted by adding to local CA store)
    4. Strong key size (2048-bit RSA)
    5. Proper signature algorithm (SHA256)
    6. Subject Alternative Names (SAN) for localhost and 127.0.0.1
    """
    # Generate Key - Using 2048-bit RSA (secure)
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    
    # SECURE: Correct Common Name and Subject Alternative Names
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Development"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Local"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Course Registration System"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),  # SECURE: Correct CN
    ])
    
    # SECURE: Valid certificate - valid from now to 1 year from now
    now = datetime.datetime.now(datetime.timezone.utc)
    not_valid_before = now - datetime.timedelta(days=1)  # Allow 1 day clock skew
    not_valid_after = now + datetime.timedelta(days=365)  # Valid for 1 year
    
    # SECURE: SHA256 signature algorithm
    signature_algorithm = hashes.SHA256()
    
    # Build certificate with Subject Alternative Names (SAN)
    # This allows the certificate to work with both localhost and 127.0.0.1
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        not_valid_before
    ).not_valid_after(
        not_valid_after
    ).add_extension(
        x509.SubjectAlternativeName([
            x509.DNSName(u"localhost"),
            x509.DNSName(u"127.0.0.1"),
            x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
            x509.IPAddress(ipaddress.IPv6Address("::1")),
        ]),
        critical=False,
    ).add_extension(
        x509.ExtendedKeyUsage([
            ExtendedKeyUsageOID.SERVER_AUTH,
        ]),
        critical=False,
    ).add_extension(
        x509.KeyUsage(
            key_encipherment=True,
            digital_signature=True,
            key_agreement=False,
            key_cert_sign=False,
            crl_sign=False,
            content_commitment=False,
            data_encipherment=False,
            encipher_only=False,
            decipher_only=False,
        ),
        critical=True,
    ).sign(key, signature_algorithm)
    
    # Write certificate and key files
    cert_path = os.path.join(os.path.dirname(__file__), "cert.pem")
    key_path = os.path.join(os.path.dirname(__file__), "key.pem")
    
    with open(key_path, "wb") as f:
        f.write(key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption()
        ))
    
    with open(cert_path, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    
    print("[+] SECURE: Trusted certificate generated with:")
    print("    - Valid dates (valid for 1 year)")
    print("    - Correct Common Name (localhost)")
    print("    - Subject Alternative Names (localhost, 127.0.0.1, ::1)")
    print("    - Strong key size (2048-bit RSA)")
    print("    - Secure signature algorithm (SHA256)")
    print(f"[+] Certificate saved to: {cert_path}")
    print(f"[+] Key saved to: {key_path}")
    print()
    print("[!] To trust this certificate in your system:")
    print("    Windows: Import cert.pem into 'Trusted Root Certification Authorities'")
    print("    macOS: Keychain Access -> Add cert.pem -> Trust -> Always Trust")
    print("    Linux: Copy cert.pem to /usr/local/share/ca-certificates/ and run update-ca-certificates")
    print()
    print("[!] Alternative: Use mkcert for automatic local CA setup:")
    print("    Install: https://github.com/FiloSottile/mkcert")
    print("    Run: mkcert -install")
    print("    Then: mkcert localhost 127.0.0.1")

if __name__ == "__main__":
    generate_trusted_cert()

