import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
import os

class DataPreprocessor:
    def __init__(self):
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.target_column = 'Is Fraud'
        self.feature_cols = []
        
    def clean_data(self, df):
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Handle missing values (if any)
        df = df.ffill().bfill()
        
        return df

    def feature_engineering(self, df):
        # Date and time features
        df['Transaction Date'] = pd.to_datetime(df['Transaction Date'])
        df['Transaction Time'] = pd.to_timedelta(df['Transaction Time'])
        
        df['Hour'] = df['Transaction Time'].dt.components.hours
        df['DayOfWeek'] = df['Transaction Date'].dt.dayofweek
        
        # Amount-to-average ratio
        df['Amount_to_Avg_Ratio'] = df['Transaction Amount'] / df['Average Customer Transaction Amount']
        
        # Unusual-hour indicator (Midnight to 4 AM)
        df['Is_Unusual_Hour'] = df['Hour'].apply(lambda x: 1 if x < 5 else 0)
        
        # High-value transaction indicator (e.g., > 50000)
        df['Is_High_Value'] = df['Transaction Amount'].apply(lambda x: 1 if x > 50000 else 0)
        
        # Risk indicators already in dataset: Is New Device, Is Unusual Location, Is International
        
        # Location Mismatch (Simplified: if sender != receiver, though in data sender is usually home/away)
        df['Location_Mismatch'] = (df['Sender Location'] != df['Receiver Location']).astype(int)
        
        return df

    def preprocess(self, df, training=True):
        df = self.clean_data(df)
        df = self.feature_engineering(df)
        
        # Columns to drop (IDs, strings not useful for ML directly without heavy encoding)
        cols_to_drop = ['Transaction ID', 'Customer ID', 'Transaction Date', 'Transaction Time', 'Device ID', 'IP Address', 'Sender Location', 'Receiver Location']
        
        # If target column exists, separate it
        y = None
        if self.target_column in df.columns:
            y = df[self.target_column]
            cols_to_drop.append(self.target_column)
            
        X = df.drop(columns=cols_to_drop)
        
        # Identify categorical and numerical columns
        cat_cols = X.select_dtypes(include=['object']).columns
        num_cols = X.select_dtypes(include=['int64', 'float64']).columns
        
        # Encoding categorical variables
        for col in cat_cols:
            if training:
                le = LabelEncoder()
                X[col] = le.fit_transform(X[col].astype(str))
                self.label_encoders[col] = le
            else:
                if col in self.label_encoders:
                    le = self.label_encoders[col]
                    # Handle unseen labels by mapping to a default or most frequent
                    X[col] = X[col].apply(lambda x: le.transform([x])[0] if x in le.classes_ else -1)
                else:
                    X[col] = 0 # Fallback
                    
        # Scaling numerical variables
        if training:
            X[num_cols] = self.scaler.fit_transform(X[num_cols])
            self.feature_cols = X.columns.tolist()
        else:
            X[num_cols] = self.scaler.transform(X[num_cols])
            # Ensure same columns and order
            for col in self.feature_cols:
                if col not in X.columns:
                    X[col] = 0
            X = X[self.feature_cols]
            
        return X, y

    def save_params(self, path='models/'):
        os.makedirs(path, exist_ok=True)
        joblib.dump(self.label_encoders, os.path.join(path, 'encoder.pkl'))
        joblib.dump(self.scaler, os.path.join(path, 'scaler.pkl'))
        joblib.dump(self.feature_cols, os.path.join(path, 'feature_cols.pkl'))

    def load_params(self, path='models/'):
        self.label_encoders = joblib.load(os.path.join(path, 'encoder.pkl'))
        self.scaler = joblib.load(os.path.join(path, 'scaler.pkl'))
        self.feature_cols = joblib.load(os.path.join(path, 'feature_cols.pkl'))

if __name__ == "__main__":
    # Test preprocessing
    df = pd.read_csv('data/financial_transactions.csv')
    preprocessor = DataPreprocessor()
    X, y = preprocessor.preprocess(df)
    print("Preprocessed features shape:", X.shape)
    print("Features:", X.columns.tolist())
    preprocessor.save_params()
