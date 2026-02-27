# MLE CI + DVC Demo

This repository demonstrates:
- GitHub Actions CI
- DVC data pull/push with a GCS remote
- `pytest` test execution
- `pre-commit` with Black formatting checks

## Project Structure

```text
.
├── .github/workflows/
│   ├── black.yml
│   ├── cml.yaml
│   ├── metrics-pr.yml
│   └── test.yml
├── data/
│   ├── .gitkeep
│   ├── green_tripdata_2025-01.parquet
│   └── green_tripdata_2025-01.parquet.dvc
├── models/
│   ├── .gitignore
│   └── model.joblib.dvc
├── src/
│   ├── __init__.py
│   ├── calculator.py
│   ├── features.py
│   └── train.py
├── tests/
│   └── test_calculator.py
├── .pre-commit-config.yaml
├── dvc.lock
├── dvc.yaml
├── params.yaml
├── requirements.txt
└── README.md
```

## CI (GitHub Actions)

Active workflow files:
- `.github/workflows/test.yml` (runs `pytest`)
- `.github/workflows/black.yml` (runs `black --check .`)
- `.github/workflows/metrics-pr.yml` (posts DVC metrics diff on PRs)

## pre-commit + Black

Configuration file: `.pre-commit-config.yaml`

```bash
pre-commit install
pre-commit run --all-files
```

## DVC Data Tracking

Dataset file:
- `data/green_tripdata_2025-01.parquet`

DVC metafile:
- `data/green_tripdata_2025-01.parquet.dvc`

Use these commands to sync data with remote storage:

```bash
dvc pull
dvc push
```

## Reproducible ML Pipeline

After pulling data, run the training stage with DVC:

```bash
dvc repro
```

Pipeline outputs:
- model: `models/model.joblib`
- metrics: `metrics.json`

## Setup (Fresh Clone)

```bash
git clone https://github.com/keithtgrehan/mle-cicd-clean-27-02-2026-final.git
cd mle-cicd-clean-27-02-2026-final
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
dvc pull
pytest
pre-commit run --all-files
```
## MLOps Upgrades

- **MLflow experiment tracking**: `src/train.py` logs params, RMSE, and `models/model.joblib` to local MLflow runs (`mlruns/`).
- **PR metrics diff**: `.github/workflows/metrics-pr.yml` runs DVC + tests on pull requests and comments a metrics markdown report with CML.
- **DVC-tracked model artifact**: `models/model.joblib` is tracked via `models/model.joblib.dvc`.

Run locally:

```bash
dvc pull
dvc repro
pytest
pre-commit run --all-files
mlflow ui --backend-store-uri ./mlruns
# optional: compare metrics against main
dvc metrics diff --md origin/main
```
