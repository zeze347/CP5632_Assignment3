import requests

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
TIMEOUT_SECONDS = 10


def main():
    while True:
        city_name = input("Enter a city name: ").strip()
        location = geocode_city(city_name)
        if location is None:
            print("City not found. Please try again.\n")
            continue
        latitude, longitude = location
        break

    temperature, time = get_weather(latitude, longitude)

    print(f"Time：{time}")
    print(f"Current temperature：{temperature} °C")


def geocode_city(city_name):
    try:
        geocode_params = {"name": city_name, "count": 1, "language": "en"}
        location_result = requests.get(GEOCODE_URL, params=geocode_params)
        geocode_data = location_result.json()
        location_results = geocode_data.get("results", [])
        latitude = location_results[0].get("latitude")
        longitude = location_results[0].get("longitude")
        return latitude, longitude

    except (KeyError, IndexError, TypeError):
        return None


def get_weather(latitude, longitude):
    weather_params = {"latitude": latitude, "longitude": longitude, "current": "temperature_2m",
                      "timezone": "auto"}
    weather_result = requests.get(FORECAST_URL, params=weather_params)
    weather_data = weather_result.json()
    current_weather = weather_data.get("current")

    temperature_2m = current_weather.get("temperature_2m")
    time = current_weather.get("time")
    return temperature_2m, time


if __name__ == "__main__":
    main()
