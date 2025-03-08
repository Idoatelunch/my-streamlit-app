import requests
import os
from typing import Dict, List, Optional
import json

class WeatherAPI:
    def __init__(self):
        # Get API key from environment
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
            raise ValueError("OpenWeatherMap API key not found in environment variables")

        self.base_url = "https://api.openweathermap.org/data/2.5"
        # Validate API key on initialization
        self._validate_api_key()

    def _validate_api_key(self):
        """Validate the API key with a test request"""
        try:
            response = requests.get(
                f"{self.base_url}/weather",
                params={
                    "q": "Jerusalem,IL",
                    "appid": self.api_key,
                    "units": "metric"
                },
                timeout=10
            )

            if response.status_code == 401:
                try:
                    error_data = response.json()
                    error_msg = error_data.get('message', 'Unknown error')
                    if 'Invalid API key' in error_msg:
                        raise ValueError(
                            "Invalid API key. Please ensure:\n"
                            "1. The key is copied correctly without spaces\n"
                            "2. The key is activated (takes ~2 hours after creation)\n"
                            "3. The key matches the one in your OpenWeatherMap dashboard"
                        )
                except json.JSONDecodeError:
                    raise ValueError("Invalid API key. Please check your OpenWeatherMap API key")

            response.raise_for_status()

        except requests.exceptions.Timeout:
            raise ValueError("Connection timed out. Please try again")
        except requests.exceptions.RequestException as e:
            if "401" in str(e):
                raise ValueError(
                    "API key authentication failed. Please verify your API key is correct and activated"
                )
            raise ValueError(f"Failed to validate API key: {str(e)}")

    def get_current_weather(self, city: str) -> Dict:
        """Fetch current weather data for a city"""
        try:
            response = requests.get(
                f"{self.base_url}/weather",
                params={
                    "q": f"{city},IL",
                    "appid": self.api_key,
                    "units": "metric"
                },
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if "401" in str(e):
                raise ValueError("API key authentication failed. Please check your OpenWeatherMap API key")
            raise Exception(f"Failed to fetch current weather: {str(e)}")

    def get_forecast(self, city: str) -> Dict:
        """Fetch 5-day forecast data for a city"""
        try:
            response = requests.get(
                f"{self.base_url}/forecast",
                params={
                    "q": f"{city},IL",
                    "appid": self.api_key,
                    "units": "metric"
                },
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if "401" in str(e):
                raise ValueError("API key authentication failed. Please check your OpenWeatherMap API key")
            raise Exception(f"Failed to fetch forecast: {str(e)}")