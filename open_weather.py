import requests
import json
from geopy.geocoders import Nominatim
from datetime import datetime


class OpenWeather:
    __DAY_START_HOUR = 6
    __DAY_END_HOUR = 23
    __RAIN_PROB_TRESH = 0.5
    __GEOLOC_APP_NAME = 'Locator-request-app'

    def __init__(self, apiKey) -> None:
        self.__apiKey = apiKey

    def _get_data_from_api(self, apiUrl):
        try:
            response = requests.get(apiUrl)
        except:
            exit('ERROR: OpenWeather API request failed.')

        return response.json()

    def _get_forecast_by_hour(self, location):
        forecastByHour = []

        # get location based on location name (ex. 'New York')
        geolocator = Nominatim(user_agent=self.__GEOLOC_APP_NAME)
        geoLocation = geolocator.geocode(location)

        apiUrl = 'http://api.openweathermap.org/data/2.5/onecall?'\
            f'&lat={geoLocation.latitude}'\
            f'&lon={geoLocation.longitude}'\
            '&exclude=current,minutely,daily,alerts&units=metric'\
            f'&appid={self.__apiKey}'

        data = self._get_data_from_api(apiUrl)

        timezoneOffset = data['timezone_offset']
        byHours = data['hourly']

        for hour in byHours:
            unixTime = hour['dt'] + timezoneOffset
            time = datetime.utcfromtimestamp(unixTime)

            rainProbability = hour['pop']

            rainData = {'t': time, 'p': rainProbability}
            forecastByHour.append(rainData)

        return forecastByHour

    def will_rain_today(self, location):
        rainToday = False
        rainStartHour = None

        forecastByHour = self._get_forecast_by_hour(location)

        timeNow = datetime.now()

        for hour in forecastByHour:
            sameDayForecast = timeNow.day == hour['t'].day
            inDayTimeRange = hour['t'].hour >= self.__DAY_START_HOUR and hour['t'].hour <= self.__DAY_END_HOUR
            highRainProbability = hour['p'] >= self.__RAIN_PROB_TRESH

            if sameDayForecast and inDayTimeRange and highRainProbability:
                rainToday = True
                rainStartHour = hour['t'].hour
                break

        return rainToday, rainStartHour
