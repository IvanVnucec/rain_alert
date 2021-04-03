import requests
import json
from datetime import datetime


class OpenWeather:
    __DAY_START_HOUR = 6
    __DAY_END_HOUR = 11
    __RAIN_PROB_TRESH = 0.5
    __ZAGREB_LAT = '45.8154'
    __ZAGREB_LON = '15.9666'

    def __init__(self, apiKey) -> None:
        self.rainStartHour = None
        self.__apiUrl = 'http://api.openweathermap.org/data/2.5/onecall?'\
            f'&lat={self.__ZAGREB_LAT}'\
            f'&lon={self.__ZAGREB_LON}'\
            '&exclude=current,minutely,daily,alerts&units=metric'\
            f'&appid={apiKey}'

    def _get_data_from_api(self):
        try:
            response = requests.get(self.__apiUrl)
        except:
            exit('ERROR: OpenWeather API request failed.')

        return response.json()

    def _get_forecast_by_hour(self):
        forecastByHour = []

        data = self._get_data_from_api()

        timezoneOffset = data['timezone_offset']
        byHours = data['hourly']

        for hour in byHours:
            unixTime = hour['dt'] + timezoneOffset
            time = datetime.utcfromtimestamp(unixTime)

            rainProbability = hour['pop']

            rainData = {'t': time, 'p': rainProbability}
            forecastByHour.append(rainData)

        return forecastByHour

    def will_rain_today(self):
        forecastByHour = self._get_forecast_by_hour()

        # get time now
        timeNow = datetime.now()

        for hour in forecastByHour:
            sameDayForecast = timeNow.day == hour['t'].day
            inDayTimeRange = hour['t'].hour >= self.__DAY_START_HOUR and hour['t'].hour <= self.__DAY_END_HOUR
            highRainProbability = hour['p'] >= self.__RAIN_PROB_TRESH

            if sameDayForecast and inDayTimeRange and highRainProbability:
                self.rainStartHour = hour['t'].hour
                return True

        return False
