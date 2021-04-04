import requests
import json
from datetime import datetime
import pytz


__ZAGREB_LAT = 45.815399
__ZAGREB_LON = 15.966568


class OpenWeather:
    def __init__(self, apiKey) -> None:
        self.__apiKey = apiKey

    def _get_data_from_api(self):
        API_URL = 'http://api.openweathermap.org/data/2.5/onecall?'\
            f'&lat={__ZAGREB_LAT}'\
            f'&lon={__ZAGREB_LON}'\
            '&exclude=current,minutely,daily,alerts&units=metric'\
            f'&appid={self.__apiKey}'

        try:
            response = requests.get(API_URL)
        except:
            exit('ERROR: OpenWeather API request failed.')

        return response.json()

    def get_forecast_by_hour(self):
        forecastByHour = []

        data = self._get_data_from_api()

        timezoneOffset = data['timezone_offset']
        byHours = data['hourly']

        for hour in byHours:
            unixTime = hour['dt'] + timezoneOffset
            localTime = datetime.utcfromtimestamp(unixTime)

            rainProbability = hour['pop']

            rainData = {'t': localTime, 'p': rainProbability}
            forecastByHour.append(rainData)

        return forecastByHour
