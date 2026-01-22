import pandas as pd

def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Robust validation for material usage data.
    Always returns a DataFrame, never crashes.
    """

    issues = []

    # Normalize column names (lowercase for safety)
    df = df.copy()
    df.columns = [str(c).strip().lower() for c in df.columns]

    # Expected columns (your engine logic)
    material_col = None
    quantity_col = None

    # Try to detect material column
    for col in df.columns:
        if col in ["material", "item", "description"]:
            material_col = col
            break

    # Try to detect quantity column
    for col in df.columns:
        if col in ["quantity", "qty", "qty utilized", "qty imported"]:
            quantity_col = col
            break

    # If no material column found
    if material_col is None:
        issues.append({"Row": None, "Issue": "No material column found"})
        return pd.DataFrame(issues)

    # If no quantity column found
    if quantity_col is None:
        issues.append({"Row": None, "Issue": "No quantity column found"})
        return pd.DataFrame(issues)

    # Row-level validation
    for idx, row in df.iterrows():

        # Missing material
        material_value = str(row[material_col]).strip()
        if material_value == "" or material_value.lower() in ["nan", "none", "unknown"]:
            issues.append({"Row": idx, "Issue": "Missing or invalid material"})

        # Missing quantity
        qty_value = row[quantity_col]
        if pd.isna(qty_value) or str(qty_value).strip() == "":
            issues.append({"Row": idx, "Issue": "Missing quantity"})
            continue

        # Non-numeric quantity
        try:
            qty_float = float(qty_value)
        except:
            issues.append({"Row": idx, "Issue": f"Non-numeric quantity: {qty_value}"})
            continue

        # Negative quantity
        if qty_float < 0:
            issues.append({"Row": idx, "Issue": "Negative quantity"})

        # Zero quantity
        if qty_float == 0:
            issues.append({"Row": idx, "Issue": "Zero quantity"})

        # Unrealistically large quantity
        if qty_float > 1_000_000:
            issues.append({"Row": idx, "Issue": "Unrealistic quantity (>1,000,000)"})

    # Always return a DataFrame
    if issues:
        return pd.DataFrame(issues)
    else:
        return pd.DataFrame(columns=["Row", "Issue"])
