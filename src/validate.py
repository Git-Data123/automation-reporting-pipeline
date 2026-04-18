import pandas as pd
from pathlib import Path


def validate_data(df):
    """
    Validate the input DataFrame for required structure and data quality.

    Args:
        df (pd.DataFrame): Input data.

    Returns:
        bool: True if validation passes.

    Raises:
        ValueError: If validation fails.
    """
    required_columns = ["date", "region", "product", "revenue", "expenses"]

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    if df[required_columns].isnull().any().any():
        raise ValueError("Data contains missing values in required columns.")

    try:
        df["revenue"] = pd.to_numeric(df["revenue"])
        df["expenses"] = pd.to_numeric(df["expenses"])
    except Exception:
        raise ValueError("Revenue and expenses must be numeric.")

    try:
        df["date"] = pd.to_datetime(df["date"])
    except Exception:
        raise ValueError("Date column contains invalid dates.")

    if (df["revenue"] < 0).any():
        raise ValueError("Revenue contains negative values.")

    if (df["expenses"] < 0).any():
        raise ValueError("Expenses contains negative values.")

    return True


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    file_path = project_root / "data" / "raw" / "sales_data.csv"

    df = pd.read_csv(file_path)
    result = validate_data(df)
    print("Validation passed:", result)