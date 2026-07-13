class FraudRulesEngine:
    def __init__(self):
        # Configuration for rules
        self.HIGH_AMOUNT_THRESHOLD = 50000
        self.FAILED_ATTEMPTS_THRESHOLD = 3
        self.MAX_TX_24H_THRESHOLD = 5
        self.AMOUNT_RATIO_THRESHOLD = 3.0
        
    def evaluate_transaction(self, tx_data):
        """
        Evaluates a single transaction based on predefined rules.
        tx_data: dictionary or pandas Series containing transaction details
        """
        score = 0
        triggered_rules = []
        
        # Rule 1: High Transaction Amount
        if tx_data['Transaction Amount'] > self.HIGH_AMOUNT_THRESHOLD:
            score += 40
            triggered_rules.append(f"Transaction amount ₹{tx_data['Transaction Amount']} exceeds limit of ₹{self.HIGH_AMOUNT_THRESHOLD}")
            
        # Rule 2: Amount to Average Ratio
        avg_amt = tx_data['Average Customer Transaction Amount']
        if avg_amt > 0:
            ratio = tx_data['Transaction Amount'] / avg_amt
            if ratio > self.AMOUNT_RATIO_THRESHOLD:
                score += 30
                triggered_rules.append(f"Amount is {ratio:.1f}x the customer's average (Threshold: {self.AMOUNT_RATIO_THRESHOLD}x)")
        
        # Rule 3: Multiple Transactions in 24 Hours
        if tx_data['Transactions in Last 24 Hours'] > self.MAX_TX_24H_THRESHOLD:
            score += 20
            triggered_rules.append(f"High frequency: {tx_data['Transactions in Last 24 Hours']} transactions in 24h")
            
        # Rule 4: Failed Attempts
        if tx_data['Failed Transaction Attempts'] >= self.FAILED_ATTEMPTS_THRESHOLD:
            score += 35
            triggered_rules.append(f"Multiple failed attempts ({tx_data['Failed Transaction Attempts']}) recorded")
            
        # Rule 5: New Device
        if tx_data.get('Is New Device', 0) == 1:
            score += 15
            triggered_rules.append("Transaction from a new/unrecognized device")
            
        # Rule 6: Unusual Location
        if tx_data.get('Is Unusual Location', 0) == 1:
            score += 20
            triggered_rules.append("Transaction from an unusual location")
            
        # Rule 7: International Transaction
        if tx_data.get('Is International', 0) == 1:
            score += 25
            triggered_rules.append("International transaction detected")
            
        # Rule 8: Unusual Hours (Midnight to 4 AM)
        # Check if tx_time is string or timedelta
        hour = 0
        if isinstance(tx_data['Transaction Time'], str):
            hour = int(tx_data['Transaction Time'].split(':')[0])
        else:
            # Assume it's already processed or a datetime/timedelta
            try:
                hour = tx_data['Hour']
            except:
                pass
                
        if hour < 5:
            score += 15
            triggered_rules.append(f"Transaction at unusual hour: {hour}:00")

        # Determine Risk Level
        if score >= 80:
            risk_level = "Critical Risk"
            color = "red"
            recommendation = "Block account and escalate for investigation"
        elif score >= 50:
            risk_level = "High Risk"
            color = "orange"
            recommendation = "Temporarily hold transaction and contact customer"
        elif score >= 25:
            risk_level = "Medium Risk"
            color = "yellow"
            recommendation = "Request OTP verification"
        else:
            risk_level = "Low Risk"
            color = "green"
            recommendation = "Approve transaction"
            
        return {
            'risk_score': min(score, 100),
            'risk_level': risk_level,
            'triggered_rules': triggered_rules,
            'recommendation': recommendation,
            'color': color
        }

if __name__ == "__main__":
    # Test
    engine = FraudRulesEngine()
    test_tx = {
        'Transaction Amount': 60000,
        'Average Customer Transaction Amount': 5000,
        'Transactions in Last 24 Hours': 6,
        'Failed Transaction Attempts': 4,
        'Is New Device': 1,
        'Is Unusual Location': 1,
        'Is International': 1,
        'Transaction Time': '02:30:00'
    }
    result = engine.evaluate_transaction(test_tx)
    print(f"Risk Score: {result['risk_score']}")
    print(f"Risk Level: {result['risk_level']}")
    print("Triggered Rules:")
    for rule in result['triggered_rules']:
        print(f"- {rule}")
