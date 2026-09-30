# FedMed Test Suite

All tests are located in the 	ests/ directory.

## Running Tests

`ash
# HE encryption tests (requires tenseal)
python -m pytest tests/test_he_encryption.py -v

# All tests
python -m pytest tests/ -v --tb=short

# With coverage
python -m pytest tests/ --cov=. --cov-report=term-missing
`

## Test Modules

| Module | Tests | Author |
|--------|-------|--------|
| 	est_he_encryption.py | 5 HE unit tests | Ranjith Kumar |

## CI

All tests run automatically on push via GitHub Actions (.github/workflows/ci.yml).
