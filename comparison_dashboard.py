import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime

from weather_api import WeatherAPI
from utils import (
    celsius_to_fahrenheit,
    process_forecast_data,
    ISRAELI_CITIES,
    WEATHER_ICONS,
    search_cities
)

def show_comparison_dashboard():
    st.title("Multi-City Weather Comparison 📊")
    
    # Get selected cities
    if 'comparison_cities' not in st.session_state:
        st.session_state.comparison_cities = ["Jerusalem", "Tel Aviv", "Haifa"]  # Default cities
    
    # City selection
    st.sidebar.markdown("## 🌍 Select Cities to Compare")
    
    # Add/Remove cities
    new_city = st.sidebar.selectbox("Add a city to compare", 
        [city for city in ISRAELI_CITIES if city not in st.session_state.comparison_cities],
        key="new_city_selector"
    )
    
    if st.sidebar.button("➕ Add City") and len(st.session_state.comparison_cities) < 5:
        st.session_state.comparison_cities.append(new_city)
        st.rerun()
    
    # Display selected cities with remove buttons
    st.sidebar.markdown("### Selected Cities")
    for city in st.session_state.comparison_cities:
        col1, col2 = st.sidebar.columns([3, 1])
        col1.write(city)
        if col2.button("❌", key=f"remove_{city}") and len(st.session_state.comparison_cities) > 2:
            st.session_state.comparison_cities.remove(city)
            st.rerun()

    # Temperature unit selection
    use_celsius = st.sidebar.radio("Temperature Unit", ["Celsius", "Fahrenheit"]) == "Celsius"

    try:
        weather_api = WeatherAPI()
        
        # Create comparison table
        st.markdown("## Current Weather Comparison")
        
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
        st.markdown("## Temperature Comparison")
        
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
            title=f"5-Day Temperature Forecast Comparison",
            labels={
                'datetime': 'Date',
                'temperature': f'Temperature (°{"C" if use_celsius else "F"})',
                'city': 'City'
            }
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Humidity comparison
        st.markdown("## Humidity Comparison")
        fig_humidity = px.line(
            combined_forecast,
            x='datetime',
            y='humidity',
            color='city',
            title=f"5-Day Humidity Forecast Comparison",
            labels={
                'datetime': 'Date',
                'humidity': 'Humidity (%)',
                'city': 'City'
            }
        )
        st.plotly_chart(fig_humidity, use_container_width=True)

    except Exception as e:
        st.error(f"Error fetching weather data: {str(e)}")
