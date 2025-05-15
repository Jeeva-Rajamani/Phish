import pandas as pd
from datetime import datetime
from pathlib import Path
import os
from email_reporter import CybercrimeReporter

def report_to_cybercrime(content, content_type):
    """
    Comprehensive reporting system that:
    - Saves to local CSV
    - Sends email alert
    - Returns detailed status
    """
    report_status = {
        'file_saved': False,
        'email_sent': False,
        'error': None
    }

    try:
        # File system reporting
        backend_dir = Path(__file__).parent
        reports_dir = backend_dir / 'reports'
        reports_dir.mkdir(exist_ok=True, mode=0o755)
        
        report_file = reports_dir / 'reported_phishing.csv'
        
        new_entry = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'type': content_type,
            'content': content,
            'status': 'reported'
        }

        # Save to CSV
        try:
            if report_file.exists():
                df = pd.read_csv(report_file)
                df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
            else:
                df = pd.DataFrame([new_entry])
            
            df.to_csv(report_file, index=False)
            report_status['file_saved'] = True
            print(f"✅ Report saved to {report_file}")
        except Exception as e:
            report_status['error'] = f"File save error: {str(e)}"
            print(f"❌ Could not save report: {str(e)}")

        # Email reporting
        try:
            reporter = CybercrimeReporter()
            report_status['email_sent'] = reporter.send_report(content, content_type)
        except Exception as e:
            report_status['error'] = f"Email error: {str(e)}" if not report_status['error'] else report_status['error']

        return report_status

    except Exception as e:
        report_status['error'] = str(e)
        return report_status