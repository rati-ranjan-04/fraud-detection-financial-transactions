import streamlit as st
import pandas as pd
import numpy as np

def show(model, preprocessor, rules_engine):
    st.title("🛡️ Transaction Risk Checker")
    st.markdown("Manually enter transaction details to evaluate fraud risk.")
    
    with st.form("risk_checker_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            amount = st.number_input("Transaction Amount (₹)", min_value=0.0, value=5000.0)
            tx_type = st.selectbox("Transaction Type", ['UPI transfer', 'Bank transfer', 'Credit-card payment', 'Debit-card payment', 'ATM withdrawal', 'Online purchase', 'Mobile-wallet payment'])
            pay_method = st.selectbox("Payment Method", ['Digital Wallet', 'Net Banking', 'Card', 'ATM', 'UPI'])
            merchant_cat = st.selectbox("Merchant Category", ['Groceries', 'Electronics', 'Fashion', 'Travel', 'Entertainment', 'Health', 'Dining', 'Services', 'Others'])
            tx_time = st.time_input("Transaction Time", value=pd.to_datetime("12:00:00").time())
            
        with col2:
            avg_amt = st.number_input("Customer Average Amount (₹)", min_value=1.0, value=3000.0)
            failed_attempts = st.number_input("Failed Attempts in Last 24h", min_value=0, max_value=10, value=0)
            tx_24h = st.number_input("Transactions in Last 24h", min_value=1, max_value=100, value=2)
            is_new_device = st.checkbox("Is New Device?")
            is_unusual_loc = st.checkbox("Is Unusual Location?")
            is_international = st.checkbox("Is International?")
            
        submitted = st.form_submit_button("Check Risk")
        
    if submitted:
        # Prepare data for rules engine
        tx_data = {
            'Transaction Amount': amount,
            'Average Customer Transaction Amount': avg_amt,
            'Transactions in Last 24 Hours': tx_24h,
            'Failed Transaction Attempts': failed_attempts,
            'Is New Device': 1 if is_new_device else 0,
            'Is Unusual Location': 1 if is_unusual_loc else 0,
            'Is International': 1 if is_international else 0,
            'Transaction Time': tx_time.strftime('%H:%M:%S'),
            'Hour': tx_time.hour
        }
        
        # Rule-based evaluation
        rule_result = rules_engine.evaluate_transaction(tx_data)
        
        # ML-based evaluation
        ml_prediction = "Legitimate"
        ml_prob = 0.0
        
        if model and preprocessor:
            # Create a dummy row with all required columns for preprocessor
            input_df = pd.DataFrame([{
                'Transaction ID': 'TXN_TEMP',
                'Customer ID': 'CUST_TEMP',
                'Transaction Date': pd.Timestamp.now().strftime('%Y-%m-%d'),
                'Transaction Time': tx_time.strftime('%H:%M:%S'),
                'Transaction Amount': amount,
                'Transaction Type': tx_type,
                'Payment Method': pay_method,
                'Merchant Category': merchant_cat,
                'Sender Location': 'Mumbai',
                'Receiver Location': 'Mumbai',
                'Account Age (Days)': 365,
                'Customer Age': 30,
                'Transactions in Last 24 Hours': tx_24h,
                'Average Customer Transaction Amount': avg_amt,
                'Failed Transaction Attempts': failed_attempts,
                'Device Type': 'Mobile',
                'Device ID': 'DEV_TEMP',
                'IP Address': '127.0.0.1',
                'Is New Device': 1 if is_new_device else 0,
                'Is Unusual Location': 1 if is_unusual_loc else 0,
                'Is International': 1 if is_international else 0,
                'Transaction Status': 'Success'
            }])
            
            X, _ = preprocessor.preprocess(input_df, training=False)
            ml_pred = model.predict(X)[0]
            ml_prob = model.predict_proba(X)[0][1]
            ml_prediction = "Fraudulent" if ml_pred == 1 else "Legitimate"
            
        # Display Results
        st.markdown("---")
        st.subheader("Analysis Results")
        
        res_col1, res_col2 = st.columns(2)
        
        with res_col1:
            st.markdown(f"### Rule-Based Result")
            st.markdown(f"**Risk Level:** <span style='color:{rule_result['color']}; font-size:24px; font-weight:bold;'>{rule_result['risk_level']}</span>", unsafe_allow_html=True)
            st.markdown(f"**Risk Score:** {rule_result['risk_score']}/100")
            st.info(f"**Recommendation:** {rule_result['recommendation']}")
            
        with res_col2:
            st.markdown(f"### ML Model Prediction")
            ml_color = "red" if ml_prediction == "Fraudulent" else "green"
            st.markdown(f"**Prediction:** <span style='color:{ml_color}; font-size:24px; font-weight:bold;'>{ml_prediction}</span>", unsafe_allow_html=True)
            st.markdown(f"**Fraud Probability:** {ml_prob*100:.2f}%")
            
        st.markdown("### Triggered Fraud Indicators")
        if rule_result['triggered_rules']:
            for rule in rule_result['triggered_rules']:
                st.warning(f"⚠️ {rule}")
        else:
            st.success("✅ No suspicious patterns detected by rule engine.")
            
        st.markdown("### Human-Readable Explanation")
        if ml_prediction == "Fraudulent" or rule_result['risk_score'] > 50:
            st.write(f"The system has flagged this transaction as suspicious because it exhibits patterns consistent with financial fraud, such as {', '.join([r.split(':')[0] for r in rule_result['triggered_rules'][:2]])}. High-risk transactions require additional verification.")
        else:
            st.write("This transaction appears to be consistent with the customer's normal behavior and does not trigger major risk indicators.")
