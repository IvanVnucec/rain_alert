import os
from datetime import datetime


def get_hourly_forecast_for_zagreb():
    import urllib.request
    import json
    ZAGREB_WEATHER_API = "https://api.open-meteo.com/v1/forecast?latitude=45.8144&longitude=15.978&hourly=precipitation_probability&timezone=Europe%2FBerlin&forecast_days=1"
    with urllib.request.urlopen(ZAGREB_WEATHER_API) as response:
        assert response.status == 200
        data = json.loads(response.read())
    assert(data["hourly_units"]["time"] == "iso8601")
    assert(data["hourly_units"]["precipitation_probability"] == "%")
    data_hourly = data["hourly"]
    forecast = [(datetime.fromisoformat(time), float(prob)/100) for time, prob in zip(data_hourly["time"], data_hourly["precipitation_probability"])]
    return forecast

def generate_email_contents(forecast):
    # get first high probability of rain
    time_now = datetime.now().hour
    hour_start = next(time for time,prob in forecast if time.hour >= time_now and prob >= 0.5)
    # Construct message subject and HTML content
    subject = f"Zagreb: padaline od {hour_start.strftime('%H:%M')}h"
    content = """<!DOCTYPE html>
<html>
    <head>
        <style type="text/css">
            table {
                font-family: arial, sans-serif;
                border-collapse: collapse;
                width: 40%;
            }
            table td,
            th {
                border: 1px solid #afafaf;
                text-align: center;
                padding: 8px;
            }"""
    for id,time_prob in enumerate(forecast):
        alpha = round(time_prob[1] * 0.6, 2)
        bColor = f'hsla(240, 100%, 50%, {alpha})'
        content += f"""
            table td#CELL{id} {{
                background-color: {bColor};
                color: black;
            }}"""

    content += f"""
        </style>
    </head>
    <body>
        <h2>Zagreb forecast</h2>
        <table>
            <tr>
                <th>Hour [h]</th>
                <th>Probability [%]</th>
            </tr>"""
    for id,time_prob in enumerate(forecast):
        hour = str(time_prob[0].hour)
        prob = str(time_prob[1])
        content += f"""
            <tr>
                <td>{hour}</td>
                <td id="CELL{id}">{prob}</td>
            </tr>
        """

    content += """</table>"""
    action_url = os.getenv('ACTION_URL') or "Unknown"
    content += f"""
        <p><a href="{action_url}">GitHub Action Run</a></p>
    </body>
</html>
"""
    return subject, content

def send_emails(receivers, forecast):
    import smtplib
    import ssl
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    SSL_PORT = 465
    SMTP_GMAIL = 'smtp.gmail.com'
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL(SMTP_GMAIL, SSL_PORT, context=context)
    sender_email, password = os.getenv('SENDER_EMAIL'), os.getenv('SENDER_PASSWORD')
    server.login(sender_email, password)

    subject, content = generate_email_contents(forecast)
    for receiver in receivers:
        message = MIMEMultipart("alternative")
        message['From'] = sender_email
        message['To'] = receiver
        message['Subject'] = subject
        message.attach(MIMEText(content, "html"))
        server.send_message(message, sender_email, receiver)

def main():
    forecast = get_hourly_forecast_for_zagreb()
    time_now = datetime.now().hour
    rain_today = any(prob >= 0.5 for time, prob in forecast if time.hour >= time_now)
    receivers = os.getenv('RECEIVERS')
    if rain_today:
        print("🌧️🌧️🌧️")
        if receivers:
            receivers = receivers.split('\n')
            send_emails(receivers, forecast)
    else:
        print("🌞🌞🌞")
    with open('cnt.txt', 'r') as f:
        cnt = int(f.readline())
    with open('cnt.txt', 'w') as f:
        f.write(str(cnt+1))

if __name__ == '__main__':
    main()
