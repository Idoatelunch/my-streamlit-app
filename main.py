import streamlit as st
import plotly.express as px
from datetime import datetime
import pandas as pd
import json
from weather_api import WeatherAPI
from utils import (
    celsius_to_fahrenheit,
    process_forecast_data,
    ISRAELI_CITIES,
    WEATHER_ICONS,
    search_cities
)
from styles import apply_custom_styles
from comparison_dashboard import show_comparison_dashboard
from wind_visualization import create_wind_overlay, get_city_coordinates # Added import


# Page configuration
st.set_page_config(
    page_title="Israel Weather App",
    page_icon="🌤️",
    layout="wide"
)

# Apply custom styles
apply_custom_styles()

# Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select View", ["Single City Weather", "City Comparison"])

if page == "Single City Weather":
    # Initialize WeatherAPI
    try:
        weather_api = WeatherAPI()
    except ValueError as e:
        st.error(str(e))
        st.stop()

    # Initialize favorites in session state
    if 'favorites' not in st.session_state:
        # Try to load favorites from local storage
        favorites_json = st.session_state.get('_favorites_json', '[]')
        try:
            st.session_state.favorites = set(json.loads(favorites_json))
        except json.JSONDecodeError:
            st.session_state.favorites = set()

    # Settings section
    st.sidebar.markdown("## ⚙️ Settings")

    # Favorites section
    st.sidebar.markdown("## ⭐ Favorite Cities")
    if st.session_state.favorites:
        selected_favorite = st.sidebar.selectbox(
            "Select from Favorites",
            sorted(list(st.session_state.favorites)),
            key="favorite_selector"
        )
        if selected_favorite:
            selected_city = selected_favorite
    else:
        st.sidebar.info("No favorite cities yet. Add some cities to your favorites!")

    # City search with autocomplete
    city_search = st.sidebar.text_input("🔍 Search City", "")
    if city_search:
        matching_cities = search_cities(city_search)
        if matching_cities:
            selected_city = st.sidebar.selectbox(
                "Select City",
                matching_cities,
                key="city_selector"
            )
        else:
            st.sidebar.warning("No matching cities found")
            selected_city = "Jerusalem"  # Default to Jerusalem if no matches
    else:
        selected_city = st.sidebar.selectbox(
            "Select City",
            ISRAELI_CITIES,
            key="city_selector"
        )

    # Favorite toggle button
    col1, col2 = st.sidebar.columns([3, 1])
    with col1:
        st.write(f"Selected: {selected_city}")
    with col2:
        if selected_city in st.session_state.favorites:
            if st.button("❤️", key=f"unfav_{selected_city}"):
                st.session_state.favorites.remove(selected_city)
                # Save to local storage
                st.session_state['_favorites_json'] = json.dumps(list(st.session_state.favorites))
                st.rerun()
        else:
            if st.button("🤍", key=f"fav_{selected_city}"):
                st.session_state.favorites.add(selected_city)
                # Save to local storage
                st.session_state['_favorites_json'] = json.dumps(list(st.session_state.favorites))
                st.rerun()

    use_celsius = st.sidebar.radio("Temperature Unit", ["Celsius", "Fahrenheit"]) == "Celsius"

    # Main content
    st.title(f"Weather in {selected_city}, Israel 🌤️")

    try:
        # Current weather
        with st.spinner("Fetching current weather..."):
            current_weather = weather_api.get_current_weather(selected_city)

        # Display current weather
        col1, col2, col3 = st.columns(3)

        temp = current_weather['main']['temp']
        if not use_celsius:
            temp = celsius_to_fahrenheit(temp)

        with col1:
            st.markdown("### Temperature")
            st.markdown(f"### {temp:.1f}°{'C' if use_celsius else 'F'}")

        with col2:
            st.markdown("### Humidity")
            st.markdown(f"### {current_weather['main']['humidity']}%")

        with col3:
            st.markdown("### Conditions")
            icon = current_weather['weather'][0]['icon']
            st.markdown(f"### {WEATHER_ICONS.get(icon, '❓')} {current_weather['weather'][0]['description'].capitalize()}")

        # Wind Visualization
        st.markdown("## Real-time Wind Conditions 🌬️")
        city_coords = get_city_coordinates()

        # Update wind data for visualization
        for city_data in city_coords:
            if city_data['city'] == selected_city:
                city_data['wind_speed'] = current_weather['wind'].get('speed', 0)
                city_data['wind_degree'] = current_weather['wind'].get('deg', 0)
                city_data['wind_direction'] = current_weather['wind'].get('direction', 'N')
                break

        # Create and display wind visualization
        wind_fig = create_wind_overlay(city_coords)
        st.plotly_chart(wind_fig, use_container_width=True)


        # Forecast
        st.markdown("## 5-Day Forecast")
        with st.spinner("Fetching forecast data..."):
            forecast_data = weather_api.get_forecast(selected_city)
            df = process_forecast_data(forecast_data)

        if not use_celsius:
            df['temperature'] = df['temperature'].apply(celsius_to_fahrenheit)

        # Create temperature trend chart
        fig = px.line(
            df,
            x='datetime',
            y='temperature',
            title=f"Temperature Trend ({selected_city})",
            labels={
                'datetime': 'Date',
                'temperature': f'Temperature (°{"C" if use_celsius else "F"})'
            }
        )
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title=f"Temperature (°{'C' if use_celsius else 'F'})"
        )
        st.plotly_chart(fig, use_container_width=True)

        # Daily forecast cards
        st.markdown("### Daily Details")
        daily_forecast = df.set_index('datetime').resample('D').mean().reset_index()

        for _, row in daily_forecast.iterrows():
            with st.container():
                st.markdown(f"""
                    <div class="weather-card">
                        <h4>{row['datetime'].strftime('%A, %B %d')}</h4>
                        <p>Temperature: {row['temperature']:.1f}°{'C' if use_celsius else 'F'}</p>
                        <p>Humidity: {row['humidity']:.0f}%</p>
                    </div>
                """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error fetching weather data: {str(e)}")

else:
    # Show comparison dashboard
    show_comparison_dashboard()