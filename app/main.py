import streamlit as st
import pandas as pd
from io import BytesIO

from engine.cleaning import clean_data
from engine.validation import validate_data
from engine.anomalies import anomaly_report

st.title("📦 Material Usage Automation Engine")
st.write("Upload your material usage Excel file to clean, validate, and analyze it.")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    st.success("File uploaded successfully!")

    # -------------------------------
    # CLEANING
    # -------------------------------
    st.subheader("🔧 Cleaning Data")
    df_clean = clean_data(uploaded_file)
    st.dataframe(df_clean.head())

    # -------------------------------
    # VALIDATION
    # -------------------------------
    st.subheader("🛑 Validation Issues")
    issues = validate_data(df_clean)

    for name, issue_df in issues.items():
        if not issue_df.empty:
            st.write(f"**{name.replace('_', ' ').title()}**")
            st.dataframe(issue_df)

    # -------------------------------
    # ANOMALY DETECTION
    # -------------------------------
    st.subheader("⚠️ Anomaly Detection")
    anomalies = anomaly_report(df_clean)

    for name, anomaly_df in anomalies.items():
        if not anomaly_df.empty:
            st.write(f"**{name.replace('_', ' ').title()}**")
            st.dataframe(anomaly_df)

    # -------------------------------
    # 📤 DOWNLOAD OUTPUTS (FINAL FIX)
    # -------------------------------
    st.subheader("📤 Download Outputs")

    # CLEAN DATA DOWNLOAD
    clean_buffer = BytesIO()
    df_clean.to_excel(clean_buffer, index=False, engine="openpyxl")
    clean_buffer.seek(0)

    st.download_button(
        label="Download Clean Data",
        data=clean_buffer,
        file_name="clean_output.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # VALIDATION ISSUES DOWNLOAD
    issues_buffer = BytesIO()
    with pd.ExcelWriter(issues_buffer, engine="openpyxl") as writer:
        wrote_sheet = False
        for name, issue_df in issues.items():
            if not issue_df.empty:
                issue_df.to_excel(writer, sheet_name=name[:31], index=False)
                wrote_sheet = True
        if not wrote_sheet:
            pd.DataFrame({"message": ["No validation issues found"]}).to_excel(
                writer, sheet_name="No_Issues", index=False
            )
    issues_buffer.seek(0)

    st.download_button(
        label="Download Validation Issues",
        data=issues_buffer,
        file_name="validation_issues.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # ANOMALY REPORT DOWNLOAD
    anomalies_buffer = BytesIO()
    with pd.ExcelWriter(anomalies_buffer, engine="openpyxl") as writer:
        wrote_sheet = False
        for name, anomaly_df in anomalies.items():
            if not anomaly_df.empty:
                anomaly_df.to_excel(writer, sheet_name=name[:31], index=False)
                wrote_sheet = True
        if not wrote_sheet:
            pd.DataFrame({"message": ["No anomalies detected"]}).to_excel(
                writer, sheet_name="No_Anomalies", index=False
            )
    anomalies_buffer.seek(0)

    st.download_button(
        label="Download Anomaly Report",
        data=anomalies_buffer,
        file_name="anomaly_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
