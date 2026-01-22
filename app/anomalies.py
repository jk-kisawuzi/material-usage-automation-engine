import pandas as pd

def detect_outliers(df, column="quantity", z_threshold=3):
    """Detect statistical outliers using Z-score."""
    if column not in df.columns:
        return pd.DataFrame()

    df_clean = df[df[column].notna()].copy()
    df_clean["z_score"] = (df_clean[column] - df_clean[column].mean()) / df_clean[column].std()

    return df_clean[df_clean["z_score"].abs() > z_threshold]

def detect_spikes(df, column="quantity", multiplier=3):
    """Detect sudden spikes compared to previous values."""
    if column not in df.columns:
        return pd.DataFrame()

    df_sorted = df.sort_values(by="posting_date").copy()
    df_sorted["prev_value"] = df_sorted[column].shift(1)
    df_sorted["ratio"] = df_sorted[column] / df_sorted["prev_value"]

    return df_sorted[df_sorted["ratio"] > multiplier]

def detect_drops(df, column="quantity", multiplier=3):
    """Detect sudden drops compared to previous values."""
    if column not in df.columns:
        return pd.DataFrame()

    df_sorted = df.sort_values(by="posting_date").copy()
    df_sorted["prev_value"] = df_sorted[column].shift(1)
    df_sorted["ratio"] = df_sorted["prev_value"] / df_sorted[column]

    return df_sorted[df_sorted["ratio"] > multiplier]

def anomaly_report(df):
    """Run all anomaly detection checks."""
    return {
        "outliers": detect_outliers(df),
        "spikes": detect_spikes(df),
        "drops": detect_drops(df),
    }
