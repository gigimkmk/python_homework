
import requests


def get_weather(city):
   
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city,
        "count": 1
    }

    response = requests.get(geo_url, params=params)

    if response.status_code != 200:
        print("Error while connecting to Geocoding API")
        return

    data = response.json()

    if "results" not in data:
        print("City not found")
        return

    city_info = data["results"][0]

    latitude = city_info["latitude"]
    longitude = city_info["longitude"]
    city_name = city_info["name"]

    
    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m",
        "timezone": "auto"
    }

    weather_response = requests.get(weather_url, params=weather_params)

    if weather_response.status_code != 200:
        print("Error while connecting to Weather API")
        return

    weather_data = weather_response.json()

    current = weather_data["current"]

    print(f"City: {city_name}")
    print(f"Temperature: {current['temperature_2m']} °C")
    print(f"Wind Speed: {current['wind_speed_10m']} km/h")
    print(f"Time: {current['time']}")


city = input("Enter city name: ")
get_weather(city)