import utils
from gmail import Gmail
from forecast import Forecast
from location import Location

SEND_EMAIL_HOUR = 5  # AM local time
CREDENTIALS_FILE_PATH = 'CREDENTIALS.yaml'
RECEIVERS_FILE_PATH = 'RECEIVERS.txt'

if __name__ == "__main__":
    sender, password, openWeatherApiKey = utils.get_credentials(
        CREDENTIALS_FILE_PATH)
    receivers = utils.get_emails_and_locations(RECEIVERS_FILE_PATH)

    gmail = Gmail(sender, password)
    forecast = Forecast(openWeatherApiKey)

    for receiver in receivers:
        location = Location(receiver['location'])

        # is it time to send an email
        if location.get_local_time().hour == SEND_EMAIL_HOUR:
            forecastToday = forecast.get_forecast_today(location)

            if forecast.rain_today(forecastToday):
                subject, content, contentHtml = forecast.construct_forecast_message(
                    forecastToday, location)
                print('INFO: Sending emails.')
                gmail.send(receiver['email'], subject, content, contentHtml)

    print('INFO: Done.')
