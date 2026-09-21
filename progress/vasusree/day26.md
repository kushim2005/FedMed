# Vasu Sree Day 26 - feat(demo): create demo/week2_demo.py — Docker Compose automated demo

## Tasks Completed
* Created `demo/week2_demo.py`: CLI tool that runs the full Week 2 FL simulation end-to-end.
* Options: `--use-docker` (runs via docker-compose), `--local` (runs Python processes directly).
* Auto-generates certs if missing, validates config, streams live logs from all containers.

## Files Modified/Created
* `demo/week2_demo.py` — 160-line automated demo script

## Notes & Challenges
* Used `subprocess.Popen` for docker-compose process + `threading` for concurrent log streaming.

## Tomorrow's Plan
* Final Docker cleanup: update `.dockerignore`, remove debug artifacts.
