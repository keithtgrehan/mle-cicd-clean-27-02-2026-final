from __future__ import annotations

import pandas as pd


def build_features(
    df: pd.DataFrame, train_params: dict
) -> tuple[pd.DataFrame, pd.Series]:
    """Return model matrix X and target y based on training parameters."""
    target_column = str(train_params["target_column"])
    feature_columns = [str(c) for c in train_params["feature_columns"]]

    missing = [c for c in [target_column, *feature_columns] if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    data = df[[*feature_columns, target_column]].copy()
    data = data.dropna(subset=[target_column])
    data = data.dropna(subset=feature_columns)

    if data.empty:
        raise ValueError(
            "No rows remain after dropping missing values for features/target."
        )

    X = data[feature_columns]
    y = data[target_column]
    return X, y
