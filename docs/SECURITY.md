# FedMed Security Model

## Threat Model

FedMed assumes the **honest-but-curious** server model:
- The FL server faithfully executes the aggregation protocol
- But attempts to learn private patient information from client updates
- Hospital clients are fully trusted
- Network adversaries can observe ciphertext traffic

## Security Guarantees

| Layer | Technology | Guarantee |
|-------|-----------|-----------|
| Transport | TLS 1.3 + mTLS | Authenticated encrypted channel |
| Weight Privacy | CKKS HE | Server never sees plaintext weights |
| Training Privacy | DP-SGD | (ε=2.79, δ=1e-5)-differential privacy |

## Key Management

- CKKS secret key: generated once, stored only at trusted coordinator
- CKKS public key: distributed to all hospital clients
- TLS certificates: RSA-2048, signed by FedMed CA (security/generate_certs.py)
- Never commit keys to Git — keys/ is gitignored

## Privacy Parameters

- Noise multiplier σ = 1.1 (Gaussian DP-SGD noise)
- Clipping norm C = 1.0 (per-sample gradient bound)
- Delta δ = 1e-5 (privacy failure probability)
- Epsilon ε ≤ 2.79 (achieved after 10 rounds)
