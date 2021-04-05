import yaml

CREDENTIALS_FILE_PATH = 'CREDENTIALS.yaml'
RECEIVERS_FILE_PATH = 'RECEIVERS.txt'

def get_credentials(filePath):
    try:
        with open(filePath, 'r') as file:
            credentials = yaml.load(file, Loader=yaml.FullLoader)

    except FileNotFoundError:
        exit('ERROR: credentials file not found.')

    sender = credentials['senderEmail']
    password = credentials['senderPassword']
    openWeatherApiKey = credentials['openWeatherApiKey']

    return sender, password, openWeatherApiKey


def get_emails_and_locations(filePath):
    try:
        with open(filePath, 'r') as file:
            receivers = file.read().splitlines()

    except FileNotFoundError:
        exit('ERROR: email list file not found.')

    if receivers:
        return receivers

    else:
        exit('ERROR: no emails list found.')
