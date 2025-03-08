from typing import Dict, List
import pandas as pd
from datetime import datetime

def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit"""
    return (celsius * 9/5) + 32

def process_forecast_data(forecast_data: Dict) -> pd.DataFrame:
    """Process forecast data into a pandas DataFrame"""
    forecasts = []
    for item in forecast_data['list']:
        forecasts.append({
            'datetime': datetime.fromtimestamp(item['dt']),
            'temperature': item['main']['temp'],
            'humidity': item['main']['humidity'],
            'description': item['weather'][0]['description'],
            'icon': item['weather'][0]['icon']
        })
    return pd.DataFrame(forecasts)

ISRAELI_CITIES = [
    "Jerusalem",
    "Tel Aviv",
    "Haifa",
    "Eilat",
    "Be'er Sheva",
    "Netanya",
    "Ashdod",
    "Ashkelon",
    "Herzliya",
    "Rishon LeZion"
]

WEATHER_ICONS = {
    "01d": "☀️",
    "02d": "⛅",
    "03d": "☁️",
    "04d": "☁️",
    "09d": "🌧️",
    "10d": "🌦️",
    "11d": "⛈️",
    "13d": "🌨️",
    "50d": "🌫️",
    "01n": "🌙",
    "02n": "☁️",
    "03n": "☁️",
    "04n": "☁️",
    "09n": "🌧️",
    "10n": "🌧️",
    "11n": "⛈️",
    "13n": "🌨️",
    "50n": "🌫️"
}
