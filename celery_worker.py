from celery import Celery
import smtplib
from email.mime.text import MIMEText
from config import Config

celery = Celery('tasks', broker=Config.CELERY_BROKER_URL)
celery.conf.result_backend = Config.CELERY_RESULT_BACKEND

@celery.task
def send_email(recipient):
    subject = "Email from Messaging System for Abasifreke Nkanang"
    body = "This is a test email sent from the Messaging System."
    sender = Config.SMTP_USERNAME

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    try:
        with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
            server.set_debuglevel(1)
            server.starttls()
            server.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
            server.sendmail(sender, recipient, msg.as_string())
        return f"Email sent successfully to {recipient}"
    except smtplib.SMTPAuthenticationError as e:
        error_msg = f"SMTP Authentication failed. Error: {str(e)}"
        return error_msg
    except smtplib.SMTPException as e:
        error_msg = f"SMTP error occurred: {str(e)}"
        return error_msg
    except Exception as e:
        error_msg = f"An unexpected error occurred: {str(e)}"
        return error_msg
