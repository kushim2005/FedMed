# Kushi Day 19 - feat(server): add server health-check ping endpoint

## Tasks Completed
* Added a `threading.Thread` running a lightweight HTTP health-check server on port 8090.
* Endpoint: `GET http://localhost:8090/health` → `{"status": "running", "round": N}`.
* Docker health check can now probe this endpoint.

## Files Modified/Created
* `server/fl_server_v2.py` — `_start_health_check()` method (30 lines)

## Notes & Challenges
* Used `http.server.HTTPServer` in a daemon thread; doesn't block FL server startup.

## Tomorrow's Plan
* Profile server memory usage during aggregation.
