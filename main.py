from gmail import Gmail
from load_credentials import loadCredentials


gmail = Gmail()

# load gmail credentials from credentials.yaml file
email, password = loadCredentials('credentials.yaml')

gmail.login(email, password)
gmail.send('test message', email)
