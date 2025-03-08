import streamlit as st
import plotly.graph_objects as go
import numpy as np
from typing import List, Dict
import json

# Israel map boundaries (approximate)
ISRAEL_BOUNDS = {
    'lat': (29.5, 33.3),  # South to North
    'lon': (34.2, 35.9)   # West to East
}

def create_wind_overlay(city_data: List[Dict]):
    """Create an animated wind overlay for Israeli cities"""
    
    # Create figure with map
    fig = go.Figure()

    # Add base map - use Hebrew city names if available
    fig.add_trace(go.Scattermapbox(
        lat=[data['lat'] for data in city_data],
        lon=[data['lon'] for data in city_data],
        mode='markers+text',
        marker=dict(size=10),
        text=[data.get('hebrew_city', data['city']) for data in city_data],
        textposition="top center",
        name='Cities'
    ))

    # Create wind arrows for animation
    frames = []
    for i in range(8):  # 8 frames for smooth animation
        arrow_traces = []
        for city in city_data:
            # Check if all required wind data is present
            if 'wind_speed' not in city or 'wind_degree' not in city:
                continue  # Skip this city if wind data is incomplete
                
            # Calculate arrow endpoint using wind direction and speed
            wind_degree = city['wind_degree']
            angle = np.radians(wind_degree)
            wind_speed = city['wind_speed']
            speed_factor = wind_speed / 50.0  # Normalize arrow length
            
            # Calculate arrow endpoint
            dx = speed_factor * np.cos(angle) * 0.1
            dy = speed_factor * np.sin(angle) * 0.1
            
            # Create arrow
            arrow_traces.append(
                go.Scattermapbox(
                    lat=[city['lat'], city['lat'] + dy],
                    lon=[city['lon'], city['lon'] + dx],
                    mode='lines',
                    line=dict(width=2, color='red'),
                    name=f"Wind - {city['city']}",
                    showlegend=False,
                    hovertext=f"Wind Speed: {city['wind_speed']} km/h<br>Direction: {city['wind_direction']}"
                )
            )
        
        frames.append(go.Frame(data=arrow_traces, name=f'frame{i}'))

    # Add frames to figure
    fig.frames = frames

    # Configure animation
    fig.update_layout(
        mapbox=dict(
            style='carto-positron',
            center=dict(lat=31.4, lon=35.0),
            zoom=6,
        ),
        updatemenus=[dict(
            type='buttons',
            showactive=False,
            buttons=[dict(
                label='Play',
                method='animate',
                args=[None, dict(
                    frame=dict(duration=100, redraw=True),
                    fromcurrent=True,
                    mode='immediate'
                )]
            )]
        )],
        showlegend=True,
        margin=dict(l=0, r=0, t=0, b=0)
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
        {"city": "Ashdod", "hebrew_city": "אשדוד", "lat": 31.8040, "lon": 34.6580},
        {"city": "Rishon LeZion", "hebrew_city": "ראשון לציון", "lat": 31.9640, "lon": 34.8044},
        {"city": "Petah Tikva", "hebrew_city": "פתח תקווה", "lat": 32.0868, "lon": 34.8876},
        {"city": "Holon", "hebrew_city": "חולון", "lat": 32.0111, "lon": 34.7792},
        {"city": "Ramat Gan", "hebrew_city": "רמת גן", "lat": 32.0684, "lon": 34.8248},
        {"city": "Herzliya", "hebrew_city": "הרצליה", "lat": 32.1660, "lon": 34.8394},
        {"city": "Rehovot", "hebrew_city": "רחובות", "lat": 31.8929, "lon": 34.8113},
        {"city": "Bat Yam", "hebrew_city": "בת ים", "lat": 32.0247, "lon": 34.7537},
        {"city": "Ashkelon", "hebrew_city": "אשקלון", "lat": 31.6690, "lon": 34.5715},
        {"city": "Kfar Saba", "hebrew_city": "כפר סבא", "lat": 32.1749, "lon": 34.9060},
        {"city": "Ra'anana", "hebrew_city": "רעננה", "lat": 32.1836, "lon": 34.8746},
        {"city": "Modiin", "hebrew_city": "מודיעין", "lat": 31.8964, "lon": 35.0053},
        {"city": "Nahariya", "hebrew_city": "נהריה", "lat": 33.0040, "lon": 35.0950},
        {"city": "Lod", "hebrew_city": "לוד", "lat": 31.9510, "lon": 34.8890},
        {"city": "Givatayim", "hebrew_city": "גבעתיים", "lat": 32.0724, "lon": 34.8124},
        {"city": "Tiberias", "hebrew_city": "טבריה", "lat": 32.7963, "lon": 35.5301},
        {"city": "Safed", "hebrew_city": "צפת", "lat": 32.9646, "lon": 35.4960},
        {"city": "Acre", "hebrew_city": "עכו", "lat": 32.9276, "lon": 35.0825},
        {"city": "Hadera", "hebrew_city": "חדרה", "lat": 32.4410, "lon": 34.9039}ד", "lat": 31.8044, "lon": 34.6448}
    ]
