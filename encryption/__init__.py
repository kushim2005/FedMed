"""FedMed Encryption Module — Homomorphic Encryption via TenSEAL CKKS scheme."""

from encryption.tenseal_context import (
    create_ckks_context,
    save_context,
    load_context,
    get_public_key_bytes,
)
from encryption.he_aggregator import aggregate_encrypted_weights

__all__ = [
    "create_ckks_context",
    "save_context",
    "load_context",
    "get_public_key_bytes",
    "aggregate_encrypted_weights",
]
