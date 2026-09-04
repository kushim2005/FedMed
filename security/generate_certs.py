"""
security/generate_certs.py
Member 3 - Kushi (FL Systems Lead)
Week 2: Generate TLS certificates for secure gRPC communication between
        the central FL server and hospital client nodes.

Usage:
    python security/generate_certs.py

Generates:
    security/certs/ca.key, ca.crt           -- Root Certificate Authority
    security/certs/server.key, server.crt   -- FL Server certificate
    security/certs/client_{1,2,3}.key/.crt  -- Per-hospital client certificates
"""
import datetime
from pathlib import Path

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa

CERTS_DIR = Path(__file__).parent / "certs"
VALIDITY_CA_DAYS = 3650   # 10 years for CA
VALIDITY_CERT_DAYS = 365  # 1 year for server/client certs


def _generate_rsa_key() -> rsa.RSAPrivateKey:
    """Generate a 2048-bit RSA private key."""
    return rsa.generate_private_key(public_exponent=65537, key_size=2048)


def generate_ca_cert():
    """Generate a self-signed Root CA certificate and private key."""
    ca_key = _generate_rsa_key()
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "IN"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "FedMed Root CA"),
        x509.NameAttribute(NameOID.COMMON_NAME, "FedMed CA"),
    ])
    ca_cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(ca_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=VALIDITY_CA_DAYS))
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .sign(ca_key, hashes.SHA256())
    )
    return ca_key, ca_cert


def generate_signed_cert(ca_key, ca_cert, common_name: str):
    """Generate a certificate signed by the CA for a given common name."""
    key = _generate_rsa_key()
    subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "IN"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "FedMed"),
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
    ])
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(ca_cert.subject)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=VALIDITY_CERT_DAYS))
        .add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.DNSName("fl-server"),
                x509.DNSName(common_name),
            ]),
            critical=False,
        )
        .sign(ca_key, hashes.SHA256())
    )
    return key, cert


def save_cert(name: str, key, cert) -> None:
    """Save private key and certificate as PEM files in CERTS_DIR."""
    CERTS_DIR.mkdir(parents=True, exist_ok=True)

    key_path = CERTS_DIR / f"{name}.key"
    with open(key_path, "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))

    cert_path = CERTS_DIR / f"{name}.crt"
    with open(cert_path, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

    print(f"  ✅  Saved: {key_path.name}, {cert_path.name}")


def generate_all_certs(num_hospitals: int = 3) -> None:
    """Generate CA, server, and client certificates for all hospital nodes."""
    print("🔐 FedMed — Generating TLS Certificates")
    print(f"   Output directory: {CERTS_DIR.resolve()}\n")

    # --- Root CA ---
    ca_key, ca_cert = generate_ca_cert()
    save_cert("ca", ca_key, ca_cert)

    # --- FL Server ---
    server_key, server_cert = generate_signed_cert(ca_key, ca_cert, "fl-server")
    save_cert("server", server_key, server_cert)

    # --- Hospital Clients ---
    for i in range(1, num_hospitals + 1):
        client_key, client_cert = generate_signed_cert(ca_key, ca_cert, f"hospital-{i}")
        save_cert(f"client_{i}", client_key, client_cert)

    print(f"\n🎉  All certificates generated in: {CERTS_DIR.resolve()}")
    print("    Run `python server/fl_server_v2.py` to start the TLS-secured FL server.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="FedMed TLS Certificate Generator")
    parser.add_argument("--num-hospitals", type=int, default=3,
                        help="Number of hospital client certificates to generate (default: 3)")
    args = parser.parse_args()
    generate_all_certs(args.num_hospitals)
