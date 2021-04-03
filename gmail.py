import smtplib
import ssl
from email.message import EmailMessage


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
            email_msg = EmailMessage()
            email_msg.set_content(message)
            email_msg['Subject'] = message
            email_msg['From'] = self.email
            email_msg['To'] = receiver_email
            self.__server.send_message(
                email_msg, self.email, receiver_email)
            self.__server.quit()
        else:
            exit('ERROR: To send en email, you first need to login.')
