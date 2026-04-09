from flask import Flask, request, jsonify, render_template
import numpy as np
from model import get_model

# Initialize Flask application
app = Flask(__name__)

# Load our saved Machine Learning model
model = get_model()

@app.route('/')
def home():
    """Renders the main dashboard webpage."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    API Endpoint that accepts JSON data, runs the ML model prediction,
    and returns the risk level and retention strategies.
    """
    try:
        # 1. Receive data from the frontend
        data = request.json
        print("Received prediction request:", data)
        
        # 2. Extract and format features for the ML model
        age = float(data.get('Age'))
        salary = float(data.get('Salary'))
        job_role = int(data.get('JobRole'))
        years = float(data.get('YearsAtCompany'))
        satisfaction = float(data.get('JobSatisfaction'))
        wlb = float(data.get('WorkLifeBalance'))
        performance = float(data.get('PerformanceRating'))
        
        # The order must match the training data features
        features = np.array([[age, salary, job_role, years, satisfaction, wlb, performance]])
        
        # 3. Make prediction
        # predict_proba returns probabilities for [Class 0 (Stay), Class 1 (Leave)]
        prob_leave = model.predict_proba(features)[0][1] 
        
        # 4. Analyze Prediction and Set Strategies
        prediction_text = "Yes" if prob_leave > 0.5 else "No"
        
        # Define Risk Levels and correspond Retention Strategies
        if prob_leave >= 0.7:
            risk_level = "High"
            strategies = [
                "URGENT: Suggest an immediate salary increase or compensation review.",
                "Offer a role change or distinct promotion opportunities.",
                "Create a personalized career development plan with leadership.",
                "Schedule a 1-on-1 meeting immediately to proactively discuss concerns."
            ]
        elif prob_leave >= 0.4:
            risk_level = "Medium"
            strategies = [
                "Provide opportunities for training programs and upskilling.",
                "Focus on work-life balance improvements (e.g., flexible hours, remote options).",
                "Conduct regular check-ins to monitor job satisfaction.",
                "Publicly recognize recent achievements."
            ]
        else:
            risk_level = "Low"
            strategies = [
                "Continue standard recognition and rewards for good performance.",
                "Maintain current engagement strategies and team building.",
                "Encourage mentorship roles to keep the employee engaged and valued."
            ]
            
        # 5. Send result back to frontend
        return jsonify({
            'prediction': prediction_text,
            'risk_level': risk_level,
            'probability': round(prob_leave * 100, 2),
            'strategies': strategies
        })
        
    except Exception as e:
        print("Error during prediction:", e)
        # Return a 400 Bad Request error if something goes wrong
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    # Start the Flask web server
    print("Starting Flask API Server...")
    app.run(debug=True, port=5000)
