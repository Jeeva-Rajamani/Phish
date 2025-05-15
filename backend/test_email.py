from email_reporter import CybercrimeReporter

reporter = CybercrimeReporter()
success = reporter.send_report("Test phishing content", "test_phishing")
print("Email sent successfully!" if success else "Email failed to send")