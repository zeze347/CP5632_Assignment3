import requests

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
WIKI_SUMMARY_URL = "https://en.wikipedia.org/api/rest_v1/page/summary/"
HEADERS = {
    "User-Agent": "CP5632_Assignment (student project)"
}


def main():
    while True:
        city_name = get_valid_city()
        location = geocode_city(city_name)
        if location is None:
            print("City not found. Please try again.")
            continue
        latitude, longitude = location
        break

    temperature, time = get_weather(latitude, longitude)

    print(f"Time：{time}")
    print(f"Current temperature：{temperature} °C")

    summary = get_city_summary(city_name)
    print(f"Here is a summary of {city_name}:")
    print(summary)

def get_valid_city():
    while True:
        city_name = input("Enter a city name: ").strip()
        if not city_name:
            print("City name cannot be empty. Please try again.\n")
            continue
        elif city_name.isdigit():
            print("City name cannot be numbers only. Please try again.\n")
            continue
        return city_name

def geocode_city(city_name):
    try:
        geocode_params = {"name": city_name, "count": 1, "language": "en"}
        location_result = requests.get(GEOCODE_URL, params=geocode_params)
        geocode_data = location_result.json()
        location_results = geocode_data.get("results", [])
        result = location_results[0]
        if result.get("feature_code") not in ("PPLC", "PPLA"):
            print("Found a location but it's not classified as a city.")
            return None
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


def get_city_summary(city_name):
    try:
        page_title = city_name.replace(" ", "_")
        url = WIKI_SUMMARY_URL + page_title
        summary_result = requests.get(url, headers=HEADERS)
        summary_data = summary_result.json()
        summary = summary_data.get("extract")
        if summary is None:
            print("Summary not found. Please try again.\n")
        return summary

    except KeyError:
        return "Unexpected data format from Wikipedia."



if __name__ == "__main__":
    main()
