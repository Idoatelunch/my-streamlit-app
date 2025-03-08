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

    # Add base map
    fig.add_trace(go.Scattermapbox(
        lat=[data['lat'] for data in city_data],
        lon=[data['lon'] for data in city_data],
        mode='markers+text',
        marker=dict(size=10),
        text=[data['city'] for data in city_data],
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
        {"city": "Jerusalem", "lat": 31.7683, "lon": 35.2137},
        {"city": "Tel Aviv", "lat": 32.0853, "lon": 34.7818},
        {"city": "Haifa", "lat": 32.7940, "lon": 34.9896},
        {"city": "Beer Sheva", "lat": 31.2516, "lon": 34.7915},
        {"city": "Eilat", "lat": 29.5577, "lon": 34.9519},
        {"city": "Netanya", "lat": 32.3329, "lon": 34.8599},
        {"city": "Nazareth", "lat": 32.7021, "lon": 35.2978},
        {"city": "Ashdod", "lat": 31.8044, "lon": 34.6448}
    ]
