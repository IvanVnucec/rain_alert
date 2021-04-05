import utils
from gmail import Gmail
from forecast import Forecast

CREDENTIALS_FILE_PATH = 'CREDENTIALS.yaml'
RECEIVERS_FILE_PATH = 'RECEIVERS.txt'

if __name__ == "__main__":
    sender, password, openWeatherApiKey = utils.get_credentials(CREDENTIALS_FILE_PATH)
    receivers = utils.get_emails_and_locations(RECEIVERS_FILE_PATH)

    gmail = Gmail(sender, password)
    forecast = Forecast(openWeatherApiKey)

    if forecast.rain_today():
        subject, content, contentHtml = forecast.construct_forecast_message()

        for receiver in receivers:
            gmail.send(receiver, subject, content, contentHtml)
    else:
        print('INFO: No rain today in Zagreb.')
