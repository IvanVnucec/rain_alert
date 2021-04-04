import utils
from gmail import Gmail
from open_weather import OpenWeather
from datetime import datetime
import pytz


DAY_START_HOUR = 6
DAY_END_HOUR = 23
RAIN_PROB_TRESH = 0.5
ZAGREB_TIMEZONE = 'Europe/Zagreb'


def will_rain_today():
    rainToday = False
    rainStartHour = None

    forecastByHour = openWeather.get_forecast_by_hour()

    localTimeNow = datetime.now(pytz.timezone(ZAGREB_TIMEZONE))

    for forecast in forecastByHour:
        forecastTime = forecast['t']
        probability = forecast['p']
        sameDayForecast = localTimeNow.day == forecastTime.day
        inTimeRange = forecastTime.hour >= DAY_START_HOUR and forecastTime.hour <= DAY_END_HOUR
        highRainProbability = probability >= RAIN_PROB_TRESH

        if sameDayForecast and inTimeRange and highRainProbability:
            rainToday = True
            rainStartHour = forecastTime.hour
            break

    return rainToday, rainStartHour


if __name__ == "__main__":
    sender, password, openWeatherApiKey = utils.load_credentials()

    gmail = Gmail(sender, password)
    openWeather = OpenWeather(openWeatherApiKey)

    receivers = utils.load_emails()

    for receiver in receivers:
        rainToday, rainStart = will_rain_today()

        if rainToday:
            # TODO: Construct message so it contains probabilities
            # by hour
            subject = 'Rain today in Zagreb'
            msg = f'Rain today at {rainStart}.'

            gmail.send(receiver, subject, msg)

        else:
            print('INFO: No rain today in Zagreb.')
