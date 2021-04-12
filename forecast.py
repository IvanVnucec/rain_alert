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

    def __construct_plain_message(self, locationName):
        plain = f'{locationName} forecast\n\n'
        for forecast in self.forecastToday:
            hourStr = str(forecast['h'])
            probStr = str(round(forecast['p'] * 100))
            plain += f'{hourStr : <2}h {probStr : >3}%\n'

        return plain

    def __construct_html_message(self, locationName):
        html = """
        <!DOCTYPE html>
        <html>
        <head>
        <style type="text/css">
        table {
            font-family: arial, sans-serif; 
            border-collapse: collapse; 
            width: 40%;
        }

        table td, th {
            border: 1px solid #afafaf; 
            text-align: center; padding: 8px;
        }
        """

        # set cell colors based on precipitation probability
        for id, forecast in enumerate(self.forecastToday):
            alpha = round(forecast['p'] * 0.6, 2)
            bColor = f'hsla(240, 100%, 50%, {alpha})'
            html += f'table td#CELL{id} {{background-color:' + \
                bColor + '; color:black;}'

        html += """
        </style>
        </head>
        <body>
        """

        html += f"""
        <h2>{locationName} forecast</h2>
        <table>
        <tr>
            <th>Hour [h]</th>
            <th>Probability [%]</th>
        </tr>"""

        # populate cells
        for id, forecast in enumerate(self.forecastToday):
            hourStr = str(forecast['h'])
            probStr = str(round(forecast['p'] * 100))
            html += f"""
                <tr>
                    <td>{hourStr}</td>
                    <td id="CELL{id}">{probStr}</td>
                </tr>
            """

        html += """
        </table>
        </body>
        </html>"""

        return html

    def construct_forecast_message(self):
        rainStartHour = self.get_rain_start_hour()
        locationName = self.location.get_location_name()

        subject = f'Rain in {locationName} from {rainStartHour}h'

        plain = self.__construct_plain_message(locationName)
        html = self.__construct_html_message(locationName)

        return (subject, plain, html)

    def rain_today(self):
        return True in [forecast['b'] for forecast in self.forecastToday]
