import pandas as pd

def export_clean_data(df, output_path="clean_output.xlsx"):
    """Export cleaned data to Excel."""
    try:
        df.to_excel(output_path, index=False)
        return output_path
    except Exception as e:
        raise ValueError(f"Error exporting clean data: {e}")

def export_issues(issues_dict, output_path="validation_issues.xlsx"):
    """Export validation issues to a multi-sheet Excel file."""
    try:
        with pd.ExcelWriter(output_path) as writer:
            for issue_name, issue_df in issues_dict.items():
                if not issue_df.empty:
                    issue_df.to_excel(writer, sheet_name=issue_name[:31], index=False)
        return output_path
    except Exception as e:
        raise ValueError(f"Error exporting validation issues: {e}")

def export_anomalies(anomalies_dict, output_path="anomaly_report.xlsx"):
    """Export anomaly detection results to a multi-sheet Excel file."""
    try:
        with pd.ExcelWriter(output_path) as writer:
            for anomaly_name, anomaly_df in anomalies_dict.items():
                if not anomaly_df.empty:
                    anomaly_df.to_excel(writer, sheet_name=anomaly_name[:31], index=False)
        return output_path
    except Exception as e:
        raise ValueError(f"Error exporting anomalies: {e}")
