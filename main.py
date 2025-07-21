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

def main():
    # Page config is now set in app.py
    
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
        selected_city = "Jerusalem"  # Default value
        
        if st.session_state.favorites:
            selected_favorite = st.sidebar.selectbox(
                "Select from Favorites",
                sorted(list(st.session_state.favorites)),
                key="favorite_selector"
            )
            if selected_favorite:
                selected_city = selected_favorite

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
                key="city_selector",
                index=ISRAELI_CITIES.index("Jerusalem") if "Jerusalem" in ISRAELI_CITIES else 0
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

        # Real-time Wind and Precipitation AR Overlay
        col_title, col_refresh = st.columns([3, 1])
        with col_title:
            st.markdown("## 🌬️ Real-time Wind & Precipitation AR Overlay")
        with col_refresh:
            if st.button("🔄 Refresh Data", help="Update AR overlay with latest weather data"):
                st.rerun()
        
        # Get multiple cities for comprehensive AR visualization
        city_coords = get_city_coordinates()
        
        # Enhance city data with weather information for AR overlay
        enhanced_cities = []
        for city_data in city_coords:
            try:
                # Get weather data for each city
                if city_data['city'] == selected_city:
                    # Use already fetched data for selected city
                    city_weather = current_weather
                else:
                    # Fetch weather for other cities
                    city_weather = weather_api.get_current_weather(city_data['city'])
                
                # Add weather data to city coordinates
                enhanced_city = city_data.copy()
                enhanced_city['wind_speed'] = city_weather.get('wind', {}).get('speed', 0)
                enhanced_city['wind_degree'] = city_weather.get('wind', {}).get('deg', 0)
                enhanced_city['wind_direction'] = city_weather.get('wind', {}).get('direction', 'N')
                enhanced_city['temperature'] = city_weather.get('main', {}).get('temp', 20)
                enhanced_city['humidity'] = city_weather.get('main', {}).get('humidity', 50)
                
                # Add precipitation data (rain or snow)
                precipitation = 0
                if 'rain' in city_weather:
                    precipitation = city_weather['rain'].get('1h', 0)
                elif 'snow' in city_weather:
                    precipitation = city_weather['snow'].get('1h', 0)
                enhanced_city['precipitation'] = precipitation
                
                enhanced_cities.append(enhanced_city)
                
            except Exception as e:
                # If we can't get weather for a city, skip it
                continue
        
        if enhanced_cities:
            # Create AR overlay with wind arrows and precipitation
            wind_fig = create_wind_overlay(enhanced_cities)
            st.plotly_chart(wind_fig, use_container_width=True, key="ar_overlay")
            
            # Enhanced AR info panel
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("""
                **🌪️ AR Weather Overlay Controls:**
                - 🔵 **Blue Circles**: City locations with live weather data
                - 🔴 **Red Arrows**: Real-time wind vectors (direction & speed)
                - 💧 **Blue Halos**: Active precipitation zones
                - 🌬️ **Click 'Flow Animation'** to activate wind flow simulation
                
                *Arrow length = wind speed • Arrow direction = wind flow*
                """)
            
            with col2:
                # Real-time weather stats
                st.markdown("**Live Weather Stats:**")
                avg_wind = sum(city.get('wind_speed', 0) for city in enhanced_cities) / len(enhanced_cities)
                active_precipitation = sum(1 for city in enhanced_cities if city.get('precipitation', 0) > 0)
                st.metric("Avg Wind Speed", f"{avg_wind:.1f} km/h")
                st.metric("Precipitation Zones", f"{active_precipitation} cities")
                
                # Weather intensity indicator
                max_wind = max(city.get('wind_speed', 0) for city in enhanced_cities)
                if max_wind > 15:
                    st.warning("⚠️ High Wind Alert")
                elif active_precipitation > 2:
                    st.info("🌧️ Multiple Rain Zones")
                else:
                    st.success("🌤️ Stable Conditions")
        else:
            st.warning("Unable to load weather data for AR visualization. Please try refreshing the page.")


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
        
        # Group by day and calculate numeric column means
        numeric_cols = ['temperature', 'humidity']
        daily_forecast = df.copy()
        daily_forecast['date'] = daily_forecast['datetime'].dt.date
        daily_means = daily_forecast.groupby('date')[numeric_cols].mean().reset_index()
        
        # Add datetime back for display
        daily_means['datetime'] = pd.to_datetime(daily_means['date'])
        
        for _, row in daily_means.iterrows():
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

if __name__ == "__main__":
    main()