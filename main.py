import utils
from gmail import Gmail
from forecast import Forecast


if __name__ == "__main__":
    sender, password, openWeatherApiKey = utils.load_credentials()
    receivers = utils.load_emails()

    gmail = Gmail(sender, password)
    forecast = Forecast(openWeatherApiKey)

    if forecast.rain_today():
        subject, content, contentHtml = forecast.construct_forecast_message()

        for receiver in receivers:
            gmail.send(receiver, subject, content, contentHtml)
    else:
        print('INFO: No rain today in Zagreb.')
