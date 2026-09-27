# Day 32 — Sept 27 | Vasu Sree | DevOps

## Focus: Week 3 Complete + Week 4 DevOps Planning

### Tasks Completed
- Tagged Docker images: `fedmed-server:v3-he`, `fedmed-client:v3-he`
- Pushed images to local registry (Docker Hub push pending public release)
- Updated CI workflow: `.github/workflows/ci.yml` with TenSEAL syntax check
- Week 4 DevOps plan:
  - Add `fedmed-dashboard` service to docker-compose (React + nginx)
  - Add `fedmed-api` service (FastAPI metrics endpoint for dashboard)
  - Configure nginx: `/api` → FastAPI, `/` → React static files
  - Add DP-SGD environment variables: `DP_ENABLED`, `NOISE_MULTIPLIER`, `MAX_GRAD_NORM`
- Reviewed React dashboard mockup from Ravi
- Reserved port 3000 for dashboard in nginx config

### Deliverables
- `docker-compose.yml` — updated with HE volumes and health checks ✅
- `scripts/generate_he_keys.sh` — CKKS key generation script ✅
- CI: TenSEAL syntax check added ✅

### Tomorrow (Week 4)
- Scaffold nginx config for dashboard reverse proxy
