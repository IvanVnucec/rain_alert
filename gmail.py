import smtplib
import ssl
from email import message_from_string


class Gmail:
    __SSL_PORT = 465
    __SMTP_GMAIL = 'smtp.gmail.com'

    def __init__(self, email, password) -> None:
        self.loginSuccessfull = False
        self.email = email

        context = ssl.create_default_context()
        self.__server = smtplib.SMTP_SSL(
            self.__SMTP_GMAIL, self.__SSL_PORT, context=context)
        try:
            self.__server.login(self.email, password)
        except smtplib.SMTPAuthenticationError as error:
            exit('ERROR: Wrong username or password.')
        else:
            self.loginSuccessfull = True

    def send(self, message, receiver_email):
        if self.loginSuccessfull:
            email_msg = message_from_string(message)
            self.__server.send_message(
                email_msg, self.email, receiver_email)
        else:
            exit('ERROR: To send en email, you first need to login.')
