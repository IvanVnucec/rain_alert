from gmail import Gmail
from open_weather import OpenWeather
from load_credentials import loadCredentials

emailToSend, password, openWeatherApiKey, emailToReceive = loadCredentials()

gmail = Gmail(emailToSend, password)
openWeather = OpenWeather(openWeatherApiKey)

if openWeather.will_rain_today():
    msg = f'Rain today at {openWeather.rainStartHour}.'
    gmail.send(msg, emailToReceive)
