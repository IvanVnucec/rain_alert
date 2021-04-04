import requests
import json
from datetime import datetime
import pytz


__DAY_START_HOUR = 6
__DAY_END_HOUR = 23
__RAIN_PROB_TRESH = 0.5
__ZAGREB_LAT = 45.815399
__ZAGREB_LON = 15.966568
__ZAGREB_TIMEZONE = 'Europe/Zagreb'


class OpenWeather:
    def __init__(self, apiKey) -> None:
        self.__apiKey = apiKey

    def _get_data_from_api(self, apiUrl):
        try:
            response = requests.get(apiUrl)
        except:
            exit('ERROR: OpenWeather API request failed.')

        return response.json()

    def _get_forecast_by_hour(self):
        forecastByHour = []

        apiUrl = 'http://api.openweathermap.org/data/2.5/onecall?'\
            f'&lat={__ZAGREB_LAT}'\
            f'&lon={__ZAGREB_LON}'\
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

        forecastByHour = self._get_forecast_by_hour()
        
        timeNow = datetime.now(pytz.timezone(__ZAGREB_TIMEZONE))

        for forecast in forecastByHour:
            time = forecast['t']
            probability = forecast ['p']
            sameDayForecast = timeNow.day == time.day
            inTimeRange = time.hour >= __DAY_START_HOUR and time.hour <= __DAY_END_HOUR
            highRainProbability = probability >= __RAIN_PROB_TRESH

            if sameDayForecast and inTimeRange and highRainProbability:
                rainToday = True
                rainStartHour = hour['t'].hour
                break

        return rainToday, rainStartHour
