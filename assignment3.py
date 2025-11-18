"""
Filename: assignment3.py
Subject: CP5632
Name: Jiaxing Tian
Introduction:
This program retrieves the current weather and a brief Wikipedia summary for a given city.
It uses three APIs: Open-Meteo Geocoding API, Open-Meteo Forecast API, and Wikipedia Summary API.
"""
import requests

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
WIKI_SUMMARY_URL = "https://en.wikipedia.org/api/rest_v1/page/summary/"
REQUEST_TIMEOUT = 10
HEADERS = {
    "User-Agent": "CP5632_Assignment (student project)"
}


def main():
    """Main program: get a valid city, fetch weather and Wikipedia summary."""
    choice = "y"
    while choice.lower().startswith("y"):
        city_name = get_valid_city()
        location = geocode_city(city_name)
        while location is None:
            print("City not found. Please try again.\n")
            city_name = get_valid_city()
            location = geocode_city(city_name)
        latitude, longitude, timezone = location
        temperature, time = get_weather(latitude, longitude)
        print(f"City: {city_name}\n"
              f"Latitude:{latitude}, Longitude:{longitude}\n"
              f"Time:{time}, timezone:{timezone}\n"
              f"Current temperature：{temperature} °C\n")
        summary = get_city_summary(city_name)
        print(f"Here is a summary of {city_name}:")
        print(summary)
        choice = input("Would you like to continue searching for other cities? (y/n): ").strip()
    print("Thank you for using this program.")


def get_valid_city():
    """Get a valid city name (not empty or numeric)."""
    city_name = ""
    while not city_name or city_name.isdigit():
        city_name = input("Enter a city name: ").strip()
        if not city_name:
            print("City name cannot be empty. Please try again.\n")
        elif city_name.isdigit():
            print("City name cannot be numbers only. Please try again.\n")
    return city_name


def geocode_city(city_name):
    """Return geographic information if the name refers to a city."""
    try:
        geocode_params = {"name": city_name, "count": 1, "language": "en"}
        location_result = requests.get(GEOCODE_URL, params=geocode_params, timeout=REQUEST_TIMEOUT)
        geocode_data = location_result.json()
        location_results = geocode_data.get("results", [])
        result = location_results[0]
        valid_codes = (
            "PPLC", "PPLA", "PPLA2", "PPLA3",
            "PPLA4", "PPL", "ADM2", "ADM3"
        )
        if result.get("feature_code") not in valid_codes:
            print("Found a location but it's not classified as a city.")
            return None
        latitude = location_results[0].get("latitude")
        longitude = location_results[0].get("longitude")
        timezone = location_results[0].get("timezone")
        return latitude, longitude, timezone

    except (KeyError, IndexError, TypeError):
        return None


def get_weather(latitude, longitude):
    """Return the current temperature and time for the given coordinates."""
    weather_params = {"latitude": latitude, "longitude": longitude, "current": "temperature_2m",
                      "timezone": "auto"}
    weather_result = requests.get(FORECAST_URL, params=weather_params, timeout=REQUEST_TIMEOUT)
    weather_data = weather_result.json()
    current_weather = weather_data.get("current")

    temperature_2m = current_weather.get("temperature_2m")
    time = current_weather.get("time")
    return temperature_2m, time


def get_city_summary(city_name):
    """Return Wikipedia summary of the given city."""
    try:
        page_title = city_name.replace(" ", "_")
        url = WIKI_SUMMARY_URL + page_title
        summary_result = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        summary_data = summary_result.json()
        summary = summary_data.get("extract")
        if summary is None:
            print("Summary not found. Please try again.\n")
        return summary

    except KeyError:
        return "Unexpected data format from Wikipedia."


if __name__ == "__main__":
    main()
