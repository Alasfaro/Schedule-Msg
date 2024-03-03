import schedule
import time

def get_weather(lat, long):
    base_url = f"https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    response = requests.get(base_url)
    data = response.json()
    return data

def weather_update():
    #Mississauga latitude longitude
    lat = 43.5890
    long = 79.6441
    weather_data = get_weather(lat, long)

    wind_speed = weather_data["hourly"]["wind_speed_10m"][0]
    temp = weather_data["hourly"]["temperature_2m"][0]
    humidity = weather_data["hourly"]["relative_humidity2m"][0]

    weather_info = (
        f"Weather in Mississauga:\n"
        f"Temperature: {temp}\n"
        f"Wind Speed: {wind_speed}\n"
        f"Humidity: {humidity}\n"
    )

def send(body):
    account_sid = "twilio_sid"
    auth_token = "twilio_token"
    from_phone = "from_phone_number"
    to_phone = "to_phone_number"

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body = body,
        from_ = from_phone
        to = to_phone
    )
    print("Text message sent")