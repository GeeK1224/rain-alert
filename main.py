import requests
from twilio.rest import Client
from dotenv import load_dotenv
import os

env_path = os.getcwd() + "/.env"
load_dotenv(env_path)

endpoint = "https://api.openweathermap.org/data/2.5/onecall"
api_key = os.getenv('API_KEY')

twilio_sid = os.getenv('TWILIO_SID')
twilio_token = os.getenv('TWILIO_TOKEN')

parameters = {"lat": os.getenv('LAT'),
              "lon": os.getenv('LON'),
              "exclude": "currently,minutely,daily",
              "appid": api_key,
              }


response = requests.get(endpoint, params=parameters)
response.raise_for_status()
weather_data = response.json()
hours = weather_data["hourly"]

place = weather_data["timezone"]

will_rain = False

for i in range(0, 12):
    elem = hours[i]
    elem_weather = elem["weather"][0]
    print(elem_weather["id"])
    if elem_weather["id"] < 700:
        will_rain = True

if will_rain:
    client = Client(twilio_sid, twilio_token)
    message = client.messages.create(
        body=f"It will be rain in {place[5:]} today. Don't forget to take an UMBRELLA",
        from_=os.getenv('TWILIO_NUMBER'),
        to=os.getenv('YOUR_NUMBER')
    )
    print(message.status)