from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import os
from pathlib import Path
from cybercrime_report import report_to_cybercrime  # <-- Add this import
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS

# Configure paths
BASE_DIR = Path(__file__).parent
MODEL_DIR = BASE_DIR / 'ml_models' / 'models'
REPORTS_DIR = BASE_DIR / 'reports'

# Load models
try:
    url_model = joblib.load(MODEL_DIR / 'url_model.pkl')
    url_vectorizer = joblib.load(MODEL_DIR / 'url_vectorizer.pkl')
    email_model = joblib.load(MODEL_DIR / 'email_model.pkl')
    email_vectorizer = joblib.load(MODEL_DIR / 'email_vectorizer.pkl')
    print("✅ All models loaded successfully!")
except Exception as e:
    print(f"❌ Error loading models: {str(e)}")
    exit(1)

@app.route('/check_url', methods=['POST'])
def check_url():
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({
                'result': 'error',
                'message': 'Please enter a URL to check'
            }), 400

        # Analyze URL
        features = url_vectorizer.transform([url])
        prediction = url_model.predict(features)[0]
        
        if prediction == 1:  # Phishing
            report_status = report_to_cybercrime(url, 'reported_phishing.csv')  # <-- Add this line
            return jsonify({
                'result': 'phishing',
                'message': '⚠️ Dangerous URL Detected!\n• This appears to be a phishing site\n• Do not enter personal information\n• Reported to cybercrime authorities',
                'reported': report_status  # <-- Include report status in response
            })
        else:  # Legitimate
            return jsonify({
                'result': 'legitimate',
                'message': '✅ This URL appears safe\n• No phishing indicators detected\n• Always verify before entering sensitive data'
            })
            
    except Exception as e:
        return jsonify({
            'result': 'error',
            'message': f'🔧 Detection error\n• {str(e)}\n• Please try again'
        }), 500

@app.route('/check_email', methods=['POST'])
def check_email():
    try:
        data = request.get_json()
        email_content = data.get('email', '').strip()
        
        if not email_content:
            return jsonify({
                'result': 'error',
                'message': 'Please enter email content to analyze'
            }), 400

        # Analyze email
        features = email_vectorizer.transform([email_content])
        prediction = email_model.predict(features)[0]
        
        if prediction == 1:  # Phishing
            report_status = report_to_cybercrime(email_content, 'phishing_email.csv')  # <-- Add this line
            return jsonify({
                'result': 'phishing',
                'message': '⚠️ Phishing Email Detected!\n• Contains suspicious elements\n• Do not click links/attachments\n• Reported to cybercrime authorities',
                'reported': report_status  # <-- Include report status in response
            })
        else:  # Legitimate
            return jsonify({
                'result': 'legitimate',
                'message': '✅ This email appears safe\n• No phishing indicators detected\n• Remain cautious with unexpected emails'
            })
            
    except Exception as e:
        return jsonify({
            'result': 'error',
            'message': f'🔧 Detection error\n• {str(e)}\n• Please try again'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)