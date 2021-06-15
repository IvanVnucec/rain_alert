# rain_alert
You will not forget your umbrella anymore. :umbrella:

## About
Check every morning at 5 AM local time if it will be raining that day, if yes 
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
Create OpenWeather API Key.
1. Create `CREDENTIALS.yaml` file and put credentials:
```
senderEmail: <sender Gmail email>
senderPassword: <Gmail email password>
openWeatherApiKey: <OpenWeather API key>
```
2. Create `RECEIVERS.txt` file and put email subscribers as:
```
<email>, <location name>
example1@gmail.com, Zagreb
example2@gmail.com, Berlin
example3@gmail.com, Milwaukee
example4@gmail.com, Mobile Alabama
example5@gmail.com, Nashville Tennessee
example6@gmail.com, Nashville Indiana
```
3. Activate virtualenv by running `virtualenv venv` and then `source ./bin/activate`.
4. Install pip dependencies from `requirements.txt` file by running `pip install -r requirements.txt`.
5. Run app as `python3 main.py`.
6. You can schedule the script to run once every 
hour like we did in CI workflow. See [GitHub Actions setup](https://github.com/IvanVnucec/rain_alert/blob/master/.github/workflows/main.yml).

## License
[MIT](LICENSE.md)
