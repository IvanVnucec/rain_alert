import smtplib
import ssl
from email import message_from_string


class Gmail:
    SSL_PORT = 465
    SMTP_GMAIL = 'smtp.gmail.com'

    def __init__(self) -> None:
        self.login_successfully = False

    def login(self, email, password):
        self.email = email
        self.__password = password

    def send(self, message, receiver_email):
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(self.SMTP_GMAIL, self.SSL_PORT, context=context) as server:
            try:
                server.login(self.email, self.__password)

            except smtplib.SMTPAuthenticationError as error:
                print('ERROR: Wrong username or password.')

            else:
                email_msg = message_from_string(message)
                server.send_message(
                    email_msg, self.email, receiver_email)
