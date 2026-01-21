import pandas as pd

def check_negative_quantities(df):
    """Flag rows where quantity is negative."""
    if "quantity" in df.columns:
        return df[df["quantity"] < 0]
    return pd.DataFrame()

def check_missing_materials(df):
    """Flag rows where material is missing or UNKNOWN."""
    if "material" in df.columns:
        return df[df["material"].isna() | (df["material"] == "UNKNOWN")]
    return pd.DataFrame()

def check_invalid_units(df, valid_units=None):
    """Flag rows with units not in the valid list."""
    if valid_units is None:
        valid_units = ["KG", "L", "EA", "G", "ML"]

    if "unit" in df.columns:
        return df[~df["unit"].isin(valid_units)]
    return pd.DataFrame()

def check_unrealistic_values(df):
    """Flag rows where quantity is extremely high or zero."""
    if "quantity" in df.columns:
        return df[(df["quantity"] == 0) | (df["quantity"] > 1_000_000)]
    return pd.DataFrame()

def validate_data(df):
    """Run all validation checks and return a dictionary of issues."""
    issues = {
        "negative_quantities": check_negative_quantities(df),
        "missing_materials": check_missing_materials(df),
        "invalid_units": check_invalid_units(df),
        "unrealistic_values": check_unrealistic_values(df),
    }
    return issues
