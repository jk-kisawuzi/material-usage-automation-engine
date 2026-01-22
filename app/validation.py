def validate_data(df):
    """Run all validation checks and return a single combined DataFrame."""
    issues = []

    # Negative quantities
    if "quantity" in df.columns:
        neg = df[df["quantity"] < 0]
        for idx in neg.index:
            issues.append({"Row": idx, "Issue": "Negative quantity"})

    # Missing materials
    if "material" in df.columns:
        miss = df[df["material"].isna() | (df["material"] == "UNKNOWN")]
        for idx in miss.index:
            issues.append({"Row": idx, "Issue": "Missing or UNKNOWN material"})

    # Invalid units
    if "unit" in df.columns:
        valid_units = ["KG", "L", "EA", "G", "ML"]
        bad_units = df[~df["unit"].isin(valid_units)]
        for idx in bad_units.index:
            issues.append({"Row": idx, "Issue": "Invalid unit"})

    # Unrealistic values
    if "quantity" in df.columns:
        weird = df[(df["quantity"] == 0) | (df["quantity"] > 1_000_000)]
        for idx in weird.index:
            issues.append({"Row": idx, "Issue": "Unrealistic quantity"})

    # Always return a DataFrame
    return pd.DataFrame(issues)
