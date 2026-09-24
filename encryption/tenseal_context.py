"""
encryption/tenseal_context.py
FedMed — CKKS homomorphic encryption context management.

Author: Kushi (FL Systems)
Week 3: Homomorphic Encryption Layer

Provides creation, serialization, and loading of TenSEAL CKKS contexts.
The CKKS scheme supports approximate arithmetic on encrypted float vectors,
making it ideal for federated learning weight aggregation.

Security: 128-bit IND-CPA under RLWE assumption.
Parameters: poly_mod_degree=8192, coeff_mod=[60,40,40,60], scale=2^40
"""

import os
import logging
from typing import Optional

try:
    import tenseal as ts
    TENSEAL_AVAILABLE = True
except ImportError:
    TENSEAL_AVAILABLE = False

logger = logging.getLogger(__name__)


def create_ckks_context(
    poly_mod_degree: int = 8192,
    coeff_mod_bit_sizes: Optional[list] = None,
    global_scale: float = 2 ** 40,
) -> "ts.Context":
    """
    Create a TenSEAL CKKS context with the given parameters.

    Args:
        poly_mod_degree: Polynomial modulus degree. Must be a power of 2.
            Higher values increase capacity but reduce performance.
            Default 8192 gives 128-bit security.
        coeff_mod_bit_sizes: Coefficient modulus bit sizes for each level.
            Default [60, 40, 40, 60] supports 2 multiplication levels.
        global_scale: Scale factor for encoding. Default 2^40 balances
            precision and range.

    Returns:
        ts.Context: Fully initialized CKKS context with public + secret keys.

    Raises:
        ImportError: If TenSEAL is not installed.
    """
    if not TENSEAL_AVAILABLE:
        raise ImportError(
            "TenSEAL is required for homomorphic encryption. "
            "Install with: pip install tenseal==0.3.14"
        )

    if coeff_mod_bit_sizes is None:
        coeff_mod_bit_sizes = [60, 40, 40, 60]

    context = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=poly_mod_degree,
        coeff_mod_bit_sizes=coeff_mod_bit_sizes,
    )
    context.global_scale = global_scale
    context.generate_galois_keys()
    context.generate_relin_keys()

    logger.info(
        "CKKS context created: poly_mod=%d, scale=2^%.0f, levels=%d",
        poly_mod_degree,
        40,
        len(coeff_mod_bit_sizes) - 1,
    )
    return context


def save_context(context: "ts.Context", path: str, secret: bool = True) -> None:
    """
    Serialize and save a TenSEAL context to disk.

    Args:
        context: The TenSEAL CKKS context to save.
        path: File path to write the serialized context.
        secret: If True, saves with secret key. Set False to export
            public-key-only context for distribution to clients.
    """
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)

    if secret:
        serialized = context.serialize(save_secret_key=True)
    else:
        public_ctx = context.copy()
        public_ctx.make_context_public()
        serialized = public_ctx.serialize()

    with open(path, "wb") as f:
        f.write(serialized)

    key_type = "secret+public" if secret else "public-only"
    logger.info("Saved %s context to %s (%d bytes)", key_type, path, len(serialized))


def load_context(path: str) -> "ts.Context":
    """
    Load a TenSEAL context from disk.

    Args:
        path: File path to the serialized context.

    Returns:
        ts.Context: Deserialized CKKS context.

    Raises:
        FileNotFoundError: If the context file does not exist.
    """
    if not TENSEAL_AVAILABLE:
        raise ImportError("TenSEAL is required. pip install tenseal==0.3.14")

    if not os.path.exists(path):
        raise FileNotFoundError(f"CKKS context file not found: {path}")

    with open(path, "rb") as f:
        data = f.read()

    context = ts.context_from(data)
    logger.info("Loaded CKKS context from %s", path)
    return context


def get_public_key_bytes(context: "ts.Context") -> bytes:
    """
    Extract the public-key-only context as bytes for distribution to clients.

    The returned bytes contain only the public key and evaluation keys
    (Galois, relinearization). The secret key is not included.

    Args:
        context: Full CKKS context (with secret key).

    Returns:
        bytes: Serialized public-key-only context.
    """
    public_ctx = context.copy()
    public_ctx.make_context_public()
    return public_ctx.serialize()


def context_from_bytes(data: bytes) -> "ts.Context":
    """
    Deserialize a CKKS context from raw bytes.

    Args:
        data: Serialized context bytes (e.g., received over the network).

    Returns:
        ts.Context: Deserialized CKKS context.
    """
    if not TENSEAL_AVAILABLE:
        raise ImportError("TenSEAL is required. pip install tenseal==0.3.14")
    return ts.context_from(data)
