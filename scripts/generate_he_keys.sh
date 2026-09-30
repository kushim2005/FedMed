#!/usr/bin/env bash
# generate_he_keys.sh — Generate CKKS context for FedMed HE.
# Author: Vasu Sree (DevOps)
set -e
echo "[FedMed] Generating CKKS keys (128-bit security)..."
mkdir -p keys
python -c "
from encryption.tenseal_context import create_ckks_context, save_context, get_public_key_bytes
ctx = create_ckks_context()
save_context(ctx, 'keys/ckks_context.tenseal', secret=True)
pub = get_public_key_bytes(ctx)
with open('keys/ckks_public.tenseal', 'wb') as f:
    f.write(pub)
print('[FedMed] Keys generated: keys/ckks_context.tenseal, keys/ckks_public.tenseal')
"
echo "[FedMed] CKKS context ready."
