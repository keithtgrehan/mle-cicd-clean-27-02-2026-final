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
│   └── test.yml
├── data/
│   ├── .gitkeep
│   ├── green_tripdata_2025-01.parquet
│   └── green_tripdata_2025-01.parquet.dvc
├── src/
│   ├── __init__.py
│   ├── calculator.py
│   ├── features.py
│   └── train.py
├── tests/
│   └── test_calculator.py
├── .pre-commit-config.yaml
├── requirements.txt
└── README.md
```

## CI (GitHub Actions)

Active workflow files:
- `.github/workflows/test.yml` (runs `pytest`)
- `.github/workflows/black.yml` (runs `black --check .`)

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
## Reproducible ML pipeline (DVC)

This repo includes a minimal ML training pipeline managed by **DVC**.

### What it does
- pulls the dataset with DVC
- trains a simple sklearn model
- writes:
  - `models/model.joblib` (the trained model)
  - `metrics.json` (evaluation metrics)

### Run it locally

```bash
# 1) Create env + install deps
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt

# 2) Pull data from the DVC remote
dvc pull

# 3) Run tests + formatting
pytest
pre-commit run --all-files

# 4) Run the training pipeline (reproducible)
dvc repro
