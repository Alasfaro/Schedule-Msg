from datetime import datetime
import os.path
import pytz
import requests
from twilio.rest import Client
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def get_weather(lat, long):
    base_url = f"https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    response = requests.get(base_url)
    data = response.json()
    return data

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def get_calendar_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())  

    # creds = service_account.Credentials.from_service_account_file (
    #     cred,
    #     SCOPES
    # )

    service = build('calendar', 'v3', credentials=creds)
    return service

def send(body):
    account_sid = 'twilio sid'
    auth_token = 'twilio auth token'
    from_phone = 'twilio phone number'
    to_phone = 'personal phone number'

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body = body,
        from_ = from_phone,
        to = to_phone
    )
    print(message.sid)

def calendar_msg():
    try:
        cal = get_calendar_service()
        est = pytz.timezone('America/Toronto')
        now = datetime.now().astimezone(est)
        end = datetime(now.year, now.month, now.day, 23, 0, 0).astimezone(est)

        res = cal.events().list(
            calendarId = 'primary',
            timeMin = now.isoformat(),
            timeMax = end.isoformat(),
            singleEvents = True,
            orderBy = 'startTime'
        ).execute()

        events = res.get('items', [])
        
        if not events:
            message = "No tasks for today\n"
        else:
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                summary = event['summary']
                message = f"{start}: {summary}\n"
                send(message)

    except HttpError as error:
        print(f"An error occurred: {error}")


def weather_msg():
    #Mississauga latitude longitude
    lat = 43.5890
    long = 79.6441
    weather_data = get_weather(lat, long)

    wind_speed = weather_data["hourly"]["wind_speed_10m"][0]
    temp = weather_data["hourly"]["temperature_2m"][0]
    humidity = weather_data["hourly"]["relative_humidity_2m"][0]

    weather_info = (
        f"Weather in Mississauga\n"
        f"Temperature: {temp}\n"
        f"Wind Speed: {wind_speed}\n"
        f"Humidity: {humidity}\n"
    )

    send(weather_info)


def main():
    weather_msg()
    calendar_msg()

if __name__ == "__main__":
    main()