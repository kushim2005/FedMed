"""
security/tls_config.py
Member 3 - Kushi (FL Systems Lead)
Week 2: TLS credential loaders for gRPC server and client channels.
"""
from pathlib import Path
import grpc

CERTS_DIR = Path(__file__).parent / "certs"

_REQUIRED_FILES = [
    "ca.crt",
    "server.key", "server.crt",
    "client_1.key", "client_1.crt",
    "client_2.key", "client_2.crt",
    "client_3.key", "client_3.crt",
]


def certs_exist() -> bool:
    """Return True if all required TLS certificate files are present."""
    return all((CERTS_DIR / f).exists() for f in _REQUIRED_FILES)


def load_server_credentials() -> grpc.ServerCredentials:
    """
    Load TLS credentials for the gRPC FL server.

    Returns:
        grpc.ServerCredentials for use with fl.server.start_server(certificates=...).

    Raises:
        FileNotFoundError: If certificate files are missing.
    """
    if not certs_exist():
        raise FileNotFoundError(
            f"TLS certificates not found in {CERTS_DIR}. "
            "Run: python security/generate_certs.py"
        )
    root_ca = (CERTS_DIR / "ca.crt").read_bytes()
    server_key = (CERTS_DIR / "server.key").read_bytes()
    server_crt = (CERTS_DIR / "server.crt").read_bytes()

    return grpc.ssl_server_credentials(
        [(server_key, server_crt)],
        root_certificates=root_ca,
        require_client_auth=False,
    )


def load_client_credentials(hospital_id: int = 1) -> grpc.ChannelCredentials:
    """
    Load TLS credentials for a hospital client gRPC channel.

    Args:
        hospital_id: Integer (1-3) identifying the hospital node.

    Returns:
        grpc.ChannelCredentials for use with fl.client.start_numpy_client.
    """
    root_ca = (CERTS_DIR / "ca.crt").read_bytes()
    client_key = (CERTS_DIR / f"client_{hospital_id}.key").read_bytes()
    client_crt = (CERTS_DIR / f"client_{hospital_id}.crt").read_bytes()

    return grpc.ssl_channel_credentials(
        root_certificates=root_ca,
        private_key=client_key,
        certificate_chain=client_crt,
    )


def get_root_ca_bytes() -> bytes:
    """Return the raw CA certificate bytes for Flower's root_certificates parameter."""
    return (CERTS_DIR / "ca.crt").read_bytes()
