from __future__ import annotations

import json
import os
from pathlib import Path

import joblib
import mlflow
import pandas as pd
import yaml
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

try:
    from .features import build_features
except ImportError:  # pragma: no cover - supports `python src/train.py`
    from features import build_features

PARAMS_PATH = Path("params.yaml")
DATA_PATH = Path("data/green_tripdata_2025-01.parquet")
MODEL_PATH = Path("models/model.joblib")
METRICS_PATH = Path("metrics.json")
DEFAULT_TRAIN_PARAMS = {
    "test_size": 0.2,
    "random_state": 42,
    "target_column": "fare_amount",
    "feature_columns": ["vendor_id", "passenger_count", "trip_distance"],
    "model_type": "linear_regression",
}


def load_params(params_path: Path = PARAMS_PATH) -> dict:
    train_params = DEFAULT_TRAIN_PARAMS.copy()
    if params_path.exists():
        with params_path.open("r", encoding="utf-8") as f:
            params = yaml.safe_load(f) or {}
        train_params.update(params.get("train", {}))

    if not train_params["feature_columns"]:
        raise ValueError("feature_columns must not be empty.")
    return train_params


def make_model(model_type: str, random_state: int):
    if model_type == "linear_regression":
        return LinearRegression()
    if model_type == "random_forest":
        return RandomForestRegressor(n_estimators=100, random_state=random_state)
    raise ValueError(f"Unsupported model_type: {model_type}")


def main() -> None:
    train_params = load_params()

    tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
    if tracking_uri:
        mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(
        os.getenv("MLFLOW_EXPERIMENT_NAME", "mle-cicd-clean-27-02-2026-final")
    )

    df = pd.read_parquet(DATA_PATH)

    target_column = str(train_params["target_column"])
    feature_columns = [str(c) for c in train_params["feature_columns"]]
    test_size = float(train_params["test_size"])
    random_state = int(train_params["random_state"])
    model_type = str(train_params["model_type"])

    X, y = build_features(df=df, train_params=train_params)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    model = make_model(model_type=model_type, random_state=random_state)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    rmse = float(mean_squared_error(y_test, predictions) ** 0.5)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    metrics = {
        "rmse": rmse,
        "model_type": model_type,
        "target_column": target_column,
        "feature_columns": feature_columns,
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test)),
    }
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    with mlflow.start_run() as run:
        mlflow.log_params(
            {
                "model_type": model_type,
                "test_size": test_size,
                "random_state": random_state,
                "target_column": target_column,
                "feature_columns": ",".join(feature_columns),
            }
        )
        mlflow.log_metric("rmse", rmse)
        mlflow.log_artifact(str(MODEL_PATH))
        run_id = run.info.run_id

    print(f"MLflow run_id: {run_id}")


if __name__ == "__main__":
    main()
