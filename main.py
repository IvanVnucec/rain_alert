import utils
from gmail import Gmail
from open_weather import OpenWeather
from timezones import Location

SEND_EMAIL_HOUR = 5

sender, password, openWeatherApiKey = utils.load_credentials()

gmail = Gmail(sender, password)
openWeather = OpenWeather(openWeatherApiKey)

receivers = utils.load_emails_and_locations()

for receiver in receivers:
    email = receiver['email']
    locName = receiver['location']

    location = Location(locName)

    # if local time to send an email
    if location.localTime.hour == SEND_EMAIL_HOUR:
        rainToday, rainStart = openWeather.will_rain_today(location)

        if rainToday:
            subject = f'Rain today in {location.name}'
            msg = f'Rain today at {rainStart}.'

            gmail.send(email, subject, msg)
