import utils
from gmail import Gmail
from open_weather import OpenWeather
from datetime import datetime
import pytz
from email.message import EmailMessage

DAY_START_HOUR = 6
DAY_END_HOUR = 23
RAIN_PROB_TRESH = 0.5
ZAGREB_TIMEZONE = 'Europe/Zagreb'


def get_forecast_today(forecast):
    forecastToday = []

    localTimeNow = datetime.now(pytz.timezone(ZAGREB_TIMEZONE))

    for forecast in forecast:
        forecastTime = forecast['t']
        probability = forecast['p']
        sameDayForecast = localTimeNow.day == forecastTime.day
        inTimeRange = forecastTime.hour >= DAY_START_HOUR and forecastTime.hour <= DAY_END_HOUR
        highRainProbability = probability >= RAIN_PROB_TRESH

        val = {}
        if sameDayForecast and inTimeRange and highRainProbability:
            val = {'bool': True, 'p': probability, 't': forecastTime}
        else:
            val = {'bool': False, 'p': probability, 't': forecastTime}

        forecastToday.append(val)

    return forecastToday


def get_rain_start_hour(forecastToday):
    for forecast in forecastToday:
        if forecast['bool']:
            return forecast['t'].hour


def construct_message(sender, receiver, forecastToday):
    message = EmailMessage()

    message['From'] = sender
    message['To'] = receiver

    rainStartHour = get_rain_start_hour(forecastToday)
    message['Subject'] = f'Rain in Zagreb from {rainStartHour}h'

    content = ''
    for forecast in forecastToday:
        hour = forecast['t'].hour
        probability = forecast['p'] * 100

        content += f'{hour}h {probability}%'
        content += '\n'

    message.set_content(content)

    return message


def rain_today(forecastToday):
    return True in [rain['bool'] for rain in forecastToday]


if __name__ == "__main__":
    sender, password, openWeatherApiKey = utils.load_credentials()
    receivers = utils.load_emails()

    gmail = Gmail(sender, password)
    openWeather = OpenWeather(openWeatherApiKey)

    forecast = openWeather.get_forecast()
    forecastToday = get_forecast_today(forecast)

    if rain_today(forecastToday):
        for receiver in receivers:
            message = construct_message(sender, receiver, forecastToday)
            gmail.send(receiver, message)
    else:
        print('INFO: No rain today in Zagreb.')
