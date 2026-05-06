"""
Transform raw JSON weather response into structured DataFrame.
"""

import pandas as pd


def transform_weather(json_data: dict, city: str) -> pd.DataFrame:
    """
    Convert Open-Meteo JSON response into a clean DataFrame.
    """

    daily = json_data.get("daily", {})

    df = pd.DataFrame({
        "date": daily.get("time"),
        "temp_max": daily.get("temperature_2m_max"),
        "temp_min": daily.get("temperature_2m_min"),
    })

    df["city"] = city

    return df