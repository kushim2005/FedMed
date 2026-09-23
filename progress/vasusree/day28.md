# Day 28 — Sept 23 | Vasu Sree | DevOps

## Focus: Week 2 Deployment Review + Week 3 Infrastructure Planning

### Tasks Completed
- Final Week 2 deployment review: all containers healthy, CI green on main branch
- Week 3 DevOps planning:
  - TenSEAL build requirements: cmake >= 3.15, ninja-build, libgmp-dev
  - Multi-stage Docker build plan: builder (compiles SEAL) + runtime (copies wheel)
  - Estimated build time: 8–12 min (SEAL C++ compilation from source)
  - CKKS key volume: shared Docker volume for context.tenseal files
- Researched TenSEAL Docker images: no official image — must build from scratch
- Created `Dockerfile.he` draft: 3-stage build (deps → build → runtime)
- Updated docker-compose plan: added `he_context` named volume
- Checked CI: TenSEAL installation adds ~3 min to CI lint job → use import guard

### Docker Image Size Estimate
| Stage       | Base         | Size  |
|-------------|--------------|-------|
| builder     | python:3.10  | 1.8GB |
| runtime     | python:3.10-slim | 890MB |
| final (HE)  | python:3.10-slim + tenseal | 1.1GB |

### Tomorrow
- Implement Dockerfile.he multi-stage build
- Test TenSEAL import inside runtime container
