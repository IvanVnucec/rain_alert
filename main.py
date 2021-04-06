from utils import get_email_credentials, get_emails_and_locations
from gmail import Gmail
from forecast import Forecast
from location import Location

SEND_EMAIL_HOUR = 5  # AM local time

if __name__ == "__main__":
    sender, password = get_email_credentials()
    receivers = get_emails_and_locations()

    numOfReceivers = len(receivers)
    print(f'INFO: found {numOfReceivers} receive emails.')

    gmail = Gmail(sender, password)

    for num, receiver in enumerate(receivers, start=1):
        print(f'INFO: {num}/{numOfReceivers}', end =' ')
        location = Location(receiver['location'])

        if location.get_local_time().hour == SEND_EMAIL_HOUR:
            forecast = Forecast(location)

            if forecast.rain_today():
                subject, content, contentHtml = forecast.construct_forecast_message()
                print('Sending email.')
                gmail.send(receiver['email'], subject, content, contentHtml)
            else:
                print('No rain today.')
        else:
            print("It's not time.")
    
    print('INFO: Done.')
