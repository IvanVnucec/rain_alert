import smtplib
import ssl
from email.message import EmailMessage


SSL_PORT = 465
SMTP_GMAIL = 'smtp.gmail.com'


class Gmail:
    def __init__(self, sender_email, password):
        self.sender = sender_email

        context = ssl.create_default_context()
        self.__server = smtplib.SMTP_SSL(SMTP_GMAIL, SSL_PORT, context=context)

        try:
            self.__server.login(self.sender, password)
        except smtplib.SMTPAuthenticationError:
            exit('ERROR: Wrong username or password.')

    def send(self, receiver, subject, content):
        message = EmailMessage()

        message['From'] = self.sender
        message['To'] = receiver
        message['Subject'] = subject
        message.set_content(content)

        self.__server.send_message(message, self.sender, receiver)
