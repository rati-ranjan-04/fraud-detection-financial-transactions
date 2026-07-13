import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_realistic_data(num_records=5500):
    print(f"Generating {num_records} records...")
    
    # Base lists
    transaction_types = ['UPI transfer', 'Bank transfer', 'Credit-card payment', 'Debit-card payment', 'ATM withdrawal', 'Online purchase', 'Mobile-wallet payment']
    payment_methods = ['Digital Wallet', 'Net Banking', 'Card', 'ATM', 'UPI']
    merchant_categories = ['Groceries', 'Electronics', 'Fashion', 'Travel', 'Entertainment', 'Health', 'Dining', 'Services', 'Others']
    device_types = ['Mobile', 'Desktop', 'Tablet']
    locations = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Ahmedabad', 'Chennai', 'Kolkata', 'Pune', 'Jaipur', 'Lucknow', 'New York', 'London', 'Dubai', 'Singapore']
    
    data = []
    
    # Pre-generate some customers to ensure multiple transactions per customer
    num_customers = 1000
    customer_profiles = {}
    for i in range(1, num_customers + 1):
        cust_id = f"CUST{10000 + i}"
        customer_profiles[cust_id] = {
            'age': random.randint(18, 75),
            'account_age_days': random.randint(30, 3650),
            'avg_amount': random.uniform(500, 5000),
            'home_location': random.choice(locations[:10]), # Mostly Indian cities
            'usual_device_id': f"DEV{random.randint(100000, 999999)}"
        }

    start_date = datetime(2024, 1, 1)
    
    for i in range(num_records):
        tx_id = f"TXN{200000 + i}"
        cust_id = random.choice(list(customer_profiles.keys()))
        profile = customer_profiles[cust_id]
        
        # Date and Time
        days_offset = random.randint(0, 180)
        seconds_offset = random.randint(0, 86399)
        tx_datetime = start_date + timedelta(days=days_offset, seconds=seconds_offset)
        tx_date = tx_datetime.strftime('%Y-%m-%d')
        tx_time = tx_datetime.strftime('%H:%M:%S')
        hour = tx_datetime.hour
        
        # Transaction Details
        tx_type = random.choice(transaction_types)
        pay_method = random.choice(payment_methods)
        merchant_cat = random.choice(merchant_categories)
        
        # Amount - log normal distribution for realism
        amount = np.random.lognormal(mean=np.log(profile['avg_amount']), sigma=0.8)
        
        # Location
        sender_loc = profile['home_location']
        if random.random() < 0.1: # 10% chance of being away from home
            sender_loc = random.choice(locations)
        receiver_loc = random.choice(locations)
        
        # Risk factors (preliminary)
        is_unusual_loc = 1 if sender_loc != profile['home_location'] else 0
        is_new_device = 1 if random.random() < 0.05 else 0
        device_id = profile['usual_device_id'] if not is_new_device else f"DEV{random.randint(100000, 999999)}"
        device_type = random.choice(device_types)
        ip_addr = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        
        is_international = 1 if sender_loc in ['New York', 'London', 'Dubai', 'Singapore'] else 0
        failed_attempts = 0
        if random.random() < 0.05:
            failed_attempts = random.randint(1, 4)
            
        tx_last_24h = random.randint(1, 10)
        
        # Fraud Logic
        is_fraud = 0
        
        # Pattern 1: High amount relative to average
        if amount > profile['avg_amount'] * 5 and random.random() < 0.7:
            is_fraud = 1
        
        # Pattern 2: Unusual hours + High amount
        if (hour < 5 or hour > 23) and amount > 10000 and random.random() < 0.6:
            is_fraud = 1
            
        # Pattern 3: Failed attempts + Success
        if failed_attempts >= 3 and random.random() < 0.8:
            is_fraud = 1
            
        # Pattern 4: New device + Unusual location
        if is_new_device and is_unusual_loc and random.random() < 0.5:
            is_fraud = 1
            
        # Pattern 5: International + New account
        if is_international and profile['account_age_days'] < 90 and random.random() < 0.7:
            is_fraud = 1

        # Pattern 6: Rapid transactions (simulated by tx_last_24h)
        if tx_last_24h > 8 and amount > 5000 and random.random() < 0.4:
            is_fraud = 1

        # Final adjustments for labels
        status = "Success"
        if failed_attempts > 0 and random.random() < 0.3:
            status = "Failed"
        
        if is_fraud:
            # Make fraudulent transactions look more suspicious if they aren't already
            if random.random() < 0.3:
                amount = profile['avg_amount'] * random.uniform(10, 50)
            if random.random() < 0.3:
                failed_attempts = random.randint(2, 5)
            status = "Success" # Fraud usually succeeds to be fraud

        data.append({
            'Transaction ID': tx_id,
            'Customer ID': cust_id,
            'Transaction Date': tx_date,
            'Transaction Time': tx_time,
            'Transaction Amount': round(amount, 2),
            'Transaction Type': tx_type,
            'Payment Method': pay_method,
            'Merchant Category': merchant_cat,
            'Sender Location': sender_loc,
            'Receiver Location': receiver_loc,
            'Account Age (Days)': profile['account_age_days'],
            'Customer Age': profile['age'],
            'Transactions in Last 24 Hours': tx_last_24h,
            'Average Customer Transaction Amount': round(profile['avg_amount'], 2),
            'Failed Transaction Attempts': failed_attempts,
            'Device Type': device_type,
            'Device ID': device_id,
            'IP Address': ip_addr,
            'Is New Device': is_new_device,
            'Is Unusual Location': is_unusual_loc,
            'Is International': is_international,
            'Transaction Status': status,
            'Is Fraud': is_fraud
        })

    df = pd.DataFrame(data)
    
    # Save to CSV
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/financial_transactions.csv', index=False)
    
    # Create a sample upload file (subset of columns without labels for testing)
    sample_upload = df.drop(columns=['Is Fraud']).sample(20)
    sample_upload.to_csv('data/sample_upload.csv', index=False)
    
    print(f"Dataset generated successfully with {len(df)} records.")
    print(f"Fraudulent transactions: {df['Is Fraud'].sum()} ({df['Is Fraud'].mean()*100:.2f}%)")
    return df

if __name__ == "__main__":
    generate_realistic_data()
