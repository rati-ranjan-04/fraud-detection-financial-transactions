import streamlit as st
import pandas as pd
import plotly.express as px

def show(df):
    st.title("📊 Dashboard")
    st.subheader("AI-Powered Financial Security and Transaction Risk Analysis System")
    
    if df is None:
        st.error("Dataset not found. Please run generate_dataset.py first.")
        return

    # Metrics
    total_tx = len(df)
    total_amt = df['Transaction Amount'].sum()
    fraud_df = df[df['Is Fraud'] == 1]
    total_fraud = len(fraud_df)
    fraud_pct = (total_fraud / total_tx) * 100
    avg_amt = df['Transaction Amount'].mean()
    fraud_amt = fraud_df['Transaction Amount'].sum()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Transactions", f"{total_tx:,}")
    with col2:
        st.metric("Total Amount", f"₹{total_amt:,.2f}")
    with col3:
        st.metric("Fraudulent Tx", f"{total_fraud:,}")
    with col4:
        st.metric("Fraud Percentage", f"{fraud_pct:.2f}%")
        
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Avg Tx Amount", f"₹{avg_amt:,.2f}")
    with col2:
        st.metric("Fraud Exposure", f"₹{fraud_amt:,.2f}")
    with col3:
        high_risk_count = len(df[df['Transaction Amount'] > 50000])
        st.metric("High Value Tx", f"{high_risk_count:,}")
    with col4:
        st.metric("Success Rate", f"{(len(df[df['Transaction Status']=='Success'])/total_tx)*100:.1f}%")

    st.markdown("---")
    
    # Simple Charts
    c1, c2 = st.columns(2)
    with c1:
        fig = px.pie(df, names='Is Fraud', title='Legitimate vs Fraudulent Transactions', 
                     color_discrete_sequence=['#2ecc71', '#e74c3c'],
                     labels={'Is Fraud': 'Fraud Status'})
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
        
    with c2:
        # Fraud by Transaction Type
        fraud_by_type = df[df['Is Fraud'] == 1].groupby('Transaction Type').size().reset_index(name='Count')
        fig = px.bar(fraud_by_type, x='Transaction Type', y='Count', title='Fraud Cases by Transaction Type',
                     color='Count', color_continuous_scale='Reds')
        st.plotly_chart(fig, use_container_width=True)

    # Trend chart
    st.subheader("Transaction Trends")
    df['Transaction Date'] = pd.to_datetime(df['Transaction Date'])
    daily_trend = df.groupby('Transaction Date').size().reset_index(name='Total')
    daily_fraud = df[df['Is Fraud'] == 1].groupby('Transaction Date').size().reset_index(name='Fraud')
    trend_df = pd.merge(daily_trend, daily_fraud, on='Transaction Date', how='left').fillna(0)
    
    fig = px.line(trend_df, x='Transaction Date', y=['Total', 'Fraud'], title='Daily Transaction Activity',
                  color_discrete_map={'Total': '#3498db', 'Fraud': '#e74c3c'})
    st.plotly_chart(fig, use_container_width=True)
