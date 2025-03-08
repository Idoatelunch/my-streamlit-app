import requests
import os
from typing import Dict, List, Optional

# OpenWeatherMap API key from environment variable
API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
BASE_URL = "https://api.openweathermap.org/data/2.5"

class WeatherAPI:
    def __init__(self):
        if not API_KEY:
            raise ValueError("OpenWeatherMap API key not found in environment variables")

    def get_current_weather(self, city: str) -> Dict:
        """Fetch current weather data for a city"""
        try:
            response = requests.get(
                f"{BASE_URL}/weather",
                params={
                    "q": f"{city},IL",
                    "appid": API_KEY,
                    "units": "metric"
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch current weather: {str(e)}")

    def get_forecast(self, city: str) -> List[Dict]:
        """Fetch 5-day forecast data for a city"""
        try:
            response = requests.get(
                f"{BASE_URL}/forecast",
                params={
                    "q": f"{city},IL",
                    "appid": API_KEY,
                    "units": "metric"
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch forecast: {str(e)}")
