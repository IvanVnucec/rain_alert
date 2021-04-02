import yaml


def loadCredentials(path):
    email = None
    password = None

    try:
        with open(path, 'r') as file:
            credentials = yaml.load(file, Loader=yaml.FullLoader)

    except FileNotFoundError:
        exit('ERROR: credentials file not found.')

    else:
        return credentials['email'], credentials['password'], credentials['openWeatherApiKey']
