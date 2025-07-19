import streamlit as st
import plotly.graph_objects as go
import numpy as np
from typing import List, Dict
import json
import math

# Israel map boundaries (approximate)
ISRAEL_BOUNDS = {
    'lat': (29.5, 33.3),  # South to North
    'lon': (34.2, 35.9)   # West to East
}

def create_wind_arrows(lat, lon, wind_speed, wind_direction_deg, color='red', scale=0.05):
    """Create arrow coordinates for wind visualization"""
    # Convert wind direction to radians (wind direction is where wind is coming FROM)
    # So we need to add 180 degrees to show where wind is going TO
    direction_rad = np.radians((wind_direction_deg + 180) % 360)
    
    # Scale arrow length based on wind speed
    length = wind_speed * scale
    
    # Calculate arrow tip coordinates
    end_lat = lat + length * np.cos(direction_rad)
    end_lon = lon + length * np.sin(direction_rad)
    
    # Create arrowhead
    arrow_angle = np.radians(30)  # 30 degree arrowhead
    head_length = length * 0.3
    
    # Left arrowhead point
    left_lat = end_lat - head_length * np.cos(direction_rad - arrow_angle)
    left_lon = end_lon - head_length * np.sin(direction_rad - arrow_angle)
    
    # Right arrowhead point
    right_lat = end_lat - head_length * np.cos(direction_rad + arrow_angle)
    right_lon = end_lon - head_length * np.sin(direction_rad + arrow_angle)
    
    return {
        'shaft': {'lat': [lat, end_lat], 'lon': [lon, end_lon]},
        'head': {'lat': [left_lat, end_lat, right_lat], 'lon': [left_lon, end_lon, right_lon]}
    }

