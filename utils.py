import yaml
import os

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


def load_emails_and_locations():
    try:
        with open(RECEIVERS_FILE_PATH, 'r') as email_list:
            receivers = email_list.read().splitlines()

    except FileNotFoundError:
        exit('ERROR: email list file not found.')

    if receivers:
        emails_and_locations = []

        for receiver in receivers:
            email_and_location = {}

            email_and_location['email'] = receiver.split(',')[0].strip()
            email_and_location['location'] = receiver.split(',')[1].strip()
            emails_and_locations.append(email_and_location)
        
        return emails_and_locations

    else:
        exit('ERROR: no emails list found.')
