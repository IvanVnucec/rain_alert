# rain_alert
You will not forget your umbrella anymore.

## About
Every morning at 5 AM local time check if it will be raining that day, if yes 
send an email with forecast message like this:
```
Subject: Rain in Zagreb from 21h
Message:
6 h 0%
7 h 0%
8 h 0%
9 h 0%
10h 0%
11h 0%
12h 0%
13h 0%
14h 1%
15h 4%
16h 4%
17h 12%
18h 12%
19h 21%
20h 39%
21h 97%
22h 100%
23h 100%
```

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
<email>, <location name>
example1@gmail.com, Zagreb
example2@gmail.com, Berlin
example3@gmail.com, Milwaukee
example4@gmail.com, Mobile Alabama
example5@gmail.com, Nashville Tennessee
example6@gmail.com, Nashville Indiana
```
3. Activate virtualenv.
4. Install dependencies from `requirements.txt`.
5. Run app as `python3 main.py'.
6. You can schedule the script to run for every hour in CI workflow (see my [GitHub Actions setup](https://github.com/IvanVnucec/rain_alert/actions)).

## License
[WTFPL – Do What the Fuck You Want to Public License](LICENSE.md)
