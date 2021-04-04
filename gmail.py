import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


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

    def send(self, receiver, subject, content, contentHtml=None):
        message = MIMEMultipart("alternative")

        message['From'] = self.sender
        message['To'] = receiver
        message['Subject'] = subject

        message.attach(MIMEText(content, "plain"))
        
        if contentHtml:
            message.attach(MIMEText(contentHtml, "html"))

        self.__server.send_message(message, self.sender, receiver)
