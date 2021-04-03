import utils
from gmail import Gmail
from open_weather import OpenWeather

sender, password, openWeatherApiKey = utils.load_credentials()

gmail = Gmail(sender, password)
openWeather = OpenWeather(openWeatherApiKey)

receivers = utils.load_emails()

if openWeather.will_rain_today() == False:
    subject = 'Rain today'
    msg = f'Rain today at {openWeather.rainStartHour}.'

    gmail.send(receivers, subject, msg)

else:
    print('INFO: No rain today.')
