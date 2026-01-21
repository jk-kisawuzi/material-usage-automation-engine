import streamlit as st
import pandas as pd
from io import BytesIO

from cleaning import clean_data
from validation import validate_data
from anomalies import detect_anomalies

st.title("Material Usage Automation Engine")

uploaded_file = st.file_uploader("Upload your material usage file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.subheader("Raw Data")
    st.dataframe(df)

    cleaned_df = clean_data(df)
    st.subheader("Cleaned Data")
    st.dataframe(cleaned_df)

    validation_issues = validate_data(cleaned_df)
    st.subheader("Validation Issues")
    st.dataframe(validation_issues)

    anomalies = detect_anomalies(cleaned_df)
    st.subheader("Anomalies")
    st.dataframe(anomalies)

    def to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False)
        return output.getvalue()

    st.download_button(
        "Download Cleaned Output",
        data=to_excel(cleaned_df),
        file_name="clean_output.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.download_button(
        "Download Validation Issues",
        data=to_excel(validation_issues),
        file_name="validation_issues.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.download_button(
        "Download Anomaly Report",
        data=to_excel(anomalies),
        file_name="anomaly_report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
