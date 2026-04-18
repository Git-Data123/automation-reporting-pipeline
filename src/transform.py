import pandas as pd
from pathlib import Path


def transform_data(df):
    """
    Transform the data and calculate basic metrics.

    Args:
        df (pd.DataFrame): Input validated data.

    Returns:
        pd.DataFrame: Transformed data.
    """
    df = df.copy()
    df["profit"] = df["revenue"] - df["expenses"]
    return df


def calculate_kpis(df):
    """
    Calculate summary KPI values from transformed data.

    Args:
        df (pd.DataFrame): Transformed data.

    Returns:
        dict: Dictionary of KPI values.
    """
    kpis = {
        "total_revenue": int(df["revenue"].sum()),
        "total_expenses": int(df["expenses"].sum()),
        "total_profit": int(df["profit"].sum()),
        "total_records": int(len(df))
    }
    return kpis


def calculate_region_summary(df):
    """
    Calculate KPI summary grouped by region.

    Args:
        df (pd.DataFrame): Transformed data.

    Returns:
        pd.DataFrame: Summary by region.
    """
    region_summary = (
        df.groupby("region")[["revenue", "expenses", "profit"]]
        .sum()
        .reset_index()
    )
    return region_summary


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    file_path = project_root / "data" / "raw" / "sales_data.csv"

    df = pd.read_csv(file_path)

    transformed_df = transform_data(df)
    kpis = calculate_kpis(transformed_df)
    region_summary = calculate_region_summary(transformed_df)

    print("Transformed data:")
    print(transformed_df.head())

    print("\nKPI Summary:")
    print(kpis)

    print("\nRegion Summary:")
    print(region_summary)



def calculate_product_summary(df):
    """
    Calculate KPI summary grouped by product.

    Args:
        df (pd.DataFrame): Transformed data.

    Returns:
        pd.DataFrame: Summary by product.
    """
    product_summary = (
        df.groupby("product")[["revenue", "expenses", "profit"]]
        .sum()
        .reset_index()
    )
    return product_summary