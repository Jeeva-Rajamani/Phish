from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from pathlib import Path
from datetime import datetime
from email_reporter import CybercrimeReporter
import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load environment variables
load_dotenv()

# Configuration
BASE_DIR = Path(__file__).parent
MODEL_DIR = BASE_DIR / 'ml_models' / 'models'
REPORTS_DIR = BASE_DIR / 'reports'

# Ensure directories exist
MODEL_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

# Load models
try:
    logger.info("Loading machine learning models...")
    url_model = joblib.load(MODEL_DIR / 'url_model.pkl')
    url_vectorizer = joblib.load(MODEL_DIR / 'url_vectorizer.pkl')
    email_model = joblib.load(MODEL_DIR / 'email_model.pkl')
    email_vectorizer = joblib.load(MODEL_DIR / 'email_vectorizer.pkl')
    logger.info("Models loaded successfully!")
except Exception as e:
    logger.error(f"Failed to load models: {str(e)}")
    exit(1)

@app.route('/check_url', methods=['POST'])
def check_url():
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'result': 'error', 'message': 'URL required'}), 400

        # Analyze URL
        features = url_vectorizer.transform([url])
        prediction = url_model.predict(features)[0]
        
        if prediction == 1:  # Phishing
            reporter = CybercrimeReporter()
            email_sent = reporter.send_report(url, 'phishing_url')
            
            return jsonify({
                'result': 'phishing',
                'message': '⚠️ Phishing URL Detected!',
                'report_status': {
                    'email_sent': email_sent,
                    'actions': [
                        'Reported to cybercrime authorities',
                        'Do not enter personal information'
                    ]
                }
            })
        else:
            return jsonify({
                'result': 'legitimate',
                'message': '✅ URL appears safe'
            })
            
    except Exception as e:
        logger.error(f"URL check error: {str(e)}")
        return jsonify({'result': 'error', 'message': str(e)}), 500

@app.route('/check_email', methods=['POST'])
def check_email():
    try:
        data = request.get_json()
        email_content = data.get('email', '').strip()
        
        if not email_content:
            return jsonify({'result': 'error', 'message': 'Email content required'}), 400

        # Analyze email
        features = email_vectorizer.transform([email_content])
        prediction = email_model.predict(features)[0]
        
        if prediction == 1:  # Phishing
            reporter = CybercrimeReporter()
            email_sent = reporter.send_report(email_content, 'phishing_email')
            
            return jsonify({
                'result': 'phishing',
                'message': '⚠️ Phishing Email Detected!',
                'report_status': {
                    'email_sent': email_sent,
                    'actions': [
                        'Reported to cybercrime authorities',
                        'Do not click links or attachments'
                    ]
                }
            })
        else:
            return jsonify({
                'result': 'legitimate',
                'message': '✅ Email appears safe'
            })
            
    except Exception as e:
        logger.error(f"Email check error: {str(e)}")
        return jsonify({'result': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    logger.info("\n🚀 Starting PhishDetect Server...")
    logger.info(f"📂 Models loaded from: {MODEL_DIR}")
    logger.info(f"📧 Email reports will be sent to: {os.getenv('RECIPIENT_EMAIL')}")
    app.run(host='0.0.0.0', port=5000, debug=False)