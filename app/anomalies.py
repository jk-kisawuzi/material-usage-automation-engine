import pandas as pd

def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detects simple anomalies in the material usage dataset.
    You can expand this logic later, but this version will run safely.
    """

    anomalies = []

    # Example anomaly rules — adjust as needed
    for idx, row in df.iterrows():
        issue_list = []

        # Rule 1: Negative quantities
        if "Quantity" in df.columns and row["Quantity"] < 0:
            issue_list.append("Negative quantity")

        # Rule 2: Zero usage
        if "Quantity" in df.columns and row["Quantity"] == 0:
            issue_list.append("Zero quantity")

        # Rule 3: Missing material code
        if "Material" in df.columns and pd.isna(row["Material"]):
            issue_list.append("Missing material code")

        # If any issues found, record them
        if issue_list:
            anomalies.append({
                "Row": idx,
                "Material": row.get("Material", None),
                "Quantity": row.get("Quantity", None),
                "Issues": ", ".join(issue_list)
            })

    # Convert to DataFrame
    if anomalies:
        return pd.DataFrame(anomalies)
    else:
        return pd.DataFrame(columns=["Row", "Material", "Quantity", "Issues"])
