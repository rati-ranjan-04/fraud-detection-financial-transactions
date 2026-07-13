# Fraud Detection in Financial Transactions
### AI-Powered Financial Security and Transaction Risk Analysis System

## 📌 Project Overview
This project is a complete, beginner-friendly academic system designed to demonstrate how banks and financial institutions can use Python and Machine Learning to detect fraudulent transactions. It analyzes banking, UPI, and credit card records to identify suspicious activity, calculate fraud risk scores, and generate analytical reports.

## 🎯 Objectives
- Analyze various digital payment transactions (UPI, Bank, Card, etc.).
- Identify unusual patterns and detect potentially fraudulent activity.
- Assign a fraud-risk score to every transaction.
- Explain the reasoning behind suspicious flags.
- Provide a modern dashboard for financial analysts.

## 🛠️ Technology Stack
- **Python 3**: Core programming language.
- **Pandas & NumPy**: Data manipulation and analysis.
- **Scikit-learn**: Machine learning model training and evaluation.
- **Matplotlib & Seaborn**: Data visualization.
- **Streamlit**: Web-based graphical user interface.
- **Joblib**: Model serialization.
- **FPDF2**: PDF report generation.

## 📂 Project Structure
```
fraud_detection_project/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Project dependencies
├── README.md               # Project documentation
├── generate_dataset.py     # Script to generate synthetic financial data
├── train_model.py          # Script to train and evaluate ML models
├── fraud_rules.py          # Rule-based fraud detection engine
├── data_preprocessing.py   # Data cleaning and feature engineering
├── report_generator.py     # PDF report generation logic
│
├── data/                   # Dataset storage
├── models/                 # Saved models and preprocessors
├── reports/                # Generated PDF reports
├── assets/                 # UI assets (logos, banners)
└── screenshots/            # Model performance visualizations
```

## 🚀 Installation & Execution

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fraud_detection_project
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Generate the dataset**
   ```bash
   python generate_dataset.py
   ```

5. **Train the ML model**
   ```bash
   python train_model.py
   ```

6. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 📊 Features
- **Interactive Dashboard**: Real-time metrics and fraud trends.
- **Dataset Explorer**: Search and filter transaction records.
- **Fraud Analysis**: Visual insights into fraud patterns by time, amount, and category.
- **Transaction Risk Checker**: Manual entry form to check specific transactions.
- **Bulk Prediction**: Upload CSV files for batch fraud analysis.
- **Model Performance**: Detailed evaluation metrics (Accuracy, Precision, Recall, F1).
- **Report Generator**: Downloadable PDF reports for stakeholders.

## 🛡️ Security & Ethics
- This project is for **educational purposes** only.
- Predictions should not be treated as final proof of fraud without human review.
- In real-world scenarios, sensitive financial data must be anonymized and protected.
- The model may produce false positives; always verify before taking action.

## 👤 Author
**Rati Ranjan Mohapatra**  
AI Internship Project
