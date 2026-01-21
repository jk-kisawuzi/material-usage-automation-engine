import sys
import os

# Fix for Streamlit Cloud: ensure root folder is in Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd

from engine.cleaning import clean_data
from engine.validation import validate_data
from engine.anomalies import detect_anomalies

st.title("Material Usage Automation Engine")

uploaded_file = st.file_uploader("Upload your material usage file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.subheader("Raw Data")
    st.dataframe(df)

    # Cleaning
    cleaned_df = clean_data(df)
    st.subheader("Cleaned Data")
    st.dataframe(cleaned_df)

    # Validation
    validation_issues = validate_data(cleaned_df)
    st.subheader("Validation Issues")
    st.dataframe(validation_issues)

    # Anomalies
    anomalies = detect_anomalies(cleaned_df)
    st.subheader("Anomalies")
    st.dataframe(anomalies)

    # Downloads
    st.download_button(
        "Download Cleaned Output",
        cleaned_df.to_excel(index=False),
        file_name="clean_output.xlsx"
    )

    st.download_button(
        "Download Validation Issues",
        validation_issues.to_excel(index=False),
        file_name="validation_issues.xlsx"
    )

    st.download_button(
        "Download Anomaly Report",
        anomalies.to_excel(index=False),
        file_name="anomaly_report.xlsx"
    )
