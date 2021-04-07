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


def get_receivers():
    try:
        with open(RECEIVERS_FILE_PATH, 'r') as file:
            lines = file.read().splitlines()

    except FileNotFoundError:
        exit('ERROR: email list file not found.')

    if lines:
        locations = {}

        for line in lines:
            line = line.partition(',')
            receiver = line[0].strip()
            location = line[2].replace('"', '').strip()

            if not location in locations:
                # create key, create empty list, append to list email
                locations[location] = []

            locations[location].append(receiver)

        return locations

    else:
        exit('ERROR: no emails list found.')
