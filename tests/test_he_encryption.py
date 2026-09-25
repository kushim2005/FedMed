"""
tests/test_he_encryption.py
FedMed — Unit tests for Homomorphic Encryption module.

Author: Ranjith Kumar (ML Engineering)
Week 3: HE Test Suite

Tests CKKS context creation, encrypt/decrypt roundtrip fidelity,
server-side encrypted aggregation correctness, key serialization,
and edge cases (zero vectors, large values).

All tests gracefully skip if TenSEAL is not installed.
"""

import os
import tempfile
import pytest
import numpy as np

try:
    import tenseal as ts
    TENSEAL_AVAILABLE = True
except ImportError:
    TENSEAL_AVAILABLE = False

skip_if_no_tenseal = pytest.mark.skipif(
    not TENSEAL_AVAILABLE,
    reason="TenSEAL not installed — skipping HE tests",
)


@pytest.fixture(scope="module")
def ckks_context():
    """Create a shared CKKS context for all tests in this module."""
    if not TENSEAL_AVAILABLE:
        pytest.skip("TenSEAL not available")

    from encryption.tenseal_context import create_ckks_context
    ctx = create_ckks_context(
        poly_mod_degree=8192,
        coeff_mod_bit_sizes=[60, 40, 40, 60],
        global_scale=2 ** 40,
    )
    return ctx


@skip_if_no_tenseal
def test_context_creation():
    """CKKS context should be created with correct parameters."""
    from encryption.tenseal_context import create_ckks_context

    ctx = create_ckks_context(
        poly_mod_degree=8192,
        coeff_mod_bit_sizes=[60, 40, 40, 60],
        global_scale=2 ** 40,
    )
    assert ctx is not None, "Context should not be None"
    assert isinstance(ctx, ts.Context), "Should return a ts.Context instance"


@skip_if_no_tenseal
def test_encrypt_decrypt_roundtrip(ckks_context):
    """Decrypted values should be close to original within CKKS tolerance."""
    from encryption.he_aggregator import encrypt_weights, decrypt_weights

    weights = [
        np.random.randn(32, 1, 3, 3, 3).astype(np.float32),
        np.random.randn(32).astype(np.float32),
        np.random.randn(64, 32, 3, 3, 3).astype(np.float32),
    ]
    shapes = [w.shape for w in weights]

    ciphertexts = encrypt_weights(weights, ckks_context)
    decrypted = decrypt_weights(ciphertexts, shapes, ckks_context)

    assert len(decrypted) == len(weights), "Should decrypt same number of arrays"

    for orig, dec in zip(weights, decrypted):
        l2_error = np.linalg.norm(orig.flatten() - dec.flatten().astype(np.float32))
        assert l2_error < 1.0, (
            f"L2 error {l2_error:.6f} exceeds CKKS tolerance. "
            "CKKS approximation may be too large."
        )


@skip_if_no_tenseal
def test_aggregation_correctness(ckks_context):
    """
    Encrypted weighted average should match plaintext weighted average
    within CKKS approximation tolerance.
    """
    from encryption.he_aggregator import (
        encrypt_weights,
        aggregate_encrypted_weights,
        decrypt_weights,
    )

    num_clients = 3
    shape = (16, 1, 3, 3, 3)
    sample_counts = [100.0, 150.0, 200.0]
    total = sum(sample_counts)
    norms = [s / total for s in sample_counts]

    client_weights = [
        [np.random.randn(*shape).astype(np.float32)]
        for _ in range(num_clients)
    ]

    expected = sum(
        norms[i] * client_weights[i][0] for i in range(num_clients)
    )

    client_ciphertexts = [
        encrypt_weights(w_list, ckks_context) for w_list in client_weights
    ]

    agg_ciphertexts = aggregate_encrypted_weights(
        client_ciphertexts, sample_counts, ckks_context
    )

    decrypted = decrypt_weights(agg_ciphertexts, [shape], ckks_context)
    actual = decrypted[0].astype(np.float32)

    max_abs_error = float(np.max(np.abs(expected - actual)))
    assert max_abs_error < 1e-2, (
        f"Max aggregation error {max_abs_error:.6f} exceeds tolerance. "
        "HE aggregation may have numerical issues."
    )


@skip_if_no_tenseal
def test_key_serialization(ckks_context):
    """Serialized context should deserialize to an equivalent context."""
    from encryption.tenseal_context import (
        save_context,
        load_context,
        get_public_key_bytes,
        context_from_bytes,
    )
    from encryption.he_aggregator import encrypt_weights, decrypt_weights

    with tempfile.TemporaryDirectory() as tmpdir:
        ctx_path = os.path.join(tmpdir, "test_context.tenseal")
        save_context(ckks_context, ctx_path, secret=True)

        assert os.path.exists(ctx_path), "Context file should be saved to disk"
        assert os.path.getsize(ctx_path) > 0, "Context file should not be empty"

        loaded_ctx = load_context(ctx_path)
        assert loaded_ctx is not None, "Loaded context should not be None"

        pub_bytes = get_public_key_bytes(ckks_context)
        assert len(pub_bytes) > 0, "Public key bytes should not be empty"

        pub_ctx = context_from_bytes(pub_bytes)
        assert pub_ctx is not None, "Public context should deserialize correctly"

        weights = [np.random.randn(8).astype(np.float32)]
        ciphertexts = encrypt_weights(weights, pub_ctx)
        decrypted = decrypt_weights(ciphertexts, [weights[0].shape], loaded_ctx)

        l2_err = np.linalg.norm(
            weights[0] - decrypted[0].astype(np.float32)
        )
        assert l2_err < 1.0, (
            f"Cross-context encrypt/decrypt L2 error {l2_err:.6f} too large"
        )


@skip_if_no_tenseal
def test_edge_cases(ckks_context):
    """HE should handle zero vectors, near-zero, and large values."""
    from encryption.he_aggregator import encrypt_weights, decrypt_weights

    zero_vec = np.zeros(64, dtype=np.float32)
    near_zero = np.full(64, 1e-6, dtype=np.float32)
    large_vals = np.full(64, 1e3, dtype=np.float32)

    for label, vec in [
        ("zero", zero_vec),
        ("near_zero", near_zero),
        ("large", large_vals),
    ]:
        cts = encrypt_weights([vec], ckks_context)
        dec = decrypt_weights(cts, [vec.shape], ckks_context)
        l2 = np.linalg.norm(vec - dec[0].astype(np.float32))
        assert l2 < max(1.0, float(np.linalg.norm(vec)) * 1e-3), (
            f"Edge case '{label}': L2 error {l2:.6f} too large"
        )
