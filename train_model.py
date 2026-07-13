import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score, roc_curve
import joblib
import os
from data_preprocessing import DataPreprocessor

def train_and_evaluate():
    print("Loading data...")
    df = pd.read_csv('data/financial_transactions.csv')
    
    print("Preprocessing data...")
    preprocessor = DataPreprocessor()
    X, y = preprocessor.preprocess(df)
    
    # Save preprocessor params
    preprocessor.save_params()
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print(f"Training data shape: {X_train.shape}")
    print(f"Test data shape: {X_test.shape}")
    
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000),
        'Decision Tree': DecisionTreeClassifier(random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42)
    }
    
    results = []
    best_f1 = 0
    best_model = None
    best_model_name = ""
    
    os.makedirs('screenshots', exist_ok=True)
    
    for name, model in models.items():
        print(f"Training {name}...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_prob)
        
        results.append({
            'Model': name,
            'Accuracy': acc,
            'Precision': prec,
            'Recall': rec,
            'F1-score': f1,
            'ROC-AUC': auc
        })
        
        print(f"{name} - F1: {f1:.4f}, Recall: {rec:.4f}")
        
        if f1 > best_f1:
            best_f1 = f1
            best_model = model
            best_model_name = name
            
    results_df = pd.DataFrame(results)
    print("\nModel Comparison:")
    print(results_df)
    results_df.to_csv('models/model_comparison.csv', index=False)
    
    print(f"\nBest Model: {best_model_name}")
    joblib.dump(best_model, 'models/fraud_detection_model.pkl')
    
    # Generate evaluation plots for the best model
    y_pred = best_model.predict(X_test)
    y_prob = best_model.predict_proba(X_test)[:, 1]
    
    # Confusion Matrix
    plt.figure(figsize=(8, 6))
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(f'Confusion Matrix - {best_model_name}')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.savefig('screenshots/confusion_matrix.png')
    
    # ROC Curve
    plt.figure(figsize=(8, 6))
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    plt.plot(fpr, tpr, label=f'ROC AUC = {roc_auc_score(y_test, y_prob):.2f}')
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'ROC Curve - {best_model_name}')
    plt.legend()
    plt.savefig('screenshots/roc_curve.png')
    
    # Feature Importance (for Tree models)
    if hasattr(best_model, 'feature_importances_'):
        plt.figure(figsize=(10, 8))
        importances = best_model.feature_importances_
        feat_importances = pd.Series(importances, index=X.columns)
        feat_importances.nlargest(10).plot(kind='barh')
        plt.title('Top 10 Feature Importances')
        plt.tight_layout()
        plt.savefig('screenshots/feature_importance.png')

    print("Model training and evaluation complete.")

if __name__ == "__main__":
    train_and_evaluate()
