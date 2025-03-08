
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
from comparison_dashboard_hebrew import show_comparison_dashboard
from wind_visualization import create_wind_overlay, get_city_coordinates
from hebrew_translations import translations

def main():
    # Page config is now set in app.py
    
    # Apply custom styles
    apply_custom_styles()

    # Navigation
    st.sidebar.title(translations["navigation"])
    page = st.sidebar.radio(translations["select_view"], [translations["single_city_weather"], translations["city_comparison"]])

    if page == translations["single_city_weather"]:
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
        st.sidebar.markdown(f"## ⚙️ {translations['settings']}")

        # Favorites section
        st.sidebar.markdown(f"## ⭐ {translations['favorite_cities']}")
        if st.session_state.favorites:
            selected_favorite = st.sidebar.selectbox(
                translations["select_from_favorites"],
                sorted(list(st.session_state.favorites)),
                key="favorite_selector"
            )
            if selected_favorite:
                selected_city = selected_favorite
        else:
            st.sidebar.info(translations["no_favorites"])

        # City search with autocomplete
        city_search = st.sidebar.text_input(f"🔍 {translations['search_city']}", "")
        if city_search:
            matching_cities = search_cities(city_search)
            if matching_cities:
                selected_city = st.sidebar.selectbox(
                    translations["select_city"],
                    matching_cities,
                    key="city_selector"
                )
            else:
                st.sidebar.warning(translations["no_matching_cities"])
                selected_city = "ירושלים"  # Default to Jerusalem if no matches
        else:
            selected_city = st.sidebar.selectbox(
                translations["select_city"],
                ISRAELI_CITIES,
                key="city_selector"
            )

        # Favorite toggle button
        col1, col2 = st.sidebar.columns([3, 1])
        with col1:
            st.write(f"{translations['selected']}: {selected_city}")
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

        use_celsius = st.sidebar.radio(translations["temperature_unit"], [translations["celsius"], translations["fahrenheit"]]) == translations["celsius"]

        # Main content
        st.title(f"{translations['weather_in']} {selected_city}, {translations['israel']} 🌤️")

        try:
            # Current weather
            with st.spinner(translations["fetching_current_weather"]):
                current_weather = weather_api.get_current_weather(selected_city)

            # Display current weather
            col1, col2, col3 = st.columns(3)

            temp = current_weather['main']['temp']
            if not use_celsius:
                temp = celsius_to_fahrenheit(temp)

            with col1:
                st.markdown(f"### {translations['temperature']}")
                st.markdown(f"### {temp:.1f}°{'C' if use_celsius else 'F'}")

            with col2:
                st.markdown(f"### {translations['humidity']}")
                st.markdown(f"### {current_weather['main']['humidity']}%")

            with col3:
                st.markdown(f"### {translations['conditions']}")
                icon = current_weather['weather'][0]['icon']
                st.markdown(f"### {WEATHER_ICONS.get(icon, '❓')} {current_weather['weather'][0]['description'].capitalize()}")

            # Wind Visualization
            st.markdown(f"## {translations['real_time_wind']} 🌬️")
            city_coords = get_city_coordinates()

            # Update wind data for visualization
            for city_data in city_coords:
                if city_data.get('hebrew_city') == selected_city or city_data['city'] == selected_city:
                    # Initialize wind properties
                    city_data['wind_speed'] = current_weather['wind']['speed']
                    city_data['wind_degree'] = current_weather['wind']['deg']
                    city_data['wind_direction'] = current_weather['wind']['direction']
                    break

            # Create and display wind visualization
            wind_fig = create_wind_overlay(city_coords)
            st.plotly_chart(wind_fig, use_container_width=True)

            # Forecast
            st.markdown(f"## {translations['five_day_forecast']}")
            with st.spinner(translations["fetching_forecast_data"]):
                forecast_data = weather_api.get_forecast(selected_city)
                df = process_forecast_data(forecast_data)

            if not use_celsius:
                df['temperature'] = df['temperature'].apply(celsius_to_fahrenheit)

            # Create temperature trend chart
            fig = px.line(
                df,
                x='datetime',
                y='temperature',
                title=f"{translations['temperature_trend']} ({selected_city})",
                labels={
                    'datetime': translations['date'],
                    'temperature': f"{translations['temperature']} (°{'C' if use_celsius else 'F'})"
                }
            )
            fig.update_layout(
                xaxis_title=translations['date'],
                yaxis_title=f"{translations['temperature']} (°{'C' if use_celsius else 'F'})"
            )
            st.plotly_chart(fig, use_container_width=True)

            # Daily forecast cards
            st.markdown(f"### {translations['daily_details']}")
            
            # Group by day and calculate numeric column means
            numeric_cols = ['temperature', 'humidity']
            daily_forecast = df.copy()
            daily_forecast['date'] = daily_forecast['datetime'].dt.date
            daily_means = daily_forecast.groupby('date')[numeric_cols].mean().reset_index()
            
            # Add datetime back for display
            daily_means['datetime'] = pd.to_datetime(daily_means['date'])
            
            # Hebrew day and month names
            hebrew_days = {
                'Monday': 'יום שני',
                'Tuesday': 'יום שלישי',
                'Wednesday': 'יום רביעי',
                'Thursday': 'יום חמישי',
                'Friday': 'יום שישי',
                'Saturday': 'יום שבת',
                'Sunday': 'יום ראשון'
            }
            
            hebrew_months = {
                'January': 'ינואר',
                'February': 'פברואר',
                'March': 'מרץ',
                'April': 'אפריל',
                'May': 'מאי',
                'June': 'יוני',
                'July': 'יולי',
                'August': 'אוגוסט',
                'September': 'ספטמבר',
                'October': 'אוקטובר',
                'November': 'נובמבר',
                'December': 'דצמבר'
            }
            
            for _, row in daily_means.iterrows():
                # Get English format first
                english_day = row['datetime'].strftime('%A')
                english_month = row['datetime'].strftime('%B')
                day_num = row['datetime'].strftime('%d')
                
                # Convert to Hebrew
                hebrew_day = hebrew_days.get(english_day, english_day)
                hebrew_month = hebrew_months.get(english_month, english_month)
                
                with st.container():
                    st.markdown(f"""
                        <div class="weather-card">
                            <h4>{hebrew_day}, {hebrew_month} {day_num}</h4>
                            <p>{translations['temperature']}: {row['temperature']:.1f}°{'C' if use_celsius else 'F'}</p>
                            <p>{translations['humidity']}: {row['humidity']:.0f}%</p>
                        </div>
                    """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"{translations['error_fetching_weather']}: {str(e)}")

    else:
        # Show comparison dashboard
        show_comparison_dashboard()

if __name__ == "__main__":
    main()
