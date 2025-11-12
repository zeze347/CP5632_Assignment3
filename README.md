# City Weather & Wiki Summary Program

## Introduction

This program mainly demonstrates how to use multiple APIs in Python.
The user enters a city name, and the program retrieves:

- The city's latitude and longitude (using Open-Meteo Geocoding API)
- The current temperature (using Open-Meteo Forecast API)
- A short summary/introduction about the city (using Wikipedia Summary API)
- The purpose of this assignment is to practice integrating multiple APIs, parsing JSON data, validating user input,
  handling errors, and writing clean modular code using functions.

## How to Install & Run

### Requirements

- Python 3.x
- `requests` library

### Installation

Open Terminal / Command Prompt based on your operating system:

- Windows: Press Win + R → type cmd → press Enter
- macOS: Press ⌘ + Space → type Terminal → press Enter
- Linux: Search for Terminal from applications menu

In the terminal, type the following command and press Enter:"pip install requests"
On macOS / Linux, if pip doesn't work, try:"pip3 install requests"

### How to run

Program interaction flow:
The program asks the user to enter a city name:
Enter a city name:
The program validates the input (city cannot be empty or numbers only).
If the city is valid, the program will:

- Retrieve the latitude and longitude of the city
- Retrieve the current temperature of the city
- Retrieve a short city summary from Wikipedia

## APIs Use

| API  / Name              | / Purpose                                          | / Documentation Link                                                           |
|--------------------------|----------------------------------------------------|--------------------------------------------------------------------------------|
| Open-Meteo Geocoding API | Convert city name into latitude & longitude        | https://open-meteo.com/en/docs/geocoding-api                                   |
| Open-Meteo Forecast API  | Get current temperature using latitude & longitude | https://open-meteo.com/en/docs                                                 |
| Wikipedia Summary API    | Return a short summary of the city                 | https://en.wikipedia.org/api/rest_v1/#/Page%20content/get_page_summary__title_ |

### 1. Open-Meteo Geocoding API

In the program, we first ask the user to input a city name, and then send this name to
the [OpeOpen-Meteo Geocoding API](https://geocoding-api.open-meteo.com/v1/search）.
This API will return JSON data, which contains geographical information. We extract two fields from it: latitude and
longitude, as they are the parameters required for weather queries.

```python
latitude = location_results[0].get("latitude")
longitude = location_results[0].get("longitude")
```

Next, we pass the latitude and longitude to the [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast), which
returns a JSON containing the
current_weather. We then extract the temperature and time fields from this JSON.
Finally, we input the names of the cities into
the [Wikipedia Summary API](https://en.wikipedia.org/api/rest_v1/page/summary/).Add the name of the city after the
URL.The API will then return a field named "extract", which contains the brief introduction of the city.




