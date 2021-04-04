# rain_alert
Every morning at 5 AM Zagreb local time check if it will be raining on that day, if yes then remind me by sending me an email.

## Get started
0. Create Gmail account and enable the Less secure app access. 
1. Create `CREDENTIALS.yaml` and put credentials:
```
senderEmail: <sender Gmail email>
senderPassword: <Gmail email password>
openWeatherApiKey: <OpenWeather API key>
```
2. Create `RECEIVERS.txt` and put email subscribers as:
```
<email address>
example@gmail.com
example2@yahoo.com
example3@hotmail.com
```
3. Activate virtualenv.
4. Install dependencies from `requirements.txt`.
5. Run app as `python3 main.py`

## License
[WTFPL – Do What the Fuck You Want to Public License](LICENSE.md)
