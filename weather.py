import requests
from utils.api_keys import WEATHER_API_KEY

def get_weather(city, units="imperial"):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units={units}&appid={WEATHER_API_KEY}"
    r = requests.get(url).json()
    return {
        "temp": int(r["main"]["temp"]),
        "description": r["weather"][0]["description"].capitalize(),
        "icon": r["weather"][0]["icon"]
    }
