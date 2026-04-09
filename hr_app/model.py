import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle
import os

def create_and_train_model():
    """
    Creates a synthetic dataset for employee turnover and trains a Random Forest model.
    """
    print("Generating synthetic data and training model...")
    np.random.seed(42)  # For reproducibility
    n_samples = 1000
    
    # Synthetic Features:
    # JobRole mapping -> 0: Developer, 1: Manager, 2: Sales, 3: HR
    data = {
        'Age': np.random.randint(22, 60, n_samples),
        'Salary': np.random.randint(40000, 150000, n_samples),
        'JobRole': np.random.randint(0, 4, n_samples),
        'YearsAtCompany': np.random.randint(0, 20, n_samples),
        'JobSatisfaction': np.random.randint(1, 6, n_samples),    # 1 to 5
        'WorkLifeBalance': np.random.randint(1, 6, n_samples),    # 1 to 5
        'PerformanceRating': np.random.randint(1, 6, n_samples),  # 1 to 5
    }
    
    df = pd.DataFrame(data)
    
    # Logic to compute target (Turnover: 1 = Leave, 0 = Stay)
    # Give penalty points for negative factors to calculate risk
    target = []
    for i in range(n_samples):
        risk_score = 0
        if df['JobSatisfaction'][i] <= 2: risk_score += 3
        if df['WorkLifeBalance'][i] <= 2: risk_score += 2
        if df['Salary'][i] < 60000: risk_score += 2
        # Underpaid high performers are highly likely to leave
        if df['YearsAtCompany'][i] > 3 and df['PerformanceRating'][i] >= 4 and df['Salary'][i] < 80000: 
            risk_score += 4
            
        # Add some random noise to make it realistic
        risk_score += np.random.randn() * 1.5
        
        # Threshold for leaving
        target.append(1 if risk_score >= 4.5 else 0)
        
    df['Turnover'] = target
    
    # Separation of features and target
    X = df.drop('Turnover', axis=1)
    y = df['Turnover']
    
    # Train test split (optional here since we use synthetic, but good practice)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train classification model
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    accuracy = clf.score(X_test, y_test)
    print(f"Model trained with accuracy: {accuracy*100:.2f}%")
    
    # Save the trained model to a file
    with open('model.pkl', 'wb') as f:
        pickle.dump(clf, f)
    print("Model saved as model.pkl")

def get_model():
    """
    Loads the trained model from disk, creating it if it doesn't exist.
    """
    if not os.path.exists('model.pkl'):
        create_and_train_model()
        
    with open('model.pkl', 'rb') as f:
        return pickle.load(f)

if __name__ == '__main__':
    # Run this file directly to generate the model
    create_and_train_model()
