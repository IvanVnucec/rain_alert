import yaml
import os

"""
# credentials.yaml file format
email: ...@gmail.com
password: ...
openWeatherApiKey: ...
"""
YAML_FILE_PATH = 'credentials.yaml'

def loadCredentials():
    # try with environment variables
    email = os.getenv('env_email')
    password = os.getenv('env_password')
    openWeatherApiKey = os.getenv('env_openWeatherApiKey')

    if email == None or password == None or openWeatherApiKey == None:
        # else try with .yaml file
        try:
            with open(YAML_FILE_PATH, 'r') as file:
                credentials = yaml.load(file, Loader=yaml.FullLoader)

        except FileNotFoundError:
            exit('ERROR: credentials file not found.')

        else:
            return credentials['email'], credentials['password'], credentials['openWeatherApiKey']
