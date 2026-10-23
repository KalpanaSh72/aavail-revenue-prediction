# AAVAIL Revenue Prediction — Starter Project

Starter scaffold for a time-series revenue-prediction workflow: data ingestion, daily aggregation, model comparison, Flask API, request logging, runtime monitoring, unit tests, and Docker files.

**Not submission-ready yet:** the original AAVAIL course dataset is not included. Add it, verify column names/business rules, fix the placeholder country encoding, create EDA and baseline-comparison plots from the real data, and run the tests/Docker build. Follow Coursera's AI-assistance policy.

## Expected CSV
Put the course data at `data/transactions.csv` with `date`, `country`, and numeric `revenue` columns. Adapt code if the course dataset differs.

## Setup
```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```
Train: `python -m src.train --data data/transactions.csv --output artifacts`
Run API: `python app.py`
Test: `python -m pytest -q` or `scripts/run_tests.sh`
Docker: `docker build -t aavail-revenue-prediction .` then `docker run --rm -p 5000:5000 aavail-revenue-prediction`

POST `/predict` JSON: `{"target_date":"2026-10-01","country":"United Kingdom"}`. Use country `ALL` for combined revenue. GET `/health` and `/metrics` for health/runtime monitoring.
