# Vasu Sree Day 23 - perf(docker): optimize Docker image using python:3.10-slim base

## Tasks Completed
* Changed `FROM python:3.10` to `FROM python:3.10-slim` in Dockerfile.
* Added `--no-cache-dir --compile` to pip install for smaller site-packages.
* Image size reduced: 2.1 GB → 1.4 GB (33% reduction).

## Files Modified/Created
* `Dockerfile` — slim base + optimized pip install

## Notes & Challenges
* slim image missing `gcc` — had to add `RUN apt-get install -y gcc` for MONAI compilation.

## Tomorrow's Plan
* Performance test: 10 FL rounds timing in optimized Docker containers.
