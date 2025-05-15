import pandas as pd
from datetime import datetime
from pathlib import Path
import os

def report_to_cybercrime(content, content_type):
    """
    Save phishing reports to CSV with proper file path handling
    
    Args:
        content (str): The URL or email content to report
        content_type (str): Either 'phishing_url' or 'phishing_email'
    Returns:
        bool: True if report was successful, False otherwise
    """
    try:
        # Get the absolute path to the backend directory
        backend_dir = Path(__file__).parent
        reports_dir = backend_dir / 'reports'
        reports_dir.mkdir(exist_ok=True)
        
        report_file = reports_dir / 'reported_phishing.csv'
        
        # Prepare new report data
        new_report = {
            'timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            'type': [content_type],
            'content': [content],
            'status': ['reported']
        }
        
        df_new = pd.DataFrame(new_report)
        
        # Try to append to existing file
        if report_file.exists():
            try:
                df_existing = pd.read_csv(report_file)
                df_combined = pd.concat([df_existing, df_new], ignore_index=True)
                df_combined.to_csv(report_file, index=False)
            except Exception as e:
                print(f"Warning: Could not read existing report file. Creating new one. Error: {str(e)}")
                df_new.to_csv(report_file, index=False)
        else:
            df_new.to_csv(report_file, index=False)
            
        print(f"✅ Report saved to: {report_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error saving report: {str(e)}")
        return False