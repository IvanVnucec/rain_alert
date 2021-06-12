from geopy.format import HTML_DOUBLE_PRIME
from utils import get_email_credentials, get_receivers
from gmail import Gmail
from forecast import Forecast
from location import Location
from exec_tracker import ExecTracker

SEND_EMAIL_HOUR = 5  # AM local time
TIMETABLE_PATH = 'EXEC_TIMETABLE.json'


def send_forecast_message(gmail, receiver, message):
    subject, msgPlain, msgHtml = message
    gmail.send(receiver, subject, msgPlain, msgHtml)


def main():
    track = ExecTracker()

    sender, password = get_email_credentials()
    receivers = get_receivers()

    gmail = Gmail(sender, password)

    timetable = track.timetable_open(TIMETABLE_PATH)
    exec_times = track.load_exec_times(timetable)

    for locationName, emails in receivers.items():
        location = Location(locationName)

        executed_today = track.script_executed_today(exec_times, location)
        time_to_send_email = location.get_local_time().hour >= SEND_EMAIL_HOUR

        if not executed_today and time_to_send_email:
            track.append_exec_time(exec_times, location)

            forecast = Forecast(location)

            if forecast.rain_today():
                message = forecast.get_forecast_message()

                for email in emails:
                    send_forecast_message(gmail, email, message)

    track.timetable_store(timetable, exec_times)
    track.timetable_close(timetable)
    print('INFO: Done.')


if __name__ == "__main__":
    main()
