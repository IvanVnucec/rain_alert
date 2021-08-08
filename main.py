from utils import error, get_email_credentials, get_receivers, debug
from gmail import Gmail
from forecast import Forecast
from location import Location
from exec_tracker import ExecTracker

SEND_EMAIL_HOUR = 5  # AM local time


def send_forecast_message(gmail, receiver, message):
    subject, msgPlain, msgHtml = message
    gmail.send(receiver, subject, msgPlain, msgHtml)


def main():
    sender, password = get_email_credentials()
    receivers = get_receivers()
    if len(receivers) == 0: error('No receivers imported.')

    gmail = Gmail(sender, password)
    
    # use password from email to encrypt exec tracker file
    track = ExecTracker(password)

    for locationName, emails in receivers.items():
        location = Location(locationName)

        executed_today = track.script_executed_today(location)
        time_to_send_email = location.get_local_time().hour >= SEND_EMAIL_HOUR

        if not executed_today and time_to_send_email:
            """ mark execution time only when time to send en email because 
            we don't want to exceed the number of free OpenWeather API calls """ 
            debug("Script not executed today and its time to send en email.")
            debug('Mark executed time.')
            track.mark_exec_time(location)

            forecast = Forecast(location)

            if forecast.rain_today():
                debug('It will rain today.')
                message = forecast.get_forecast_message()

                for email in emails:
                    debug('Sending email message.')
                    send_forecast_message(gmail, email, message)
            else:
                debug('It will not rain today.')

        else:
            debug('Script already executed today and/or its not time to send an email.')

    debug('Closing execution timetable.')
    track.close()
    debug("Application finished.")


if __name__ == "__main__":
    main()
