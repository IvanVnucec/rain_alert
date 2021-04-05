import yaml

CREDENTIALS_FILE_PATH = 'CREDENTIALS.yaml'
RECEIVERS_FILE_PATH = 'RECEIVERS.txt'


def get_email_credentials():
    try:
        with open(CREDENTIALS_FILE_PATH, 'r') as file:
            credentials = yaml.load(file, Loader=yaml.FullLoader)

    except FileNotFoundError:
        exit('ERROR: credentials file not found.')

    sender = credentials['senderEmail']
    password = credentials['senderPassword']

    return sender, password


def get_openWeather_api_key():
    try:
        with open(CREDENTIALS_FILE_PATH, 'r') as file:
            credentials = yaml.load(file, Loader=yaml.FullLoader)

    except FileNotFoundError:
        exit('ERROR: credentials file not found.')

    return credentials['openWeatherApiKey']


def get_emails_and_locations():
    try:
        with open(RECEIVERS_FILE_PATH, 'r') as file:
            receivers = file.read().splitlines()

    except FileNotFoundError:
        exit('ERROR: email list file not found.')

    if receivers:
        emails_and_locations = []

        for receiver in receivers:
            email_and_location = {}
            string = receiver.partition(',')
            email_and_location['email'] = string[0].strip()
            email_and_location['location'] = string[2].replace('"', '').strip()
            emails_and_locations.append(email_and_location)

        return emails_and_locations

    else:
        exit('ERROR: no emails list found.')
