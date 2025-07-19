import streamlit as st
import plotly.express as px
import pandas as pd
from weather_api import WeatherAPI
from utils import (
    celsius_to_fahrenheit,
    process_forecast_data,
    ISRAELI_CITIES,
    WEATHER_ICONS
)
from hebrew_translations import translations

def show_comparison_dashboard():
    st.title(f"{translations['multi_city_comparison']} 📊")
    
    # Hebrew city translations
    city_translations = {
        "Jerusalem": "ירושלים",
        "Tel Aviv": "תל אביב",
        "Haifa": "חיפה",
        "Rishon LeZion": "ראשון לציון",
        "Petah Tikva": "פתח תקווה",
        "Ashdod": "אשדוד",
        "Netanya": "נתניה",
        "Be'er Sheva": "באר שבע",
        "Beer Sheva": "באר שבע",
        "Holon": "חולון",
        "Ramat Gan": "רמת גן",
        "Herzliya": "הרצליה",
        "Rehovot": "רחובות",
        "Bat Yam": "בת ים",
        "Ashkelon": "אשקלון",
        "Kfar Saba": "כפר סבא",
        "Ra'anana": "רעננה",
        "Modiin": "מודיעין",
        "Nahariya": "נהריה",
        "Lod": "לוד",
        "Givatayim": "גבעתיים",
        "Eilat": "אילת",
        "Nazareth": "נצרת",
        "Tiberias": "טבריה",
        "Safed": "צפת",
        "Acre": "עכו",
        "Hadera": "חדרה",
        "Ashkelon": "אשקלון", # Adding more common cities
        "Kiryat ShmONA": "קרית שמונה",
        "Dimona": "דימונה",
        "Ramat Hasharon": "רמפת השרון",
        "Ofakim": "אופקים",
        "Tzfat": "צפת",
        "Jaffa": "יפו",
        "Bnei Brak": "בני ברק",
        "Moshav": "מושב",
        "Kfar Yona": "כפר יונה",
        "Kiryat Ata": "קרית אתא",
        "Tirat Carmel": "טירת כרמל"
    }
    
    # Get selected cities
    if 'comparison_cities' not in st.session_state:
        st.session_state.comparison_cities = ["ירושלים", "תל אביב", "חיפה"]  # Default cities
    
    # City selection
    st.sidebar.markdown(f"## 🌍 {translations['select_cities_to_compare']}")
    
    # Create list of Hebrew city names
    hebrew_cities = []
    for city in ISRAELI_CITIES:
        if city in city_translations:
            hebrew_cities.append(city_translations[city])
        else:
            hebrew_cities.append(city)
    
    # Add/Remove cities
    new_city = st.sidebar.selectbox(translations['add_city_to_compare'], 
        [city for city in hebrew_cities if city not in st.session_state.comparison_cities],
        key="new_city_selector"
    )
    
    if st.sidebar.button(f"➕ {translations['add_city']}") and len(st.session_state.comparison_cities) < 5:
        st.session_state.comparison_cities.append(new_city)
        st.rerun()
    
    # Display selected cities with remove buttons
    st.sidebar.markdown(f"### {translations['selected_cities']}")
    for city in st.session_state.comparison_cities:
        col1, col2 = st.sidebar.columns([3, 1])
        col1.write(city)
        if col2.button("❌", key=f"remove_{city}") and len(st.session_state.comparison_cities) > 2:
            st.session_state.comparison_cities.remove(city)
            st.rerun()

    # Temperature unit selection
    use_celsius = st.sidebar.radio(translations['temperature_unit'], [translations['celsius'], translations['fahrenheit']]) == translations['celsius']

    try:
        weather_api = WeatherAPI()
        
        # Create comparison table
        st.markdown(f"## {translations['current_weather_comparison']}")
        
        weather_data = []
        for city in st.session_state.comparison_cities:
            current = weather_api.get_current_weather(city)
            temp = current['main']['temp']
            if not use_celsius:
                temp = celsius_to_fahrenheit(temp)
            
            weather_data.append({
                'City': city,
                'Temperature': temp,  # Store numeric values
                'TemperatureDisplay': f"{temp:.1f}°{'C' if use_celsius else 'F'}",  # For display only
                'Humidity': current['main']['humidity'],  # Store numeric values
                'HumidityDisplay': f"{current['main']['humidity']}%",  # For display only
                'Conditions': f"{WEATHER_ICONS.get(current['weather'][0]['icon'], '❓')} {current['weather'][0]['description']}"
            })
        
        # Display comparison table
        df_current = pd.DataFrame(weather_data)
        st.table(df_current)
        
        # Temperature comparison chart
        st.markdown(f"## {translations['temperature_comparison']}")
        
        # Collect forecast data for all cities
        forecast_data = []
        for city in st.session_state.comparison_cities:
            city_forecast = weather_api.get_forecast(city)
            df = process_forecast_data(city_forecast)
            if not use_celsius:
                df['temperature'] = df['temperature'].apply(celsius_to_fahrenheit)
            df['city'] = city
            forecast_data.append(df)
        
        # Combine all forecast data
        combined_forecast = pd.concat(forecast_data, ignore_index=True)
        
        # Create temperature trend chart
        fig = px.line(
            combined_forecast,
            x='datetime',
            y='temperature',
            color='city',
            title=f"{translations['five_day_temperature_forecast']}",
            labels={
                'datetime': translations['date'],
                'temperature': f"{translations['temperature']} (°{'C' if use_celsius else 'F'})",
                'city': translations['city']
            }
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Humidity comparison
        st.markdown(f"## {translations['humidity_comparison']}")
        fig_humidity = px.line(
            combined_forecast,
            x='datetime',
            y='humidity',
            color='city',
            title=f"{translations['five_day_humidity_forecast']}",
            labels={
                'datetime': translations['date'],
                'humidity': f"{translations['humidity']} (%)",
                'city': translations['city']
            }
        )
        st.plotly_chart(fig_humidity, use_container_width=True)
    
    except Exception as e:
        st.error(f"{translations['error_fetching_weather']}: {str(e)}")