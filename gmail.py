import smtplib
import ssl
from email.message import EmailMessage


SSL_PORT = 465
SMTP_GMAIL = 'smtp.gmail.com'


class Gmail:
    def __init__(self, sender_email, password):
        self.loginSuccessfull = False
        self.sender = sender_email

        context = ssl.create_default_context()
        self.__server = smtplib.SMTP_SSL(SMTP_GMAIL, SSL_PORT, context=context)

        try:
            self.__server.login(self.sender, password)
        except smtplib.SMTPAuthenticationError:
            exit('ERROR: Wrong username or password.')
        else:
            self.loginSuccessfull = True

    def send(self, receiver, subject, message):
        if self.loginSuccessfull:
            msg = EmailMessage()
            msg['From'] = self.sender
            msg['Subject'] = subject
            msg.set_content(message)
            msg['To'] = receiver

            self.__server.send_message(msg, self.sender, receiver)

        else:
            exit('ERROR: To send en email, you first need to login.')
