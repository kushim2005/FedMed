# Day 31 — Sept 26 | Vasu Sree | DevOps

## Focus: Full Stack HE Integration Validation

### Tasks Completed
- Successfully ran 5 FL rounds with HE-enabled stack (3 hospital containers)
- All CKKS encrypt/aggregate/decrypt operations inside Docker network: zero plaintext weight exposure
- Monitored container resource usage during HE rounds:
  - CPU: 340% (server), 280% (each client) — expected for SEAL operations
  - RAM: 4.2GB (server), 3.8GB (clients) — ciphertext buffer allocation
- Added resource limits to docker-compose: `cpus: 4`, `mem_limit: 6g`
- CI: added container smoke test (5-round HE training) to weekly CI schedule
- Fixed networking: client containers use `server:8080` hostname resolution

### Stack Logs (Round 5 summary)
```
[server] Round 5: Aggregating 3 ciphertexts...
[server] Decrypted global weights. Dice: 0.694
[server] Broadcast complete. Round time: 19.1s
```

### Tomorrow
- Prepare Docker stack for Week 4 (DP-SGD + nginx dashboard proxy)
