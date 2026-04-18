import pandas as pd
from pathlib import Path


def load_data(file_path):
    """
    Load a CSV file into a pandas DataFrame.

    Args:
        file_path (str or Path): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded data.

    Raises:
        FileNotFoundError: If the file does not exist.
        Exception: If the file cannot be loaded.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: File not found at path: {file_path}")
        raise
    except Exception as e:
        print(f"Error loading file: {e}")
        raise


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    file_path = project_root / "data" / "raw" / "sales_data.csv"

    data = load_data(file_path)
    print("Data loaded successfully.")
    print(f"Rows: {data.shape[0]}, Columns: {data.shape[1]}")
    print(data.head())