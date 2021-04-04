import utils
from gmail import Gmail
from open_weather import OpenWeather

sender, password, openWeatherApiKey = utils.load_credentials()

gmail = Gmail(sender, password)
openWeather = OpenWeather(openWeatherApiKey)

receivers = utils.load_emails()

for receiver in receivers:
    # TODO: implement will_rain_today function here.
    # openWeather object should only get data.
    rainToday, rainStart = openWeather.will_rain_today()

    if rainToday:
        subject = 'Rain today in Zagreb'
        msg = f'Rain today at {rainStart}.'

        gmail.send(receiver, subject, msg)

    else:
        print('INFO: No rain today in Zagreb.')
