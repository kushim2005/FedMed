# Ravi Day 12 - feat(config): create config/week2_config.yaml

## Tasks Completed
* Created `config/week2_config.yaml` with sections: server, client, data, security, training, evaluation.
* Set `dirichlet_alpha: 0.5`, `num_rounds: 10`, `tls: true`, `min_clients: 2`.
* Shared config with Kushi for server integration.

## Files Modified/Created
* `config/week2_config.yaml` — full Week 2 configuration (50 lines)
* `config/__init__.py` — package init

## Notes & Challenges
* Agreed with Kushi: `min_clients: 2` allows training even if one hospital drops offline.

## Tomorrow's Plan
* Integration test: load partitioned data into fl_client_v2.
