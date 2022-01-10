import yaml
from os import path, getenv

DEBUG = True
CREDENTIALS_FILE_PATH = path.abspath(
    path.join('credentials', 'credentials.yaml'))
RECEIVERS_FILE_PATH = path.abspath(path.join('credentials', 'receivers.txt'))
ACTION_URL_ENV = 'ACTION_URL' # defined in weather_check.yml


def get_email_credentials():
    try:
        with open(CREDENTIALS_FILE_PATH, 'r') as file:
            credentials = yaml.load(file, Loader=yaml.FullLoader)
    except:
        error(
            f"Could not open {CREDENTIALS_FILE_PATH}. Check if the file exist with the correct name.")

    try:
        sender = credentials['senderEmail']
        password = credentials['senderPassword']
    except:
        error("Could not retrieve Email or Email password from the Credentials file.")

    return sender, password


def get_openWeather_api_key():
    try:
        with open(CREDENTIALS_FILE_PATH, 'r') as file:
            credentials = yaml.load(file, Loader=yaml.FullLoader)
    except:
        error(
            f"Could not open {CREDENTIALS_FILE_PATH}. Check if the file exist with the correct name.")

    try:
        key = credentials['openWeatherApiKey']
    except:
        error("Could not get the OpenWeather API key from Credentials file.")

    return key


def get_receivers():
    try:
        with open(RECEIVERS_FILE_PATH, 'r') as file:
            lines = file.read().splitlines()
    except FileNotFoundError:
            error(f"Could not open {RECEIVERS_FILE_PATH}. Check if the file exist with the correct name.")
    else:
        locations = {}

        for line in lines:
            receiver, _, location = line.partition(',')
            receiver = receiver.strip()
            location = location.strip()

            if not location in locations:
                locations[location] = []

            locations[location].append(receiver)

        return locations


def get_github_actions_url():
    action_url = getenv(ACTION_URL_ENV)
    if action_url is None:
        debug('Cannot get GitHub Actions link')
        action_url = ''
    
    return action_url


def debug(msg):
    if DEBUG:
        if type(msg) is dict:
            print('DEBUG: ')
            print(msg)
        else:
            print('DEBUG: ' + msg)


def error(msg):
    exit('ERROR: ' + msg)
