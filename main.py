import os


def get_hourly_forecast_for_zagreb() -> list[tuple]:
    import urllib.request
    import json
    ZAGREB_WEATHER_API = "https://api.open-meteo.com/v1/forecast?latitude=45.8144&longitude=15.978&hourly=precipitation_probability&timezone=Europe%2FBerlin&forecast_days=1"
    with urllib.request.urlopen(ZAGREB_WEATHER_API) as response:
        assert response.status == 200
        data = json.loads(response.read())

    from datetime import datetime
    data_hourly = data["hourly"]
    forecast = [(datetime.fromisoformat(time), int(prob)) for time, prob in zip(data_hourly["time"], data_hourly["precipitation_probability"])]
    return forecast

def construct_html_table(forecast) -> tuple[str, str]:
    # get first high probability of rain
    hour_start = [time for time, prob in forecast if prob >= 0.5]
    # Construct message subject and HTML content
    subject = f"Zagreb: padaline od {hour_start[0].strftime('%H:%M')}h"
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
    for id,forecast in enumerate(forecast):
        alpha = round(forecast[1] * 0.6, 2)
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
    for id,forecast in enumerate(forecast):
        hourStr = str(forecast[0].hour)
        probStr = str(forecast[1])
        content += f"""
            <tr>
                <td>{hourStr}</td>
                <td id="CELL{id}">{probStr}</td>
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

    subject, content = construct_html_table(forecast)
    for receiver in receivers:
        message = MIMEMultipart("alternative")
        message['From'] = sender_email
        message['To'] = receiver
        message['Subject'] = subject
        message.attach(MIMEText(content, "html"))
        server.send_message(message, sender_email, receiver)

def main():
    forecast = get_hourly_forecast_for_zagreb()
    rain_today = any(prob >= 0.5 for _,prob in forecast)
    if rain_today:
        receivers = os.getenv('RECEIVERS').split('\n')
        send_emails(receivers, forecast)

if __name__ == '__main__':
    main()