def create_wind_overlay(city_data: List[Dict]):
    """Create an animated wind and precipitation overlay for Israeli cities"""
    
    # Create figure with map
    fig = go.Figure()

    # Add city markers with weather info
    valid_cities = [city for city in city_data if 'wind_speed' in city and 'wind_degree' in city]
    
    if not valid_cities:
        st.warning("No wind data available for visualization")
        return fig

    # Add city markers
    fig.add_trace(go.Scattermapbox(
        lat=[city['lat'] for city in valid_cities],
        lon=[city['lon'] for city in valid_cities],
        mode='markers+text',
        marker=dict(
            size=15,
            color='blue',
            symbol='circle'
        ),
        text=[city.get('hebrew_city', city['city']) for city in valid_cities],
        textposition="bottom center",
        textfont=dict(size=12, color='black'),
        name='Cities',
        hovertemplate='<b>%{text}</b><br>Click to see details<extra></extra>'
    ))

    # Add precipitation layer if available
    for city in valid_cities:
        if 'precipitation' in city and city['precipitation'] > 0:
            # Add precipitation circles
            fig.add_trace(go.Scattermapbox(
                lat=[city['lat']],
                lon=[city['lon']],
                mode='markers',
                marker=dict(
                    size=city['precipitation'] * 3,  # Scale size by precipitation
                    color='rgba(0, 100, 255, 0.3)',
                    symbol='circle'
                ),
                name=f"Rain - {city['city']}",
                showlegend=False,
                hovertemplate=f"<b>{city['city']}</b><br>Precipitation: {city['precipitation']}mm<extra></extra>"
            ))

    # Create animated wind arrows
    frames = []
    base_traces = list(fig.data)  # Keep city markers and precipitation
    
    for frame_i in range(12):  # 12 frames for smooth animation
        frame_traces = base_traces.copy()
        
        for city in valid_cities:
            # Add slight animation by rotating wind direction slightly
            animated_direction = (city['wind_degree'] + frame_i * 3) % 360
            
            # Create wind arrow
            arrow = create_wind_arrows(
                city['lat'], 
                city['lon'], 
                city['wind_speed'], 
                animated_direction,
                color='red',
                scale=0.008  # Adjusted scale for better visibility
            )
            
            # Add arrow shaft
            frame_traces.append(go.Scattermapbox(
                lat=arrow['shaft']['lat'],
                lon=arrow['shaft']['lon'],
                mode='lines',
                line=dict(width=3, color='red'),
                name=f"Wind - {city['city']}",
                showlegend=False,
                hovertemplate=f"<b>{city['city']}</b><br>Wind Speed: {city['wind_speed']} km/h<br>Direction: {city.get('wind_direction', 'N/A')}<extra></extra>"
            ))
            
            # Add arrowhead
            frame_traces.append(go.Scattermapbox(
                lat=arrow['head']['lat'],
                lon=arrow['head']['lon'],
                mode='lines',
                line=dict(width=3, color='red'),
                showlegend=False,
                hovertemplate=f"<b>{city['city']}</b><br>Wind Speed: {city['wind_speed']} km/h<extra></extra>"
            ))
        
        frames.append(go.Frame(data=frame_traces, name=f'frame{frame_i}'))

    # Add initial wind arrows to the base figure
    for city in valid_cities:
        arrow = create_wind_arrows(
            city['lat'], 
            city['lon'], 
            city['wind_speed'], 
            city['wind_degree'],
            scale=0.008
        )
        
        # Add arrow shaft
        fig.add_trace(go.Scattermapbox(
            lat=arrow['shaft']['lat'],
            lon=arrow['shaft']['lon'],
            mode='lines',
            line=dict(width=3, color='red'),
            name=f"Wind - {city['city']}",
            showlegend=False,
            hovertemplate=f"<b>{city['city']}</b><br>Wind Speed: {city['wind_speed']} km/h<br>Direction: {city.get('wind_direction', 'N/A')}<extra></extra>"
        ))
        
        # Add arrowhead
        fig.add_trace(go.Scattermapbox(
            lat=arrow['head']['lat'],
            lon=arrow['head']['lon'],
            mode='lines',
            line=dict(width=3, color='red'),
            showlegend=False,
            hovertemplate=f"<b>{city['city']}</b><br>Wind Speed: {city['wind_speed']} km/h<extra></extra>"
        ))

    # Add frames to figure
    fig.frames = frames

    # Configure layout and animation
    fig.update_layout(
        mapbox=dict(
            style='open-street-map',  # Changed to a more reliable map style
            center=dict(lat=31.4, lon=35.0),
            zoom=7,
        ),
        updatemenus=[dict(
            type='buttons',
            showactive=False,
            y=0.9,
            x=0.1,
            buttons=[
                dict(
                    label='▶ Animate Wind',
                    method='animate',
                    args=[None, dict(
                        frame=dict(duration=200, redraw=True),
                        fromcurrent=True,
                        mode='immediate',
                        transition=dict(duration=100)
                    )]
                ),
                dict(
                    label='⏸ Stop',
                    method='animate',
                    args=[[None], dict(
                        frame=dict(duration=0, redraw=False),
                        mode='immediate',
                        transition=dict(duration=0)
                    )]
                )
            ]
        )],
        showlegend=True,
        margin=dict(l=0, r=0, t=40, b=0),
        height=600,
        title={
            'text': "Real-time Wind & Precipitation AR Overlay",
            'x': 0.5,
            'xanchor': 'center'
        }
    )

    return fig

def get_city_coordinates():
    """Return hardcoded coordinates for major Israeli cities"""
    return [
        {"city": "Jerusalem", "hebrew_city": "ירושלים", "lat": 31.7683, "lon": 35.2137},
        {"city": "Tel Aviv", "hebrew_city": "תל אביב", "lat": 32.0853, "lon": 34.7818},
        {"city": "Haifa", "hebrew_city": "חיפה", "lat": 32.7940, "lon": 34.9896},
        {"city": "Beer Sheva", "hebrew_city": "באר שבע", "lat": 31.2516, "lon": 34.7915},
        {"city": "Eilat", "hebrew_city": "אילת", "lat": 29.5577, "lon": 34.9519},
        {"city": "Netanya", "hebrew_city": "נתניה", "lat": 32.3329, "lon": 34.8599},
        {"city": "Nazareth", "hebrew_city": "נצרת", "lat": 32.7021, "lon": 35.2978},
        {"city": "Ashdod", "hebrew_city": "אשדוד", "lat": 31.8044, "lon": 34.6448}
    ]
