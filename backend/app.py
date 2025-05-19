from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import tldextract
import urllib.parse
from transformers import pipeline
import logging
from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)
load_dotenv()

# Phishing detection configuration
PHISHING_KEYWORDS = {
    # High confidence indicators
    'verify': 3, 'account': 3, 'suspended': 3, 'limited': 3, 'unauthorized': 3,
    'locked': 3, 'expire': 3, 'reset': 3, 'confirm': 3, 'security': 3, 'payment': 3,
    'issue': 3, 'reconfirm': 3, 'secure my account': 3, 'unusual': 3,
    # Medium confidence indicators
    'login': 2, 'urgent': 2, 'action required': 2, 'click here': 2, 'detected': 2,
    # Low confidence indicators
    'support': 1, 'alert': 1, 'notice': 1, 'service': 1, 'secure': 1
}

LEGITIMATE_DOMAINS = {
    'paypal.com', 'apple.com', 'amazon.com', 'microsoft.com', 
    'github.com', 'linkedin.com', 'google.com', 'bankofamerica.com'
}

PHISHING_PATTERNS = [
    r'paypal[^\w]alert', r'apple[^\w]support', r'amazon[^\w]verify',
    r'microsoft[^\w]security', r'outlook[^\w]secure', r'account[^\w]verify',
    r'login[^\w]security', r'secure[^\w]login', r'update[^\w]account',
    r'verify[^\w]user', r'support[^\w]alert', r'alert[^\w]support'
]

class CybercrimeReporter:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("EMAIL_PASSWORD")
        self.recipient_email = os.getenv("RECIPIENT_EMAIL")
        
        if not all([self.sender_email, self.sender_password, self.recipient_email]):
            logger.error("Email configuration incomplete. Check .env file")

    def send_report(self, content, content_type):
        """Send phishing report via email"""
        try:
            if not all([self.sender_email, self.sender_password, self.recipient_email]):
                logger.error("Email configuration incomplete")
                return False

            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = self.recipient_email
            message["Subject"] = f"[URGENT] Phishing {content_type} Detected - {datetime.now().strftime('%Y-%m-%d %H:%M')}"

            body = f"""
            ===== PHISHING DETECTION ALERT =====
            
            Type: {content_type}
            Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            
            Content:
            {content}
            
            ===== END OF REPORT =====
            """
            message.attach(MIMEText(body, "plain"))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, self.recipient_email, message.as_string())
            
            logger.info(f"Report sent to {self.recipient_email}")
            return True

        except smtplib.SMTPAuthenticationError:
            logger.error("SMTP Authentication Failed. Please verify your email credentials in .env")
            return False
            
        except Exception as e:
            logger.error(f"Failed to send report: {str(e)}")
            return False

def is_legitimate_domain(url_or_email):
    """Check if domain is in whitelist"""
    try:
        if '@' in url_or_email:  # Email address
            domain = url_or_email.split('@')[-1].lower()
        else:  # URL
            extracted = tldextract.extract(url_or_email)
            domain = f"{extracted.domain}.{extracted.suffix}".lower()
        
        for legit_domain in LEGITIMATE_DOMAINS:
            if domain == legit_domain or domain.endswith(f".{legit_domain}"):
                return True
        return False
    except:
        return False

def analyze_domain_suspiciousness(url_or_email):
    """Check for suspicious domain patterns"""
    domain = ""
    try:
        if '@' in url_or_email:  # Email address
            domain = url_or_email.split('@')[-1].lower()
        else:  # URL
            extracted = tldextract.extract(url_or_email)
            domain = f"{extracted.domain}.{extracted.suffix}".lower()
        
        for pattern in PHISHING_PATTERNS:
            if re.search(pattern, domain):
                return True
                
        for legit_domain in LEGITIMATE_DOMAINS:
            if legit_domain.replace('.', '') in domain.replace('.', ''):
                if domain != legit_domain and not domain.endswith(f".{legit_domain}"):
                    return True
                    
        if any(legit in domain for legit in ['paypal', 'apple', 'amazon', 'microsoft']):
            if not domain.endswith(('.com', '.net', '.org', '.edu', '.gov')):
                return True
                
        return False
    except:
        return False

def keyword_analysis(content):
    """Score content based on phishing keywords"""
    score = 0
    content_lower = content.lower()
    
    for word, points in PHISHING_KEYWORDS.items():
        if word in content_lower:
            score += points
    
    return score

