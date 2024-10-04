# rain_alert

[![App running](https://github.com/IvanVnucec/rain_alert/actions/workflows/weather_check.yml/badge.svg?branch=master&event=schedule)](https://github.com/IvanVnucec/rain_alert/actions/workflows/weather_check.yml)

You will not forget your :umbrella: anymore.

## About

Check the weather at 5AM Zagreb time and send an email if it will rain today.

## Get started

1. Create Gmail account and enable the Less secure app access.
2. Add the following environment variables to GitHub actions:
    - `SENDER_EMAIL` - sender Gmail email
    - `SENDER_PASSWORD` - Gmail email password
    - `RECEIVERS` - list of email addresses to send the alert to
3. Run the GitHub Action workflow manually to check if everything is working.

## License

[MIT](LICENSE.md)
