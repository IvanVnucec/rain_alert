import yaml
import os

"""
# credentials.yaml file format
emailToSend: ...@gmail.com
password: ...
openWeatherApiKey: ...
emailToReceive: ...
"""
YAML_FILE_PATH = 'credentials.yaml'


def loadCredentials():
    # try with environment variables
    emailToSend = os.getenv('env_emailToSend')
    password = os.getenv('env_password')
    openWeatherApiKey = os.getenv('env_openWeatherApiKey')
    emailToReceive = os.getenv('env_emailToReceive')

    if emailToSend == None or password == None or openWeatherApiKey == None or emailToReceive == None:
        print('INFO: No credentials in environments variables, trying with credentials.yaml file...')
        try:
            with open(YAML_FILE_PATH, 'r') as file:
                credentials = yaml.load(file, Loader=yaml.FullLoader)

        except FileNotFoundError:
            exit('ERROR: credentials file not found.')

        else:
            emailToSend = credentials['emailToSend']
            password = credentials['password']
            openWeatherApiKey = credentials['openWeatherApiKey']
            emailToReceive = credentials['emailToReceive']

    return emailToSend, password, openWeatherApiKey, emailToReceive
