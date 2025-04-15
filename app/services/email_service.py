import smtplib
from email.message import EmailMessage

from config.config import get_settings

settings = get_settings()


class EmailService:
    def __init__(self):
        self.address = settings.EMAIL_ADDRESS
        self.password = settings.EMAIL_PASSWORD

    def send_email(self, recipient: str, subject: str, body: str):
        msg = EmailMessage()
        msg["From"] = self.address
        msg["To"] = recipient
        msg["Subject"] = subject

        msg.set_content(body)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(self.address, self.password)
            smtp.send_message(msg)
