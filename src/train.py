import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
import yaml
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a linear regression model.")
    parser.add_argument("input_path", help="Path to engineered features parquet file.")
    parser.add_argument("model_output", help="Path to output model pickle file.")
    parser.add_argument("metrics_output", help="Path to output metrics JSON file.")
    parser.add_argument(
        "--params-path",
        default="params.yaml",
        help="Path to parameters YAML file.",
    )
    return parser.parse_args()


def load_train_params(params_path: str) -> tuple[float, int]:
    params_file = Path(params_path)
    if not params_file.exists():
        return 0.2, 42

    with params_file.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    train_config = config.get("train", {})
    test_size = float(train_config.get("test_size", 0.2))
    random_state = int(train_config.get("random_state", 42))
    return test_size, random_state


def choose_target_column(df: pd.DataFrame) -> str:
    preferred_targets = ("fare_amount", "target", "label", "y")
    for column in preferred_targets:
        if column in df.columns:
            return column
    return str(df.columns[-1])


def main() -> None:
    args = parse_args()
    df = pd.read_parquet(args.input_path)

    if df.shape[1] < 2:
        raise ValueError("Expected at least two numeric columns to train a model.")

    target_column = choose_target_column(df)
    feature_columns = [column for column in df.columns if column != target_column]

    if not feature_columns:
        raise ValueError("No feature columns remain after selecting target column.")

    X = df[feature_columns]
    y = df[target_column]
    test_size, random_state = load_train_params(args.params_path)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    rmse = float(mean_squared_error(y_test, y_pred) ** 0.5)

    model_output_path = Path(args.model_output)
    model_output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "model": model,
            "target_column": target_column,
            "feature_columns": feature_columns,
        },
        model_output_path,
    )

    metrics_output_path = Path(args.metrics_output)
    metrics_output_path.parent.mkdir(parents=True, exist_ok=True)
    with metrics_output_path.open("w", encoding="utf-8") as f:
        json.dump({"rmse": rmse}, f, indent=2)


if __name__ == "__main__":
    main()
