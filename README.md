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

In the terminal, type the following command and press Enter:`pip install requests`
On macOS / Linux, if pip doesn't work, try:`pip3 install requests`

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

| API                      | Purpose                                            | Documentation Link                                                             |
|--------------------------|----------------------------------------------------|--------------------------------------------------------------------------------|
| Open-Meteo Geocoding API | Convert city name into latitude & longitude        | https://open-meteo.com/en/docs/geocoding-api                                   |
| Open-Meteo Forecast API  | Get current temperature using latitude & longitude | https://open-meteo.com/en/docs                                                 |
| Wikipedia Summary API    | Return a short summary of the city                 | https://en.wikipedia.org/api/rest_v1/#/Page%20content/get_page_summary__title_ |

### Understanding How the Program Uses APIs

In the program, we first ask the user to input a city name, and then send this name to
the [Open-Meteo Geocoding API](https://geocoding-api.open-meteo.com/v1/search).
This API will return JSON data, which contains geographical information. We extract two fields from it: latitude and
longitude, as they are the parameters required for weather queries.

```python
latitude = location_results[0].get("latitude")
longitude = location_results[0].get("longitude")
```

Next, we pass the latitude and longitude to the [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast), which
returns a JSON containing the
current_weather. We then extract the temperature and time fields from this JSON.

```python
weather_params = {"latitude": latitude, "longitude": longitude, "current": "temperature_2m",
                  "timezone": "auto"}
weather_result = requests.get(FORECAST_URL, params=weather_params, timeout=REQUEST_TIMEOUT)
weather_data = weather_result.json()
current_weather = weather_data.get("current")
```

Finally, we input the names of the cities into
the [Wikipedia Summary API](https://en.wikipedia.org/api/rest_v1/page/summary/).Add the name of the city after the
URL.The API will then return a field named "extract", which contains the brief introduction of the city.

```python
url = WIKI_SUMMARY_URL + page_title
summary_result = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
summary_data = summary_result.json()
summary = summary_data.get("extract")
```

## Reflection

Before starting this assignment, my understanding of APIs was merely at the conceptual level, and I had never actually
implemented the functionality for API interaction. After the project began, the biggest challenge was understanding the
Json data returned by the API. The data returned by each API is different, and the documentation doesn't tell me which
fields are the ones I need. What I did was to continuously print the content of the Json to observe which fields were
the key information I needed (such as `latitude` and `longitude`)
And, when writing the program, I encountered many problems. To address these issues, I added input validation to check
if
`results` is empty, and used `try/except` to catch and handle any exceptions. In addition, I found that the Open-Meteo
Geocoding API can locate some small cities and even rural areas. However, most unknown cities may not be recorded in
Wikipedia. The solution is to check the `feature_code` when parsing the JSON data returned by the Geocoding API, to
ensure that the input city does not include small towns.Overall, this assignment enabled me to truly master the
interaction with real-time online APIs, understand the JSON data structure, learn to extract the required fields from
it, and enhance my debugging skills and problem-solving abilities.  

Furthermore, I also learned the importance of modular programming. At the beginning, I placed all the logic in the main
function, which made my code very difficult to maintain. After splitting the logic into multiple small functions, the
readability of my program became extremely high, making it very clear at a glance. The structure was also very clear,
making it easy to debug and modify. I also realized that real APIs do not always return ideal data, so input validation
and error handling are the key to the robustness of the program.

## Conclusion

This project gave me hands-on experience with working APIs, understanding JSON structures, and designing a robust Python
program. It helped me gain confidence in both programming logic and data processing using real-world web services.
