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
    # Major Cities
    "Jerusalem",
    "Tel Aviv",
    "Haifa",
    "Rishon LeZion",
    "Petah Tikva",
    "Ashdod",
    "Netanya",
    "Be'er Sheva",
    "Holon",
    "Ramat Gan",

    # Regional Centers
    "Herzliya",
    "Rehovot",
    "Bat Yam",
    "Ashkelon",
    "Kfar Saba",
    "Ra'anana",
    "Modiin",
    "Nahariya",
    "Lod",
    "Givatayim",

    # Haifa Metropolitan Area (Krayot)
    "Kiryat Bialik",
    "Kiryat Motzkin",
    "Kiryat Yam",
    "Kiryat Ata",
    "Kiryat Haim",
    "Nesher",
    "Tirat Carmel",

    # Northern Cities
    "Tiberias",
    "Safed",
    "Acre",
    "Kiryat Shmona",
    "Afula",
    "Nazareth",
    "Migdal HaEmek",
    "Yokneam",
    "Kiryat Tivon",
    "Rosh Pina",
    "Metula",
    "Ma'alot-Tarshiha",
    "Karmiel",

    # Central Region
    "Ramat HaSharon",
    "Hod HaSharon",
    "Rosh HaAyin",
    "Yavne",
    "Ramla",
    "Ness Ziona",
    "Or Yehuda",
    "Ganei Tikva",
    "Kiryat Ono",
    "Shoham",
    "Even Yehuda",
    "Kadima-Zoran",
    "Tel Mond",
    "Kfar Yona",
    "Givat Shmuel",
    "Yehud",

    # Southern Cities
    "Eilat",
    "Dimona",
    "Arad",
    "Sderot",
    "Ofakim",
    "Kiryat Gat",
    "Yeroham",
    "Mitzpe Ramon",
    "Netivot",
    "Rahat",
    "Yeruham",
    "Kiryat Malakhi",
    "Beer Yaakov",
    "Kuseife",
    "Tel Sheva",
    "Lehavim",
    "Meitar",
    "Omer",

    # Sharon Region
    "Hadera",
    "Pardes Hanna-Karkur",
    "Zichron Yaakov",
    "Or Akiva",
    "Binyamina",
    "Givat Ada",
    "Karkur",
    "Caesarea",
    "Bat Hefer",
    "Ein Iron",
    "Kfar Yona",
    "Tel Mond",

    # Judea and Samaria
    "Maale Adumim",
    "Ariel",
    "Beitar Illit",
    "Modiin Illit",
    "Efrat",
    "Kiryat Arba",
    "Alfei Menashe",
    "Oranit",
    "Elkana",
    "Karnei Shomron",
    "Kedumim",
    "Beit El",
    "Kochav Yaakov",

    # Galilee Region
    "Karmiel",
    "Ma'alot-Tarshiha",
    "Sakhnin",
    "Tamra",
    "Shfaram",
    "Majd al-Krum",
    "Maghar",
    "Arraba",
    "I'billin",
    "Kafr Kanna",
    "Yafa an-Naseriyye",
    "Julis",
    "Abu Sinan",
    "Jadeidi-Makr"
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