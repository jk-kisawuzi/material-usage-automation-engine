import pandas as pd

def load_file(file_path):
    """Load Excel file into a DataFrame."""
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        raise ValueError(f"Error loading file: {e}")

def standardize_columns(df):
    """Standardize column names to lowercase and replace spaces with underscores."""
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    return df

def clean_dates(df, date_columns):
    """Convert date columns to datetime format."""
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df

def remove_duplicates(df):
    """Remove duplicate rows."""
    return df.drop_duplicates()

def handle_missing(df):
    """Fill or drop missing values depending on context."""
    df = df.fillna({
        "material": "UNKNOWN",
        "quantity": 0
    })
    return df

def clean_data(file_path):
    """Full cleaning pipeline."""
    df = load_file(file_path)
    df = standardize_columns(df)
    df = clean_dates(df, ["posting_date", "document_date"])
    df = remove_duplicates(df)
    df = handle_missing(df)
    return df
