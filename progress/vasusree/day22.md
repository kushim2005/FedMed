# Vasu Sree Day 22 - docs(review): mid-project DevOps review — Docker performance

## Tasks Completed
* Presented Docker simulation results to team: 38 min for 10 rounds, TLS stable, no OOM.
* Docker image sizes: `fl_server:latest` = 2.3 GB, `hospital_client:latest` = 2.1 GB.
* Action item from review: optimize image size by switching to `python:3.10-slim`.

## Files Modified/Created
* `docs/docker_performance_report.md` — Docker simulation analysis

## Notes & Challenges
* Team agreed: switching to slim base image is priority for Week 3 cloud deployment.

## Tomorrow's Plan
* Optimize Docker image: switch to `python:3.10-slim` base.
