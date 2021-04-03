# rain_alert
Send an email if it will be raining today. :umbrella:

## Get started
1. Create `CREDENTIALS.yaml` and put credentials as:
```
senderEmail: <sender Gmail email>
senderPassword: <Gmail email password>
openWeatherApiKey: <OpenWeather API key>
```
2. Create `RECEIVERS.txt` and put email subscribers as:
```
<email address>, <location name>
example@gmail.com, New York
example2@yahoo.com, London
example3@yahoo.com, Zagreb
```
3. Activate virtualenv.
4. Install dependencies from `requirements.txt`.
5. Run app as `python3 main.py`

## License
[WTFPL – Do What the Fuck You Want to Public License](LICENSE.md)