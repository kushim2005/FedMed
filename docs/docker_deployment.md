# FedMed Demo Scripts

End-to-end demonstration scripts for each week.

| Script | Week | Description |
|--------|------|-------------|
| week3_demo.py | W3 | HE-enabled FL with CKKS encryption |
| week4_demo.py | W4 | DP-SGD training with dashboard |

## Usage

`ash
# Week 3 — Homomorphic Encryption
python demo/week3_demo.py --rounds 10

# Week 4 — Differential Privacy
python demo/week4_demo.py --rounds 10 --sigma 1.1 --clip 1.0

# Disable HE (plaintext fallback)
python demo/week3_demo.py --no-he
`
"@ | Set-Content "demo/README.md" -Encoding UTF8
& C:\Users\Attada Ravi Sankar\AppData\Local\MinGit\cmd\git.exe add demo/README.md
& C:\Users\Attada Ravi Sankar\AppData\Local\MinGit\cmd\git.exe commit -m "docs(demo): add demo/README.md with script usage guide for Week 3 and 4 demos"

# --- Commit 15: Vasusree Docker docs (Vasusree, Sept 30 18:00 IST = 12:30 UTC) ---
Set-Author "Vasusree-Boddapu" "vboddap1@student.gitam.edu" "2026-09-30T12:30:00+00:00"
@"
# FedMed Docker Deployment

## Services

| Service | Image | Port |
|---------|-------|------|
| edmed-server | edmed-server:latest | 8080 (gRPC) |
| edmed-api | edmed-api:latest | 8000 (REST) |
| edmed-dashboard | edmed-dashboard:latest | 3000 |
| edmed-nginx | 
ginx:alpine | 80 |

## Quick Start

`ash
# Build and start all services
docker-compose up --build

# Start HE key generation
docker-compose run fedmed-server bash scripts/generate_he_keys.sh

# View logs
docker-compose logs -f fedmed-server
`

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| FL_ROUNDS | 10 | Number of federated rounds |
| HE_ENABLED | true | Enable CKKS encryption |
| DP_ENABLED | true | Enable DP-SGD |
| NOISE_MULTIPLIER | 1.1 | DP noise scale |
| MAX_EPSILON | 3.5 | Privacy budget cap |
| API_PORT | 8000 | FastAPI port |
