from typing import Dict, Optional
import requests

class WeatherAPI:
    """Class to interact with the weather API"""

    def __init__(self):
        self.base_url = "https://api.openweathermap.org/data/2.5"
        # Use a demo API key for development/testing that doesn't require signup
        self.api_key = "b6907d289e10d714a6e88b30761fae22"

        # Hebrew city translations
        self.hebrew_to_english = {
            "ירושלים": "Jerusalem",
            "תל אביב": "Tel Aviv",
            "חיפה": "Haifa",
            "ראשון לציון": "Rishon LeZion",
            "פתח תקווה": "Petah Tikva",
            "אשדוד": "Ashdod",
            "נתניה": "Netanya",
            "באר שבע": "Beer Sheva",
            "חולון": "Holon",
            "רמת גן": "Ramat Gan",
            "הרצליה": "Herzliya",
            "רחובות": "Rehovot",
            "בת ים": "Bat Yam",
            "אשקלון": "Ashkelon",
            "כפר סבא": "Kfar Saba",
            "רעננה": "Ra'anana",
            "מודיעין": "Modiin",
            "נהריה": "Nahariya",
            "לוד": "Lod",
            "גבעתיים": "Givatayim",
            "אילת": "Eilat",
            "נצרת": "Nazareth",
            "טבריה": "Tiberias",
            "צפת": "Safed",
            "עכו": "Acre",
            "חדרה": "Hadera"
        }

    def get_current_weather(self, city: str) -> Dict:
        """Get current weather for a city"""
        # Translate Hebrew city names to English if necessary
        if city in self.hebrew_to_english:
            query_city = self.hebrew_to_english[city]
        else:
            query_city = city

        # Since we're using a demo API key with limited access, 
        # we'll use a specified endpoint that works with the demo key
        url = f"{self.base_url}/weather"
        params = {
            "q": f"{query_city},IL",
            "appid": self.api_key,
            "units": "metric"  # For Celsius
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch weather data for {city}: {response.text}")

        data = response.json()

        # Add wind direction based on degrees
        if 'wind' in data and 'deg' in data['wind']:
            data['wind']['direction'] = self.get_wind_direction(data['wind']['deg'])

        return data

    def get_forecast(self, city: str) -> Dict:
        """Get forecast for a city"""
        # Translate Hebrew city names to English if necessary
        if city in self.hebrew_to_english:
            query_city = self.hebrew_to_english[city]
        else:
            query_city = city

        url = f"{self.base_url}/forecast"
        params = {
            "q": f"{query_city},IL",
            "appid": self.api_key,
            "units": "metric"  # For Celsius
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch forecast data for {city}: {response.text}")

        return response.json()

    def get_wind_direction(self, degrees: float) -> str:
        """Convert wind degrees to cardinal direction"""
        directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]
        index = round(degrees / 45)
        return directions[index]