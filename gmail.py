import smtplib
import ssl
from email.message import EmailMessage


__SSL_PORT = 465
__SMTP_GMAIL = 'smtp.gmail.com'


class Gmail:
    def __init__(self, sender_email, password):
        self.loginSuccessfull = False
        self.sender = sender_email

        context = ssl.create_default_context()
        self.__server = smtplib.SMTP_SSL(
            __SMTP_GMAIL, __SSL_PORT, context=context)
        try:
            self.__server.login(self.sender, password)
        except smtplib.SMTPAuthenticationError as error:
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
