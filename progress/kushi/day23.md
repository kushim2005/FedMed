# Kushi Day 23 - docs(pipeline): complete gRPC TLS architecture documentation

## Tasks Completed
* Added mermaid sequence diagram for TLS handshake in `docs/week2_pipeline.md`.
* Documented cert hierarchy: Root CA → Server Cert + 3 Client Certs.
* Added FAQ: "Why self-signed certs?" (development only; production uses Let's Encrypt).

## Files Modified/Created
* `docs/week2_pipeline.md` — TLS handshake sequence diagram + cert hierarchy

## Notes & Challenges
* Mermaid `sequenceDiagram` renders correctly in GitHub markdown.

## Tomorrow's Plan
* Run FedProx vs FedAvg comparison and document convergence difference.
