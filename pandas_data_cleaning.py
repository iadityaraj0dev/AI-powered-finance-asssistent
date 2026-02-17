"""Simple pandas-based data cleaning utility.

Usage:
    python pandas_data_cleaning.py input.csv output.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd



def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned copy of the input DataFrame."""
    cleaned = df.copy()

    # Normalize column names
    cleaned.columns = (
        cleaned.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    # Drop exact duplicate rows
    cleaned = cleaned.drop_duplicates()

    # Trim whitespace for text columns
    text_columns = cleaned.select_dtypes(include=["object", "string"]).columns
    for col in text_columns:
        cleaned[col] = cleaned[col].astype("string").str.strip()

    # Try converting likely date columns
    for col in cleaned.columns:
        if "date" in col or col.endswith("_at"):
            cleaned[col] = pd.to_datetime(cleaned[col], errors="coerce")

    # Convert numeric-like text values to numbers when possible
    for col in cleaned.columns:
        if cleaned[col].dtype == "string" or cleaned[col].dtype == object:
            numeric_version = pd.to_numeric(cleaned[col], errors="coerce")
            if numeric_version.notna().sum() > 0:
                # Keep numeric conversion if at least half of non-null values converted
                original_non_null = cleaned[col].notna().sum()
                if original_non_null > 0 and numeric_version.notna().sum() >= original_non_null / 2:
                    cleaned[col] = numeric_version

    # Fill missing values: median for numeric, mode for text
    numeric_columns = cleaned.select_dtypes(include=["number"]).columns
    for col in numeric_columns:
        cleaned[col] = cleaned[col].fillna(cleaned[col].median())

    text_columns = cleaned.select_dtypes(include=["object", "string"]).columns
    for col in text_columns:
        mode_values = cleaned[col].mode(dropna=True)
        if not mode_values.empty:
            cleaned[col] = cleaned[col].fillna(mode_values.iloc[0])

    # Drop rows where every value is missing
    cleaned = cleaned.dropna(how="all")

    return cleaned



def run(input_csv: Path, output_csv: Path) -> None:
    df = pd.read_csv(input_csv)
    cleaned = clean_dataframe(df)
    cleaned.to_csv(output_csv, index=False)



def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Clean CSV data with pandas.")
    parser.add_argument("input_csv", type=Path, help="Path to the raw input CSV file")
    parser.add_argument("output_csv", type=Path, help="Path to write cleaned CSV output")
    return parser



if __name__ == "__main__":
    args = build_parser().parse_args()
    run(args.input_csv, args.output_csv)
