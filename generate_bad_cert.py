from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime
import ipaddress

def generate_legit_looking_cert():
    # Generate Key
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    # Subject and Issuer
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Giza"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Advanced Cyber Security Project"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),
    ])

    # Subject Alternative Names (CRITICAL FOR STABILITY)
    san = x509.SubjectAlternativeName([
        x509.DNSName(u"localhost"),
        x509.DNSName(u"127.0.0.1"),
        x509.IPAddress(ipaddress.IPv4Address(u"127.0.0.1")),
    ])

    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=365)
    ).add_extension(
        san, critical=False
    ).sign(key, hashes.SHA256())

    # Write files
    with open("key.pem", "wb") as f:
        f.write(key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.TraditionalOpenSSL, serialization.NoEncryption()))
    with open("cert.pem", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

    print("[+] High-quality SAN certificate generated.")

if __name__ == "__main__":
    generate_legit_looking_cert()