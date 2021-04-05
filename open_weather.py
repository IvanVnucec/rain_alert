import requests
import json
from datetime import datetime
import pytz


class OpenWeather:
    def __init__(self, apiKey) -> None:
        self.__apiKey = apiKey

    def _get_data_from_api(self, latitude, longitude):

        API_URL = 'http://api.openweathermap.org/data/2.5/onecall?'\
            f'&lat={latitude}'\
            f'&lon={longitude}'\
            '&exclude=current,minutely,daily,alerts&units=metric'\
            f'&appid={self.__apiKey}'

        try:
            response = requests.get(API_URL)
        except:
            exit('ERROR: OpenWeather API request failed.')

        return response.json()

    def get_forecast(self, latitude, longitude):
        forecastByHour = []

        data = self._get_data_from_api(latitude, longitude)

        timezoneOffset = data['timezone_offset']
        byHours = data['hourly']

        for hour in byHours:
            unixTime = hour['dt'] + timezoneOffset
            localTime = datetime.utcfromtimestamp(unixTime)

            rainProbability = hour['pop']

            rainData = {'t': localTime, 'p': rainProbability}
            forecastByHour.append(rainData)

        return forecastByHour
