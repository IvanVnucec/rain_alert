import requests
import json
from datetime import datetime
import pytz


class OpenWeather:
    __DAY_START_HOUR = 6
    __DAY_END_HOUR = 23
    __RAIN_PROB_TRESH = 0.5
    __ZAGREB_LAT = 45.815399
    __ZAGREB_LON = 15.966568
    __ZAGREB_TIMEZONE = 'Europe/Zagreb'

    def __init__(self, apiKey) -> None:
        self.__apiKey = apiKey

    def _get_data_from_api(self, apiUrl):
        try:
            response = requests.get(apiUrl)
        except:
            exit('ERROR: OpenWeather API request failed.')

        return response.json()

    def _get_forecast_by_hour(self, latitude, longitude):
        forecastByHour = []

        apiUrl = 'http://api.openweathermap.org/data/2.5/onecall?'\
            f'&lat={latitude}'\
            f'&lon={longitude}'\
            '&exclude=current,minutely,daily,alerts&units=metric'\
            f'&appid={self.__apiKey}'

        data = self._get_data_from_api(apiUrl)

        timezoneOffset = data['timezone_offset']
        byHours = data['hourly']

        for hour in byHours:
            unixTime = hour['dt'] + timezoneOffset
            localTime = datetime.utcfromtimestamp(unixTime)

            rainProbability = hour['pop']

            rainData = {'t': localTime, 'p': rainProbability}
            forecastByHour.append(rainData)

        return forecastByHour

    def will_rain_today(self):
        rainToday = False
        rainStartHour = None

        forecastByHour = self._get_forecast_by_hour(self.__ZAGREB_LAT, self.__ZAGREB_LON)
        
        timeNow = datetime.now(pytz.timezone(self.__ZAGREB_TIMEZONE))

        for hour in forecastByHour:
            sameDayForecast = timeNow.day == hour['t'].day
            inDayTimeRange = hour['t'].hour >= self.__DAY_START_HOUR and hour['t'].hour <= self.__DAY_END_HOUR
            highRainProbability = hour['p'] >= self.__RAIN_PROB_TRESH

            if sameDayForecast and inDayTimeRange and highRainProbability:
                rainToday = True
                rainStartHour = hour['t'].hour
                break

        return rainToday, rainStartHour
