import argparse
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate numeric features parquet.")
    parser.add_argument("input_path", help="Input parquet dataset path.")
    parser.add_argument("output_path", help="Output parquet feature dataset path.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    df = pd.read_parquet(args.input_path)

    features_df = df.select_dtypes(include="number").dropna().reset_index(drop=True)
    if features_df.empty:
        raise ValueError("Feature dataset is empty after numeric selection and dropna.")

    output_path = Path(args.output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    features_df.to_parquet(output_path, index=False)


if __name__ == "__main__":
    main()
