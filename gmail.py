import smtplib
import ssl
from email import message_from_string


class Gmail:
    SSL_PORT = 465
    SMTP_GMAIL = 'smtp.gmail.com'

    def __init__(self, email, password) -> None:
        self.loginSuccessfull = False
        self.email = email

        context = ssl.create_default_context()
        self.server = smtplib.SMTP_SSL(
            self.SMTP_GMAIL, self.SSL_PORT, context=context)
        try:
            self.server.login(self.email, password)
        except smtplib.SMTPAuthenticationError as error:
            exit('ERROR: Wrong username or password.')
        else:
            self.loginSuccessfull = True

    def send(self, message, receiver_email):
        if self.loginSuccessfull:
            email_msg = message_from_string(message)
            self.server.send_message(
                email_msg, self.email, receiver_email)
        else:
            exit('ERROR: To send en email, you first need to login.')
