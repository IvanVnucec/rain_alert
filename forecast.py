from datetime import datetime
import pytz
from open_weather import OpenWeather

DAY_START_HOUR = 6
DAY_END_HOUR = 23
RAIN_PROB_TRESHOLD = 0.5
ZAGREB_TIMEZONE = 'Europe/Zagreb'


class Forecast(OpenWeather):
    def __init__(self, apiKey):
        super().__init__(apiKey)
        self.rainToday = False
        self.rainStartHour = None
        self.forecastToday = self.get_forecast_today()

    def get_forecast_today(self):
        forecastToday = []

        forecasts = self.get_forecast()
        localDate = datetime.now(pytz.timezone(ZAGREB_TIMEZONE)).date()

        for forecast in forecasts:
            forecastDate = forecast['t'].date()
            forecastHour = forecast['t'].hour
            probability = forecast['p']

            sameDayForecast = localDate == forecastDate
            inTimeRange = forecastHour >= DAY_START_HOUR and forecastHour <= DAY_END_HOUR
            highRainProbability = probability >= RAIN_PROB_TRESHOLD

            if sameDayForecast and inTimeRange:
                forecastToday.append(
                    {'b': highRainProbability, 'p': probability, 'h': forecastHour})

                if highRainProbability:
                    self.rainToday = True
                    # set rain start hour
                    if self.rainStartHour == None:
                        self.rainStartHour = forecastHour

        return forecastToday

    def construct_forecast_message(self):
        subject = f'Rain in Zagreb from {self.rainStartHour}h'

        content = ''
        for forecast in self.forecastToday:
            hour = str(forecast['h'])
            probability = str(round(forecast['p'] * 100))

            content += f'{hour : <2}h {probability : >3}%\n'

        return subject, content

    def rain_today(self):
        return self.rainToday
