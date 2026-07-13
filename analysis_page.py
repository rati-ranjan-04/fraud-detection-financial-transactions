import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

def show(df):
    st.title("📈 Fraud Analysis")
    
    if df is None:
        st.error("Dataset not found.")
        return

    fraud_df = df[df['Is Fraud'] == 1]
    
    tab1, tab2, tab3 = st.tabs(["Pattern Analysis", "Categorical Analysis", "Risk Distribution"])
    
    with tab1:
        st.subheader("Fraud Patterns by Time and Amount")
        
        # Fraud by Hour
        df['Hour'] = pd.to_datetime(df['Transaction Time'], format='%H:%M:%S').dt.hour
        hour_fraud = df.groupby('Hour')['Is Fraud'].mean().reset_index()
        fig1 = px.line(hour_fraud, x='Hour', y='Is Fraud', title='Fraud Probability by Hour of Day',
                       labels={'Is Fraud': 'Fraud Rate'})
        st.plotly_chart(fig1, use_container_width=True)
        st.info("Interpretation: Higher fraud rates are often observed during late-night hours (midnight to 4 AM).")
        
        # Fraud by Amount
        fig2 = px.histogram(df, x='Transaction Amount', color='Is Fraud', barmode='overlay',
                            title='Distribution of Transaction Amounts',
                            color_discrete_map={0: '#2ecc71', 1: '#e74c3c'})
        st.plotly_chart(fig2, use_container_width=True)
        st.info("Interpretation: Fraudulent transactions often exhibit higher amounts compared to legitimate ones.")

    with tab2:
        st.subheader("Fraud by Category")
        
        c1, c2 = st.columns(2)
        with c1:
            method_fraud = fraud_df.groupby('Payment Method').size().reset_index(name='Count')
            fig3 = px.pie(method_fraud, names='Payment Method', values='Count', title='Fraud by Payment Method')
            st.plotly_chart(fig3, use_container_width=True)
            
        with c2:
            cat_fraud = fraud_df.groupby('Merchant Category').size().reset_index(name='Count')
            fig4 = px.bar(cat_fraud, x='Merchant Category', y='Count', title='Fraud by Merchant Category',
                          color='Count', color_continuous_scale='Reds')
            st.plotly_chart(fig4, use_container_width=True)

    with tab3:
        st.subheader("Correlation and Risk Factors")
        
        # Numerical correlation
        num_cols = df.select_dtypes(include=['float64', 'int64']).columns
        corr = df[num_cols].corr()
        
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', ax=ax)
        plt.title("Correlation Heatmap of Numerical Features")
        st.pyplot(fig)
        
        st.subheader("Top Suspicious Accounts")
        suspicious_accounts = df.groupby('Customer ID').agg({
            'Is Fraud': 'sum',
            'Transaction Amount': 'sum',
            'Failed Transaction Attempts': 'sum'
        }).sort_values(by='Is Fraud', ascending=False).head(10)
        st.table(suspicious_accounts)
