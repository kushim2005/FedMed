"""
encryption/he_aggregator.py
FedMed — Server-side Homomorphic Encryption aggregation.

Author: Ravi (Integration Lead)
Week 3: Encrypted Federated Averaging

Implements weighted FedAvg aggregation directly over CKKS ciphertexts.
The server never sees plaintext weights — aggregation is performed entirely
in the encrypted domain using TenSEAL homomorphic operations.

Protocol:
  1. Each client encrypts: w_i → Enc(w_i) using shared public key
  2. Server computes: Enc(sum_i p_i * w_i) / sum_i p_i (homomorphically)
  3. Secret key holder decrypts aggregated global weights
"""

import base64
import logging
from typing import List, Tuple

import numpy as np

try:
    import tenseal as ts
    TENSEAL_AVAILABLE = True
except ImportError:
    TENSEAL_AVAILABLE = False

logger = logging.getLogger(__name__)


def encrypt_weights(
    weights: List[np.ndarray],
    context: "ts.Context",
) -> List[bytes]:
    """
    Encrypt a list of weight vectors using CKKS scheme.

    Each numpy array in weights is flattened, cast to float64, and
    encrypted as a CKKS vector. The result is serialized to bytes
    for transport.

    Args:
        weights: List of numpy arrays (model layer weights).
        context: TenSEAL CKKS context (must contain public key).

    Returns:
        List of serialized ciphertext bytes, one per weight array.
    """
    if not TENSEAL_AVAILABLE:
        raise ImportError("TenSEAL required. pip install tenseal==0.3.14")

    ciphertexts = []
    for w in weights:
        flat = w.flatten().astype(np.float64).tolist()
        enc = ts.ckks_vector(context, flat)
        ciphertexts.append(enc.serialize())

    logger.debug("Encrypted %d weight tensors", len(ciphertexts))
    return ciphertexts


def decrypt_weights(
    ciphertext_bytes: List[bytes],
    shapes: List[tuple],
    context: "ts.Context",
) -> List[np.ndarray]:
    """
    Decrypt a list of CKKS ciphertext bytes back to numpy weight arrays.

    Args:
        ciphertext_bytes: List of serialized ciphertext bytes.
        shapes: Original shapes for each weight tensor.
        context: TenSEAL CKKS context (must contain secret key).

    Returns:
        List of numpy arrays with the decrypted weight values.
    """
    if not TENSEAL_AVAILABLE:
        raise ImportError("TenSEAL required. pip install tenseal==0.3.14")

    results = []
    for ct_bytes, shape in zip(ciphertext_bytes, shapes):
        vec = ts.ckks_vector_from(context, ct_bytes)
        decrypted = np.array(vec.decrypt(), dtype=np.float32)
        results.append(decrypted[: int(np.prod(shape))].reshape(shape))

    logger.debug("Decrypted %d weight tensors", len(results))
    return results


def aggregate_encrypted_weights(
    client_ciphertexts: List[List[bytes]],
    client_weights: List[float],
    context: "ts.Context",
) -> List[bytes]:
    """
    Perform weighted FedAvg aggregation over encrypted client weights.

    Computes the homomorphic weighted average:
        Enc(w_global) = sum_i(p_i * Enc(w_i)) / sum(p_i)

    where p_i is the number of samples at client i. The server never
    decrypts individual client weights during aggregation.

    Args:
        client_ciphertexts: List of per-client ciphertext lists.
            client_ciphertexts[i] is the encrypted weight list from client i.
        client_weights: Proportional weights (e.g., num_samples per client).
            Will be normalized internally.
        context: TenSEAL CKKS context with at least public key and
            relinearization/Galois keys (no secret key required).

    Returns:
        List of serialized aggregated ciphertext bytes, one per layer.

    Raises:
        ValueError: If client count or layer count is inconsistent.
    """
    if not TENSEAL_AVAILABLE:
        raise ImportError("TenSEAL required. pip install tenseal==0.3.14")

    if len(client_ciphertexts) != len(client_weights):
        raise ValueError(
            f"Expected {len(client_weights)} clients, "
            f"got {len(client_ciphertexts)} ciphertext lists"
        )

    if len(client_ciphertexts) == 0:
        raise ValueError("No client ciphertexts provided for aggregation")

    total_weight = sum(client_weights)
    if total_weight <= 0:
        raise ValueError("Sum of client weights must be positive")

    normalized = [w / total_weight for w in client_weights]
    num_layers = len(client_ciphertexts[0])

    aggregated = []
    for layer_idx in range(num_layers):
        aggregated_vec = None

        for client_idx, (ct_list, norm_w) in enumerate(
            zip(client_ciphertexts, normalized)
        ):
            if len(ct_list) != num_layers:
                raise ValueError(
                    f"Client {client_idx} has {len(ct_list)} layers, "
                    f"expected {num_layers}"
                )

            vec = ts.ckks_vector_from(context, ct_list[layer_idx])
            scaled_vec = vec * norm_w

            if aggregated_vec is None:
                aggregated_vec = scaled_vec
            else:
                aggregated_vec += scaled_vec

        aggregated.append(aggregated_vec.serialize())

    logger.info(
        "HE aggregation complete: %d clients, %d layers",
        len(client_ciphertexts),
        num_layers,
    )
    return aggregated


def ciphertexts_to_ndarray(ciphertexts: List[bytes]) -> np.ndarray:
    """
    Encode a list of ciphertext bytes as a numpy byte array for Flower transport.

    Flower's FitRes expects numpy NDArrays. This packs each ciphertext
    as a base64 string stored in a numpy array of bytes.

    Args:
        ciphertexts: List of serialized CKKS ciphertext bytes.

    Returns:
        numpy array of shape (N,) with dtype=object, each element a
        base64-encoded ciphertext string.
    """
    encoded = [base64.b64encode(ct).decode("ascii") for ct in ciphertexts]
    return np.array(encoded, dtype=object)


def ndarray_to_ciphertexts(arr: np.ndarray) -> List[bytes]:
    """
    Decode a numpy byte array back to a list of ciphertext bytes.

    Reverses ciphertexts_to_ndarray for server-side deserialization.

    Args:
        arr: numpy array of base64-encoded ciphertext strings.

    Returns:
        List of raw ciphertext bytes for TenSEAL deserialization.
    """
    return [base64.b64decode(item.encode("ascii")) for item in arr.tolist()]
