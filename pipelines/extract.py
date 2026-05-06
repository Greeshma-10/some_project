import requests


def fetch_weather(latitude: float, longitude: float, start_date: str, end_date: str) -> dict:
    """
    Fetch historical weather data from Open-Meteo archive API.
    """

    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "temperature_2m_max,temperature_2m_min",
        "timezone": "auto"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()