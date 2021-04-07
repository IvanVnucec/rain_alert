from open_weather import OpenWeather

DAY_START_HOUR = 6
DAY_END_HOUR = 23
RAIN_PROB_TRESHOLD = 0.5


class Forecast:
    def __init__(self, location):
        self.location = location
        self.forecastToday = self.get_forecast_today()

    def get_forecast_today(self):
        forecastToday = []

        lat, lon = self.location.get_latitude_longitude()

        ow = OpenWeather()
        forecasts = ow.get_forecast(lat, lon)
        localDate = self.location.get_local_time().date()

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

        return forecastToday

    def get_rain_start_hour(self):
        hour = None

        for forecast in self.forecastToday:
            if forecast['b']:
                hour = forecast['h']
                break

        return hour

    def construct_forecast_message(self):
        rainStartHour = self.get_rain_start_hour()
        locationName = self.location.get_location_name()

        subject = f'Rain in {locationName} from {rainStartHour}h'

        html = '<html><body>'
        plain = ''
        for forecast in self.forecastToday:
            hourStr = str(forecast['h'])
            probStr = str(round(forecast['p'] * 100))

            plain += f'{hourStr : <2}h {probStr : >3}%\n'

            alpha = forecast['p'] * 0.6
            alpha = round(alpha, 2)
            bColor = f'hsla(240, 100%, 50%, {alpha})'

            if len(hourStr) == 1:
                hourStr += ' '

            html += f'<span>{hourStr}h </span>'
            html += f'<span style="color: rgb(0, 0, 0); background-color: {bColor};">{probStr}%</span><br>'

        html += '</body></html>'

        return (subject, plain, html)

    def rain_today(self):
        return True in [forecast['b'] for forecast in self.forecastToday]
