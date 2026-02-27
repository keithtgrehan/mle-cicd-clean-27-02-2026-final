from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
import yaml
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

from .features import build_features

PARAMS_PATH = Path("params.yaml")
DATA_PATH = Path("data/green_tripdata_2025-01.parquet")
MODEL_PATH = Path("models/model.joblib")
METRICS_PATH = Path("metrics.json")


def load_params(params_path: Path = PARAMS_PATH) -> dict:
    with params_path.open("r", encoding="utf-8") as f:
        params = yaml.safe_load(f) or {}
    train = params.get("train", {})
    required = {
        "test_size",
        "random_state",
        "target_column",
        "feature_columns",
        "model_type",
    }
    missing = required - set(train.keys())
    if missing:
        raise ValueError(f"Missing required train params: {sorted(missing)}")
    return train


def make_model(model_type: str, random_state: int):
    if model_type == "linear_regression":
        return LinearRegression()
    if model_type == "random_forest":
        return RandomForestRegressor(n_estimators=100, random_state=random_state)
    raise ValueError(f"Unsupported model_type: {model_type}")


def main() -> None:
    train_params = load_params()
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


if __name__ == "__main__":
    main()
