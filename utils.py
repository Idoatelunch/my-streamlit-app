from typing import Dict, List
import pandas as pd
from datetime import datetime
from fuzzywuzzy import fuzz

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

def search_cities(query: str, min_score: int = 60) -> List[str]:
    """Search Israeli cities using fuzzy matching"""
    matches = []
    for city in ISRAELI_CITIES:
        # Calculate fuzzy match score
        score = fuzz.partial_ratio(query.lower(), city.lower())
        if score >= min_score:
            matches.append(city)
    return sorted(matches)

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
    "Rishon LeZion",
    "Petah Tikva",
    "Bat Yam",
    "Holon",
    "Ramat Gan",
    "Rehovot",
    "Kfar Saba",
    "Ra'anana",
    "Nahariya",
    "Lod",
    "Modiin"
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