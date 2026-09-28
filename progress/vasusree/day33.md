# Day 33 — Sept 28 | Vasu Sree | DevOps

## Focus: Dashboard Infrastructure Setup

### Tasks Completed
- Added `fedmed-dashboard` and `fedmed-api` services to docker-compose.yml
- Configured nginx reverse proxy:
  - `/` → React static build (served from dashboard/dist)
  - `/api/` → FastAPI metrics server (port 8000)
  - `/grpc/` → gRPC FL server (port 8080)
- Created `api/metrics_server.py` (FastAPI):
  - `GET /api/metrics` — returns per-round Dice, Loss, epsilon
  - `GET /api/hospitals` — returns hospital node status
  - `GET /api/privacy` — returns privacy budget per round
  - `GET /api/health` — health check
- Wrote `nginx/fedmed.conf` — upstream blocks and proxy_pass rules
- Tested: `docker-compose up` brings all 5 services healthy

### Services Running
| Service           | Port | Status  |
|-------------------|------|---------|
| fedmed-server     | 8080 | Healthy |
| fedmed-client-x3  | —    | Running |
| fedmed-api        | 8000 | Healthy |
| fedmed-dashboard  | 3000 | Healthy |
| fedmed-nginx      | 80   | Up      |

### Tomorrow
- Integrate React dashboard with live API endpoints
