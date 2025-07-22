from typing import Dict, Optional
import requests

class WeatherAPI:
    """Class to interact with the weather API"""

    def __init__(self):
        self.base_url = "https://api.openweathermap.org/data/2.5"
        # Get API key from environment variable
        import os
        self.api_key = os.environ.get('OPENWEATHER_API_KEY')
        # Use mock data only if no API key is provided
        self.use_mock_data = not bool(self.api_key)
        
        # Debug: Print API key status (without revealing the actual key)
        if self.api_key:
            print(f"✅ API Key found - Length: {len(self.api_key)} characters")
            print("🌤️ Using REAL weather data from OpenWeatherMap")
        else:
            print("⚠️ No API key found - Using MOCK weather data")
            print("💡 Add OPENWEATHER_API_KEY to your Secrets to use real data")

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
        
        if self.use_mock_data:
            return self._get_mock_current_weather(query_city)
            
        # For actual API use when you have a valid key
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
        
    def _get_mock_current_weather(self, city: str) -> Dict:
        """Provide mock weather data for demonstration"""
        import random
        from datetime import datetime
        
        # Create realistic mock data
        temp = round(random.uniform(15, 35), 1)
        humidity = random.randint(30, 80)
        wind_speed = round(random.uniform(1, 10), 1)
        wind_deg = random.randint(0, 359)
        
        # Weather conditions and precipitation based on temperature and randomness
        precipitation_chance = random.random()
        has_precipitation = precipitation_chance > 0.7  # 30% chance of precipitation
        
        if temp > 30:
            condition = "clear sky"
            icon = "01d"
        elif temp > 25:
            condition = "few clouds"
            icon = "02d"
        elif temp > 20:
            if has_precipitation:
                condition = "light rain"
                icon = "10d"
            else:
                condition = "scattered clouds"
                icon = "03d"
        elif temp > 15:
            if has_precipitation:
                condition = "moderate rain"
                icon = "10d"
            else:
                condition = "broken clouds"
                icon = "04d"
        else:
            if has_precipitation:
                condition = "heavy rain"
                icon = "10d"
            else:
                condition = "overcast clouds"
                icon = "04d"
        
        # Create base weather data
        weather_data = {
            "coord": {"lon": 35.21, "lat": 31.77},
            "weather": [{"id": 800, "main": "Clear", "description": condition, "icon": icon}],
            "base": "stations",
            "main": {
                "temp": temp,
                "feels_like": temp - 2,
                "temp_min": temp - 3,
                "temp_max": temp + 3,
                "pressure": 1013,
                "humidity": humidity
            },
            "visibility": 10000,
            "wind": {
                "speed": wind_speed,
                "deg": wind_deg,
                "direction": self.get_wind_direction(wind_deg)
            },
            "clouds": {"all": random.randint(0, 100)},
            "dt": datetime.now().timestamp(),
            "sys": {
                "type": 1,
                "id": 6854,
                "country": "IL",
                "sunrise": 1661834187,
                "sunset": 1661882048
            },
            "timezone": 10800,
            "id": 281184,
            "name": city,
            "cod": 200
        }
        
        # Add precipitation data if present
        if has_precipitation:
            if temp > 2:  # Rain
                precipitation_amount = round(random.uniform(0.5, 5.0), 1)
                weather_data["rain"] = {"1h": precipitation_amount}
            else:  # Snow (rare in Israel but possible)
                precipitation_amount = round(random.uniform(0.1, 2.0), 1)
                weather_data["snow"] = {"1h": precipitation_amount}
        
        return weather_data

    def get_forecast(self, city: str) -> Dict:
        """Get forecast for a city"""
        # Translate Hebrew city names to English if necessary
        if city in self.hebrew_to_english:
            query_city = self.hebrew_to_english[city]
        else:
            query_city = city
            
        if self.use_mock_data:
            return self._get_mock_forecast(query_city)

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
        
    def _get_mock_forecast(self, city: str) -> Dict:
        """Provide mock forecast data for demonstration"""
        import random
        from datetime import datetime, timedelta
        
        # Base temperature for the city with some seasonal adjustment
        current_month = datetime.now().month
        is_summer = 4 <= current_month <= 10
        base_temp = random.uniform(25, 33) if is_summer else random.uniform(10, 20)
        
        # Generate forecast data for the next 5 days
        forecast_list = []
        start_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        for day in range(5):
            # For each day, create 8 timestamps (every 3 hours)
            for hour in [0, 3, 6, 9, 12, 15, 18, 21]:
                current_time = start_time + timedelta(days=day, hours=hour)
                
                # Temperature varies by time of day
                hour_adjustment = 0
                if 6 <= hour < 12:
                    hour_adjustment = 2  # Morning warming
                elif 12 <= hour < 18:
                    hour_adjustment = 4  # Afternoon peak
                elif 18 <= hour < 21:
                    hour_adjustment = 1  # Evening cooling
                
                # Add some random variation
                temp = base_temp + hour_adjustment + random.uniform(-2, 2)
                humidity = random.randint(30, 80)
                
                # Weather conditions based on temperature and time
                if temp > 30:
                    condition = "clear sky"
                    icon = "01d" if 6 <= hour < 18 else "01n"
                elif temp > 25:
                    condition = "few clouds"
                    icon = "02d" if 6 <= hour < 18 else "02n"
                elif temp > 20:
                    condition = "scattered clouds"
                    icon = "03d" if 6 <= hour < 18 else "03n"
                elif temp > 15:
                    condition = "broken clouds"
                    icon = "04d" if 6 <= hour < 18 else "04n"
                else:
                    condition = "light rain"
                    icon = "10d" if 6 <= hour < 18 else "10n"
                
                forecast_list.append({
                    "dt": int(current_time.timestamp()),
                    "main": {
                        "temp": temp,
                        "feels_like": temp - 2,
                        "temp_min": temp - 1,
                        "temp_max": temp + 1,
                        "pressure": 1013,
                        "humidity": humidity,
                        "sea_level": 1013,
                        "grnd_level": 952
                    },
                    "weather": [
                        {
                            "id": 800 if temp > 25 else 801,
                            "main": "Clear" if temp > 25 else "Clouds",
                            "description": condition,
                            "icon": icon
                        }
                    ],
                    "clouds": {"all": random.randint(0, 100)},
                    "wind": {
                        "speed": random.uniform(1, 8),
                        "deg": random.randint(0, 359)
                    },
                    "visibility": 10000,
                    "pop": 0.2 if temp < 20 else 0,
                    "sys": {"pod": "d" if 6 <= hour < 18 else "n"},
                    "dt_txt": current_time.strftime("%Y-%m-%d %H:%M:%S")
                })
                
        return {
            "cod": "200",
            "message": 0,
            "cnt": len(forecast_list),
            "list": forecast_list,
            "city": {
                "id": 281184,
                "name": city,
                "coord": {"lat": 31.77, "lon": 35.21},
                "country": "IL",
                "population": 1000000,
                "timezone": 10800,
                "sunrise": 1661834187,
                "sunset": 1661882048
            }
        }

    def get_wind_direction(self, degrees: float) -> str:
        """Convert wind degrees to cardinal direction"""
        directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]
        index = round(degrees / 45)
        return directions[index]