import streamlit as st
import pandas as pd
import os
from report_generator import generate_pdf_report

def show(df):
    st.title("📄 Fraud Report Generator")
    st.markdown("Generate a comprehensive PDF report of the fraud analysis.")
    
    if df is None:
        st.error("Dataset not found.")
        return

    st.subheader("Report Configuration")
    report_title = st.text_input("Report Title", "Fraud Analysis Report - " + pd.Timestamp.now().strftime('%Y-%m-%d'))
    author = st.text_input("Author Name", "Rati Ranjan Mohapatra")
    
    st.markdown("""
    The report will include:
    - Executive Summary
    - Dataset Overview
    - Fraud Statistics
    - Risk Level Distribution
    - Top Suspicious Transactions
    - Preventive Recommendations
    """)
    
    if st.button("Generate and Download Report"):
        with st.spinner("Generating PDF..."):
            report_path = 'reports/fraud_analysis_report.pdf'
            os.makedirs('reports', exist_ok=True)
            
            success = generate_pdf_report(df, report_path, report_title, author)
            
            if success and os.path.exists(report_path):
                with open(report_path, "rb") as f:
                    st.download_button(
                        label="Download PDF Report",
                        data=f,
                        file_name=f"Fraud_Report_{pd.Timestamp.now().strftime('%Y%m%d')}.pdf",
                        mime="application/pdf"
                    )
                st.success("Report generated successfully!")
            else:
                st.error("Failed to generate report. Please check if 'report_generator.py' is implemented correctly.")
