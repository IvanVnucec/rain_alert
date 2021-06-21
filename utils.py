import yaml

CREDENTIALS_FILE_PATH = 'credentials.yaml'
RECEIVERS_FILE_PATH = 'receivers.txt'


def get_email_credentials():
    try:
        with open(CREDENTIALS_FILE_PATH, 'r') as file:
            credentials = yaml.load(file, Loader=yaml.FullLoader)

    except FileNotFoundError:
        error('Credentials file not found.')

    sender = credentials['senderEmail']
    password = credentials['senderPassword']

    return sender, password


def get_openWeather_api_key():
    try:
        with open(CREDENTIALS_FILE_PATH, 'r') as file:
            credentials = yaml.load(file, Loader=yaml.FullLoader)

    except FileNotFoundError:
        error('Credentials file not found.')

    return credentials['openWeatherApiKey']


def get_receivers():
    try:
        with open(RECEIVERS_FILE_PATH, 'r') as file:
            lines = file.read().splitlines()

    except FileNotFoundError:
        error('Email list file not found.')

    if lines:
        locations = {}

        for line in lines:
            receiver, _, location = line.partition(',')
            receiver = receiver.strip()
            location = location.strip()

            if not location in locations:
                locations[location] = []

            locations[location].append(receiver)

        return locations

    else:
        error('No emails list found.')


def debug(msg):
    print('DEBUG: ' + msg)


def error(msg):
    exit('ERROR: ' + msg)