import utils
from gmail import Gmail
from open_weather import OpenWeather

sender, password, openWeatherApiKey = utils.load_credentials()

gmail = Gmail(sender, password)
openWeather = OpenWeather(openWeatherApiKey)

receivers = utils.load_emails_and_locations()

for receiver in receivers:
    email = receiver['email']
    location = receiver['location']

    rainToday, rainStart = openWeather.will_rain_today(location)
    if rainToday:
        subject = f'Rain today in {location}'
        msg = f'Rain today at {rainStart}.'

        gmail.send(email, subject, msg)
