import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class CybercrimeReporter:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("EMAIL_PASSWORD")
        self.recipient_email = os.getenv("RECIPIENT_EMAIL")
        
        # Validate configuration
        if not all([self.sender_email, self.sender_password, self.recipient_email]):
            logger.error("Email configuration incomplete. Check .env file")

    def send_report(self, content, content_type):
        """Send phishing report via email with enhanced error handling"""
        try:
            if not all([self.sender_email, self.sender_password, self.recipient_email]):
                logger.error("Email configuration incomplete")
                return False

            # Create message
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = self.recipient_email
            message["Subject"] = f"[URGENT] Phishing {content_type} Detected - {datetime.now().strftime('%Y-%m-%d %H:%M')}"

            # Email body
            body = f"""
            ===== PHISHING DETECTION ALERT =====
            
            Type: {content_type}
            Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            
            Content:
            Subject: Reporting Phishing Email/URL for Investigation

            Dear Cybercrime Cell,

            I would like to report a phishing incident for your attention.
            {content}
            
            
            ===== END OF REPORT =====
            """
            message.attach(MIMEText(body, "plain"))

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            logger.info(f"Email alert sent to {self.recipient_email}")
            return True

        except smtplib.SMTPAuthenticationError:
            logger.error("""
            SMTP Authentication Failed. Please verify:
            1. You enabled 2-Step Verification on your Google account
            2. You created an App Password (not your regular password)
            3. The App Password is correctly set in .env file
            """)
            return False
            
        except Exception as e:
            logger.error(f"Email sending failed: {str(e)}")
            return False