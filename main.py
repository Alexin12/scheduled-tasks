
import os
from datetime import datetime, timedelta, timezone

import requests
from twilio.rest import Client

OWM_API_KEY = os.getenv("OWM_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

query_para = {
    "lat": 30.433283,
    "lon": -87.240372,
    "appid": OWM_API_KEY,
    "cnt": 4,
}

response = requests.get(
    "https://api.openweathermap.org/data/2.5/forecast",
    params=query_para,
)
response.raise_for_status()

response_json = response.json()
forecast_blocks = response_json["list"]

timezone_offset = response_json["city"]["timezone"]
local_timezone = timezone(timedelta(seconds=timezone_offset))


def format_time(dt):
    return dt.strftime("%I:%M %p").lstrip("0")


rain_time_ranges = []

for block in forecast_blocks:
    weather_code = block["weather"][0]["id"]

    # OpenWeather codes:
    # 2xx thunderstorm, 3xx drizzle, 5xx rain, 6xx snow
    if weather_code < 700:
        start_time = datetime.fromtimestamp(block["dt"], tz=timezone.utc).astimezone(local_timezone)
        end_time = start_time + timedelta(hours=3)

        rain_time_ranges.append(
            f"{format_time(start_time)} - {format_time(end_time)}"
        )

if rain_time_ranges:
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message_body = (
        "Rain is expected during these time ranges today: "
        + ", ".join(rain_time_ranges)
        + ". Remember to bring an umbrella!"
    )

    message = client.messages.create(
        from_="whatsapp:+14155238886",
        body=message_body,
        to="whatsapp:+18572057736",
    )

    print(message.sid)
else:
    print("No rain expected in the next forecast periods.")
