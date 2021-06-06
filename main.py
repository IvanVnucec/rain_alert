from utils import get_email_credentials, get_receivers
from gmail import Gmail
from forecast import Forecast
from location import Location
from exec_tracker import ExecTracker

SEND_EMAIL_HOUR = 5  # AM local time


def send_forecast_message(gmail, receiver, message):
    subject, msgPlain, msgHtml = message
    gmail.send(receiver, subject, msgPlain, msgHtml)


def main():
    tracker = ExecTracker()

    sender, password = get_email_credentials()
    receivers = get_receivers()

    gmail = Gmail(sender, password)

    for locationName, emails in receivers.items():
        location = Location(locationName)

        # get local time
        local_time = location.get_local_time()

        time_to_run = local_time.hour >= SEND_EMAIL_HOUR
        already_executed = tracker.script_executed_today(local_time)

        if time_to_run and not already_executed:
            forecast = Forecast(location)

            if forecast.rain_today():
                message = forecast.get_forecast_message()

                for email in emails:
                    send_forecast_message(gmail, email, message)

    tracker.store_execution_time()
    print('INFO: Done.')


if __name__ == "__main__":
    main()
