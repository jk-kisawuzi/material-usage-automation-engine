import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic cleaning operations for material usage data.
    Adjust this logic to match your real cleaning rules.
    """

    cleaned = df.copy()

    # Example cleaning rules:
    # Remove empty rows
    cleaned = cleaned.dropna(how="all")

    # Strip whitespace from column names
    cleaned.columns = cleaned.columns.str.strip()

    # Fill missing numeric values with 0
    for col in cleaned.select_dtypes(include=["float", "int"]).columns:
        cleaned[col] = cleaned[col].fillna(0)

    return cleaned
