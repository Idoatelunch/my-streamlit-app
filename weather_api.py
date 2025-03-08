import requests
import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class WeatherAPI:
    def __init__(self):
        # Get API key from environment
        self.api_key = os.getenv("WEATHERAPI_KEY")
        if not self.api_key:
            raise ValueError("WeatherAPI.com key not found in environment variables")

        self.base_url = "http://api.weatherapi.com/v1"

    def get_current_weather(self, city: str) -> Dict:
        """Fetch current weather data for a city"""
        try:
            response = requests.get(
                f"{self.base_url}/current.json",
                params={
                    "key": self.api_key,
                    "q": f"{city},Israel",
                    "aqi": "no"
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return self._format_current_weather(data)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch current weather: {str(e)}")

    def get_forecast(self, city: str) -> Dict:
        """Fetch 5-day forecast data for a city"""
        try:
            response = requests.get(
                f"{self.base_url}/forecast.json",
                params={
                    "key": self.api_key,
                    "q": f"{city},Israel",
                    "days": 5,
                    "aqi": "no"
                },
                timeout=10
            )
            response.raise_for_status()
            return self._format_forecast_data(response.json())
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch forecast: {str(e)}")

    def _format_current_weather(self, data: Dict) -> Dict:
        """Format WeatherAPI.com current weather data to match our app's structure"""
        current = data.get('current', {})
        condition = current.get('condition', {})

        return {
            'main': {
                'temp': current.get('temp_c', 0),
                'humidity': current.get('humidity', 0)
            },
            'weather': [{
                'description': condition.get('text', 'Unknown'),
                'icon': self._get_weather_icon(condition.get('code', 1000))
            }],
            'wind': {
                'speed': current.get('wind_kph', 0),
                'deg': current.get('wind_degree', 0),
                'direction': current.get('wind_dir', 'N')
            }
        }

    def _format_forecast_data(self, data: Dict) -> Dict:
        """Format WeatherAPI.com forecast data to match our app's structure"""
        forecast_days = data.get('forecast', {}).get('forecastday', [])
        forecast_list = []

        for day in forecast_days:
            day_data = day.get('day', {})
            condition = day_data.get('condition', {})
            hour_data = day.get('hour', [])

            # Get hourly wind data
            wind_data = []
            for hour in hour_data:
                wind_data.append({
                    'time': hour.get('time'),
                    'wind_kph': hour.get('wind_kph', 0),
                    'wind_degree': hour.get('wind_degree', 0),
                    'wind_dir': hour.get('wind_dir', 'N')
                })

            forecast_list.append({
                'dt': int(datetime.strptime(day['date'], '%Y-%m-%d').timestamp()),
                'main': {
                    'temp': day_data.get('avgtemp_c', 0),
                    'humidity': day_data.get('avghumidity', 0)
                },
                'weather': [{
                    'description': condition.get('text', 'Unknown'),
                    'icon': self._get_weather_icon(condition.get('code', 1000))
                }],
                'wind_data': wind_data
            })

        return {'list': forecast_list}

    def _get_weather_icon(self, code: int) -> str:
        """Convert WeatherAPI.com weather codes to our icon codes"""
        # Mapping WeatherAPI.com codes to our icon set
        code_map = {
            1000: "01d",  # Clear
            1003: "02d",  # Partly cloudy
            1006: "03d",  # Cloudy
            1009: "04d",  # Overcast
            1030: "50d",  # Mist
            1063: "09d",  # Patchy rain
            1186: "10d",  # Moderate rain
            1189: "10d",  # Moderate rain
            1192: "11d",  # Heavy rain
            1195: "11d",  # Heavy rain
            1273: "11d",  # Patchy light rain with thunder
            1276: "11d",  # Moderate or heavy rain with thunder
        }
        return code_map.get(code, "01d")  # Default to clear sky if code not found