import streamlit as st
import pandas as pd
import io
from fraud_rules import FraudRulesEngine

def show(model, preprocessor, rules_engine):
    st.title("📂 Bulk Prediction")
    st.markdown("Upload a CSV file containing multiple transactions for fraud analysis.")
    
    st.info("The CSV should contain columns like: Transaction Amount, Transaction Type, Payment Method, Average Customer Transaction Amount, etc.")
    
    # Download template
    if st.button("Download Sample Template"):
        sample_df = pd.read_csv('data/sample_upload.csv')
        csv = sample_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Click here to download template",
            data=csv,
            file_name='sample_transactions.csv',
            mime='text/csv',
        )
        
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            input_df = pd.read_csv(uploaded_file)
            st.success(f"Successfully loaded {len(input_df)} records.")
            
            if st.button("Run Bulk Analysis"):
                with st.spinner("Processing..."):
                    # Preprocess for ML
                    X, _ = preprocessor.preprocess(input_df, training=False)
                    
                    # ML Predictions
                    ml_preds = model.predict(X)
                    ml_probs = model.predict_proba(X)[:, 1]
                    
                    # Rule-based and combined results
                    results = []
                    for i in range(len(input_df)):
                        row = input_df.iloc[i]
                        # Need to handle case where columns might be missing in uploaded file
                        tx_data = row.to_dict()
                        # Ensure Hour exists for rules engine
                        if 'Hour' not in tx_data:
                            try:
                                tx_data['Hour'] = pd.to_datetime(tx_data['Transaction Time']).hour
                            except:
                                tx_data['Hour'] = 12
                                
                        rule_res = rules_engine.evaluate_transaction(tx_data)
                        
                        results.append({
                            'ML Prediction': 'Fraud' if ml_preds[i] == 1 else 'Legitimate',
                            'Fraud Probability': f"{ml_probs[i]*100:.2f}%",
                            'Risk Score': rule_res['risk_score'],
                            'Risk Level': rule_res['risk_level'],
                            'Recommendation': rule_res['recommendation']
                        })
                    
                    res_df = pd.concat([input_df, pd.DataFrame(results)], axis=1)
                    
                    st.subheader("Analysis Results")
                    st.dataframe(res_df, use_container_width=True)
                    
                    # Filter suspicious
                    suspicious = res_df[(res_df['ML Prediction'] == 'Fraud') | (res_df['Risk Score'] >= 50)]
                    st.warning(f"Detected {len(suspicious)} suspicious transactions.")
                    
                    # Download results
                    csv = res_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download Full Prediction Results",
                        data=csv,
                        file_name='fraud_prediction_results.csv',
                        mime='text/csv',
                    )
        except Exception as e:
            st.error(f"Error processing file: {e}")
            st.info("Please ensure the CSV file structure matches the sample template.")