def analyze_url(url):
    """Specialized URL analysis"""
    if is_legitimate_domain(url):
        return False
        
    if analyze_domain_suspiciousness(url):
        return True
        
    parsed = urllib.parse.urlparse(url)
    
    if re.match(r'\d+\.\d+\.\d+\.\d+', parsed.netloc):
        return True
        
    if '@' in url:
        return True
        
    if parsed.netloc.count('.') > 3:
        return True
        
    if keyword_analysis(url) >= 5:
        return True
        
    return False

def analyze_email(email_content):
    """Specialized email analysis"""
    sender_match = re.search(r'From:\s*(.*?)\n', email_content, re.IGNORECASE)
    if sender_match:
        sender = sender_match.group(1).strip()
        if analyze_domain_suspiciousness(sender):
            return True
    
    subject_match = re.search(r'Subject:\s*(.*?)\n', email_content, re.IGNORECASE)
    if subject_match:
        subject = subject_match.group(1).strip()
        if keyword_analysis(subject) >= 5:
            return True
    
    body = re.sub(r'^(From:|Subject:).*?\n', '', email_content, flags=re.IGNORECASE|re.MULTILINE)
    if keyword_analysis(body) >= 7:
        return True
        
    url_matches = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', email_content)
    for url in url_matches:
        if analyze_url(url):
            return True
            
    return False

# Load BERT model
try:
    bert_model = pipeline(
        "text-classification", 
        model="ealvaradob/bert-finetuned-phishing",
        device=-1
    )
except Exception as e:
    logger.error(f"Failed to load BERT model: {str(e)}")
    bert_model = None

@app.route('/check_url', methods=['POST'])
def check_url_endpoint():
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'result': 'error', 'message': 'URL required'}), 400

        if analyze_url(url):
            reporter = CybercrimeReporter()
            email_sent = reporter.send_report(url, 'phishing_url')
            return jsonify({
                'result': 'phishing',
                'message': '⚠️ Phishing URL Detected!',
                'report_sent': email_sent,
                'method': 'pattern analysis'
            })
        
        if bert_model:
            result = bert_model(url[:512])
            if result[0]['label'] == 'LABEL_1' and result[0]['score'] > 0.85:
                reporter = CybercrimeReporter()
                email_sent = reporter.send_report(url, 'phishing_url')
                return jsonify({
                    'result': 'phishing',
                    'message': '⚠️ Phishing URL Detected!',
                    'report_sent': email_sent,
                    'method': 'BERT model',
                    'confidence': f"{result[0]['score']:.2f}"
                })
        
        return jsonify({
            'result': 'legitimate',
            'message': '✅ URL appears safe'
        })
        
    except Exception as e:
        logger.error(f"URL check error: {str(e)}")
        return jsonify({'result': 'error', 'message': str(e)}), 500

@app.route('/check_email', methods=['POST'])
def check_email_endpoint():
    try:
        data = request.get_json()
        email_content = data.get('email', '').strip()
        
        if not email_content:
            return jsonify({'result': 'error', 'message': 'Email content required'}), 400

        if analyze_email(email_content):
            reporter = CybercrimeReporter()
            email_sent = reporter.send_report(email_content, 'phishing_email')
            return jsonify({
                'result': 'phishing',
                'message': '⚠️ Phishing Email Detected!',
                'report_sent': email_sent,
                'method': 'pattern analysis'
            })
        
        if bert_model:
            result = bert_model(email_content[:512])
            if result[0]['label'] == 'LABEL_1' and result[0]['score'] > 0.85:
                reporter = CybercrimeReporter()
                email_sent = reporter.send_report(email_content, 'phishing_email')
                return jsonify({
                    'result': 'phishing',
                    'message': '⚠️ Phishing Email Detected!',
                    'report_sent': email_sent,
                    'method': 'BERT model',
                    'confidence': f"{result[0]['score']:.2f}"
                })
        
        return jsonify({
            'result': 'legitimate',
            'message': '✅ Email appears safe'
        })
        
    except Exception as e:
        logger.error(f"Email check error: {str(e)}")
        return jsonify({'result': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    logger.info("\n🚀 Starting PhishDetect Server...")
    logger.info("📧 Email reporting configured to: " + os.getenv("RECIPIENT_EMAIL", "NOT SET"))
    app.run(host='0.0.0.0', port=5000, debug=True)