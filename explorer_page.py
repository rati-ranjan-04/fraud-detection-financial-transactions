import streamlit as st
import pandas as pd

def show(df):
    st.title("🔍 Dataset Explorer")
    
    if df is None:
        st.error("Dataset not found.")
        return

    # Filters
    st.sidebar.subheader("Filters")
    
    search_id = st.sidebar.text_input("Search Transaction ID or Customer ID")
    
    pay_methods = ['All'] + sorted(df['Payment Method'].unique().tolist())
    sel_method = st.sidebar.selectbox("Payment Method", pay_methods)
    
    tx_types = ['All'] + sorted(df['Transaction Type'].unique().tolist())
    sel_type = st.sidebar.selectbox("Transaction Type", tx_types)
    
    fraud_status = st.sidebar.selectbox("Fraud Status", ["All", "Legitimate", "Fraudulent"])
    
    # Apply filters
    filtered_df = df.copy()
    
    if search_id:
        filtered_df = filtered_df[
            (filtered_df['Transaction ID'].str.contains(search_id, case=False)) | 
            (filtered_df['Customer ID'].str.contains(search_id, case=False))
        ]
        
    if sel_method != 'All':
        filtered_df = filtered_df[filtered_df['Payment Method'] == sel_method]
        
    if sel_type != 'All':
        filtered_df = filtered_df[filtered_df['Transaction Type'] == sel_type]
        
    if fraud_status == "Legitimate":
        filtered_df = filtered_df[filtered_df['Is Fraud'] == 0]
    elif fraud_status == "Fraudulent":
        filtered_df = filtered_df[filtered_df['Is Fraud'] == 1]
        
    st.write(f"Showing {len(filtered_df)} records")
    st.dataframe(filtered_df, use_container_width=True)
    
    # Download
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Filtered Data as CSV",
        data=csv,
        file_name='filtered_transactions.csv',
        mime='text/csv',
    )
