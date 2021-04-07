from utils import get_email_credentials, get_receivers
from gmail import Gmail
from forecast import Forecast
from location import Location

SEND_EMAIL_HOUR = 5  # AM local time


def send_forecast_message(receiver, message):
    subject = message[0]
    contentPlain = message[1]
    contentHtml = message[2]
    gmail.send(receiver, subject, contentPlain, contentHtml)


if __name__ == "__main__":
    sender, password = get_email_credentials()
    receivers = get_receivers()

    gmail = Gmail(sender, password)

    for locationName, emails in receivers.items():
        location = Location(locationName)

        if location.get_local_time().hour == SEND_EMAIL_HOUR:
            forecast = Forecast(location)
            
            if forecast.rain_today():
                message = forecast.construct_forecast_message()
                
                for email in emails:
                    send_forecast_message(email, message)

    print('INFO: Done.')
