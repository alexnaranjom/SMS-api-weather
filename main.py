import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure

#Connect phone
account_sid = "AC05f50a5e72f502ab0863806478917cd5"
auth_token = os.environ.get("AUTH_TOKEN")




OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
api_key = os.environ.get("OWS_API_KEY")


#https://api.openweathermap.org/data/2.5/weather?zip=20912,us&appid=5d26ff3e273d498e40ca139457ea48e1
weather_params ={
    "lon": -77.002708,
    "lat": 38.981171,


    "appid": api_key,
    "exclude": "current,minutely,daily"
}
response = requests.get(OWM_Endpoint,params= weather_params)
# status 200 ok print(response.status_code)
response.raise_for_status()
weather_data=response.json()
weather_slice = weather_data["hourly"][:12]

will_rain = False
for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if condition_code < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    #send message
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body="IT's raining, Bring an umbrella frpom task.",
        from_="+18458271241",
        to="+13012223327"
    )
    print(message.status)
#print(weather_slice)
#print(weather_data["hourly"][0]["weather"][0]["id"])