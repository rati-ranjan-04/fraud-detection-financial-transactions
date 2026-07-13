import streamlit as st
import pandas as pd
import os
from PIL import Image

def show():
    st.title("🎯 Model Performance")
    
    if not os.path.exists('models/model_comparison.csv'):
        st.error("Model performance data not found. Please run train_model.py first.")
        return

    comparison_df = pd.read_csv('models/model_comparison.csv')
    
    st.subheader("Model Comparison")
    st.table(comparison_df.style.highlight_max(axis=0, subset=['Accuracy', 'Precision', 'Recall', 'F1-score', 'ROC-AUC'], color='lightgreen'))
    
    st.info("""
    **Evaluation Metrics Explanation:**
    - **Recall:** Crucial for fraud detection. It measures how many actual fraud cases were caught.
    - **Precision:** Measures how many predicted fraud cases were actually fraud.
    - **F1-score:** The harmonic mean of Precision and Recall.
    - **ROC-AUC:** Measures the model's ability to distinguish between classes.
    """)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Confusion Matrix")
        if os.path.exists('screenshots/confusion_matrix.png'):
            st.image('screenshots/confusion_matrix.png', use_container_width=True)
        else:
            st.info("Confusion matrix plot not available.")
            
    with col2:
        st.subheader("ROC Curve")
        if os.path.exists('screenshots/roc_curve.png'):
            st.image('screenshots/roc_curve.png', use_container_width=True)
        else:
            st.info("ROC curve plot not available.")
            
    st.markdown("---")
    
    st.subheader("Feature Importance")
    if os.path.exists('screenshots/feature_importance.png'):
        st.image('screenshots/feature_importance.png', use_container_width=True)
        st.write("Feature importance shows which variables the model relies on most to identify fraud.")
    else:
        st.info("Feature importance plot not available.")
        
    st.subheader("Model Limitations")
    st.markdown("""
    - **Data Imbalance:** Fraudulent transactions are rare (approx. 5-6% in this dataset), which can lead to biased models.
    - **Evolving Patterns:** Fraudsters constantly change tactics; models need regular retraining.
    - **False Positives:** Legitimate transactions might be flagged, causing customer friction.
    - **Privacy:** Real-world deployment requires strict data anonymization and compliance.
    """)
