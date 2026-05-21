import requests
import os
from twilio.rest import Client
API_KEY = "a5684aed171b416a353884f53bcbaf02"

query_para = {
    "lat": 30.433283,
    "lon": -87.240372,
    "appid": API_KEY,
    "cnt" :4
}

response = requests.get(
    "https://api.openweathermap.org/data/2.5/forecast",
    params=query_para,
)

response.raise_for_status()

response_json = response.json()# parse response "body as JSON " and return Python data


time_3hours = response_json["list"]
weather_codes = [hour["weather"][0]["id"] for hour in time_3hours]

account_sid =os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)



for weather_code in weather_codes :
    if int(weather_code) <900:
        message = client.messages.create(
        from_='whatsapp:+14155238886',
        body="It's going to rain today. Remember to bring an umbrella!!!",
        to='whatsapp:+18572057736'
    )

        print(message.sid)
