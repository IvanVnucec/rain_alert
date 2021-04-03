import yaml

CREDENTIALS_FILE_PATH = 'CREDENTIALS.yaml'
RECEIVERS_FILE_PATH = 'RECEIVERS.txt'


def load_credentials():
    try:
        with open(CREDENTIALS_FILE_PATH, 'r') as file:
            credentials = yaml.load(file, Loader=yaml.FullLoader)

    except FileNotFoundError:
        exit('ERROR: credentials file not found.')

    sender = credentials['senderEmail']
    password = credentials['senderPassword']
    openWeatherApiKey = credentials['openWeatherApiKey']

    return sender, password, openWeatherApiKey


def load_emails():
    try:
        with open(RECEIVERS_FILE_PATH, 'r') as email_list:
            receivers = email_list.read().splitlines()

    except FileNotFoundError:
        exit('ERROR: email list file not found.')

    if receivers:
        return receivers

    else:
        exit('ERROR: no emails list found.')
