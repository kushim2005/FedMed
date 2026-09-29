# Day 34 — Sept 29 | Vasu Sree | DevOps

## Focus: Dashboard Deployment + CI Integration

### Tasks Completed
- Configured React build pipeline inside Docker:
  - `node:20-alpine` build stage: `npm ci && npm run build`
  - `nginx:alpine` runtime stage: copies `dist/` to `/usr/share/nginx/html`
  - Final image size: 48MB (optimized)
- Added dashboard deployment to CI workflow:
  - `.github/workflows/ci.yml`: added `dashboard-build` job (runs `npm ci && npm run build`)
  - Verifies React build succeeds on every push
- Health check for dashboard container: `curl -f http://localhost:3000`
- Tested full stack with live DP-SGD training:
  - Dashboard updates every 5s via polling `/api/metrics`
  - Epsilon bar chart fills in real-time as rounds complete
- Fixed CORS: FastAPI `allow_origins=["http://localhost:3000"]`

### Docker Build Time
- Dashboard image build: 42s (node_modules cached via Docker layer)
- Total stack `docker-compose up --build`: 3m 12s

### Tomorrow
- Final stack testing + documentation
