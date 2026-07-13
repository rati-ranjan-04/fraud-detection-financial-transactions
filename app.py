import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
from datetime import datetime
from data_preprocessing import DataPreprocessor
from fraud_rules import FraudRulesEngine

# Page configuration
st.set_page_config(
    page_title="Fraud Detection System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: #f5f7f9;
    }
    .stSidebar {
        background-color: #001f3f;
    }
    .stSidebar .sidebar-content {
        color: white;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-left: 5px solid #001f3f;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: #001f3f;
        text-align: center;
        padding: 10px;
        font-size: 12px;
        border-top: 1px solid #ddd;
    }
</style>
""", unsafe_allow_state_warnings=True, unsafe_allow_html=True)

# Load data and models
@st.cache_data
def load_data():
    if os.path.exists('data/financial_transactions.csv'):
        return pd.read_csv('data/financial_transactions.csv')
    return None

@st.cache_resource
def load_ml_models():
    if os.path.exists('models/fraud_detection_model.pkl'):
        model = joblib.load('models/fraud_detection_model.pkl')
        preprocessor = DataPreprocessor()
        preprocessor.load_params()
        return model, preprocessor
    return None, None

df = load_data()
model, preprocessor = load_ml_models()
rules_engine = FraudRulesEngine()

# Sidebar navigation
st.sidebar.title("🛡️ Fraud Guard AI")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Dataset Explorer", "Fraud Analysis", "Transaction Risk Checker", "Bulk Prediction", "Model Performance", "Fraud Report Generator"]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**Project Title:**  
Fraud Detection in Financial Transactions

**Subtitle:**  
AI-Powered Financial Security System
""")

# Footer
st.markdown("""
<div class="footer">
    Developed by Rati Ranjan Mohapatra | AI Internship Project
</div>
""", unsafe_allow_html=True)

# Page logic
if page == "Dashboard":
    import dashboard_page
    dashboard_page.show(df)
elif page == "Dataset Explorer":
    import explorer_page
    explorer_page.show(df)
elif page == "Fraud Analysis":
    import analysis_page
    analysis_page.show(df)
elif page == "Transaction Risk Checker":
    import checker_page
    checker_page.show(model, preprocessor, rules_engine)
elif page == "Bulk Prediction":
    import bulk_page
    bulk_page.show(model, preprocessor, rules_engine)
elif page == "Model Performance":
    import performance_page
    performance_page.show()
elif page == "Fraud Report Generator":
    import report_page
    report_page.show(df)
