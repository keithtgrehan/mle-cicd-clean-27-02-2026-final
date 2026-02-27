# MLE CI/CD Pipeline Demo

This repository demonstrates a **minimal Machine Learning Engineering workflow** combining:

- Git + GitHub
- GitHub Actions (CI)
- DVC (Data Version Control)
- Google Cloud Storage (remote data storage)
- pytest for testing
- pre-commit + Black for code formatting

The project is intentionally simple but shows how modern ML pipelines are structured and automated.

---

# Project Structure
├── src/
│   ├── calculator.py
│   ├── features.py
│   └── train.py
│
├── tests/
│   └── test_calculator.py
│
├── data/
│   └── green_tripdata_2025-01.parquet.dvc
│
├── models/
│
├── dvc.yaml
├── params.yaml
├── requirements.txt
├── pytest.ini
├── .pre-commit-config.yaml
└── .github/workflows/test.yml
---

# Core Concepts Demonstrated

## 1. Continuous Integration (CI)

Every push triggers GitHub Actions:
.github/workflows/test.yml
The pipeline:

1. Checkout repository
2. Setup Python
3. Install dependencies
4. Run tests with pytest

This ensures code changes do not break the project.

---

## 2. Code Quality Automation

The repository uses **pre-commit** with **Black** formatting.
.pre-commit-config.yaml
Install locally:
pre-commit install
Run manually:
pre-commit run –all-files
---

## 3. Data Version Control (DVC)

Large datasets are not stored in Git.

Instead:
data/green_tripdata_2025-01.parquet
is tracked with
data/green_tripdata_2025-01.parquet.dvc
The actual data is stored remotely in **Google Cloud Storage**.

---

### Pull dataset
dvc pull
---

### Push dataset
dvc push
---

## 4. Reproducible ML Pipelines

DVC defines a pipeline in:
dvc.yaml
Example stage:
stages:
train:
cmd: python src/train.py
deps:
- src/train.py
- src/features.py
- data/green_tripdata_2025-01.parquet
outs:
- models/model.joblib
Run pipeline:
dvc repro
---

# Environment Setup

Clone repository:
git clone https://github.com/keithtgrehan/mle-cicd-clean-27-02-2026-final.git
cd mle-cicd-clean-27-02-2026-final
Create environment:
python3 -m venv .venv
source .venv/bin/activate
Install dependencies:
pip install -r requirements.txt
Pull dataset:
dvc pull
---

# Run Tests
pytest
---

# Run Pipeline
dvc repro
---

# Verify Code Formatting
pre-commit run –all-files
---

# Typical ML Engineering Workflow
git pull
dvc pull

develop

pytest

run training pipeline

dvc repro

push artifacts

dvc push
git add .
git commit -m “Update pipeline”
git push
---

# What This Project Demonstrates

This repo simulates the **core pieces of a production ML system**:

- reproducible pipelines
- versioned datasets
- automated testing
- CI validation
- code quality enforcement
- cloud data storage

These are foundational tools used in real ML platforms.

---

# Next Possible Extensions

Possible upgrades:

- MLflow experiment tracking
- model registry
- FastAPI inference service
- Docker deployment
- automated retraining pipeline
- feature store integration
- monitoring / drift detection

---

# Author

Keith Grehan  
AI / Machine Learning Engineering Workflow Demo
