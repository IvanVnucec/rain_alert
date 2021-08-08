import requests
from datetime import datetime
from utils import get_openWeather_api_key, error


class OpenWeather:
    # we want to get API key only once
    __API_KEY = get_openWeather_api_key()

    def __init__(self):
        pass

    def _get_data_from_api(self, latitude, longitude):

        API_URL = 'http://api.openweathermap.org/data/2.5/onecall?'\
            f'&lat={latitude}'\
            f'&lon={longitude}'\
            '&exclude=current,minutely,daily,alerts&units=metric'\
            f'&appid={self.__API_KEY}'

        try:
            response = requests.get(API_URL)
        except:
            error('OpenWeather API request failed.')

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
