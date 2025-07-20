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

def create_wind_arrows(lat, lon, wind_speed, wind_direction_deg, color='red', scale=0.02):
    """Create arrow coordinates for wind visualization"""
    # Convert meteorological wind direction (where wind comes FROM) to mathematical angle
    # Meteorological: 0° = North, 90° = East, 180° = South, 270° = West
    # Mathematical: 0° = East, 90° = North, 180° = West, 270° = South
    # We want to show where wind is GOING TO (add 180°) and convert to math coordinates
    math_angle = np.radians(90 - wind_direction_deg)  # Convert to math coordinates
    
    # Scale arrow length based on wind speed (minimum visible length)
    length = max(wind_speed * scale, 0.01)
    
    # Calculate arrow endpoint
    end_lat = lat + length * np.sin(math_angle)
    end_lon = lon + length * np.cos(math_angle)
    
    # Create arrowhead points
    head_angle = np.radians(25)  # Narrower arrowhead
    head_length = length * 0.4
    
    # Calculate arrowhead points
    left_angle = math_angle + head_angle + np.pi
    right_angle = math_angle - head_angle + np.pi
    
    left_lat = end_lat + head_length * np.sin(left_angle)
    left_lon = end_lon + head_length * np.cos(left_angle)
    
    right_lat = end_lat + head_length * np.sin(right_angle)
    right_lon = end_lon + head_length * np.cos(right_angle)
    
    return {
        'shaft': {'lat': [lat, end_lat], 'lon': [lon, end_lon]},
        'head': {'lat': [left_lat, end_lat, right_lat, left_lat], 'lon': [left_lon, end_lon, right_lon, left_lon]},
        'wind_speed': wind_speed,
        'direction': wind_direction_deg
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

    # Add city markers with temperature color coding
    temperatures = [city.get('temperature', 20) for city in valid_cities]
    fig.add_trace(go.Scattermapbox(
        lat=[city['lat'] for city in valid_cities],
        lon=[city['lon'] for city in valid_cities],
        mode='markers+text',
        marker=dict(
            size=18,
            color=temperatures,
            colorscale='RdYlBu_r',  # Red for hot, blue for cold
            cmin=0,
            cmax=40,
            symbol='circle',
            colorbar=dict(
                title="Temperature (°C)",
                x=1.02,
                len=0.7
            )
        ),
        text=[city.get('hebrew_city', city['city']) for city in valid_cities],
        textposition="bottom center",
        textfont=dict(size=11, color='white'),
        name='Cities',
        hovertemplate='<b>%{text}</b><br>Temperature: %{marker.color:.1f}°C<br>Click for details<extra></extra>'
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

    # Create animated wind flow patterns - simplified for better performance
    frames = []
    base_traces = list(fig.data)  # Keep city markers and precipitation
    
    for frame_i in range(8):  # Reduced frames for better performance
        frame_traces = base_traces.copy()
        
        for city in valid_cities:
            wind_direction = city['wind_degree']
            wind_speed = city['wind_speed']
            
            # Create flowing effect by moving arrow position along wind direction
            flow_distance = (frame_i / 8.0) * 0.05  # Flow distance based on frame
            math_angle = np.radians(90 - wind_direction)
            
            # Calculate flowing position
            flow_lat = city['lat'] + flow_distance * np.sin(math_angle)
            flow_lon = city['lon'] + flow_distance * np.cos(math_angle)
            
            # Create wind arrow at flowing position
            arrow = create_wind_arrows(
                flow_lat,
                flow_lon,
                wind_speed,
                wind_direction,
                scale=0.015
            )
            
            # Add arrow shaft
            frame_traces.append(go.Scattermapbox(
                lat=arrow['shaft']['lat'],
                lon=arrow['shaft']['lon'],
                mode='lines',
                line=dict(width=4, color='red'),
                name=f"Wind - {city['city']}",
                showlegend=False,
                hovertemplate=f"<b>{city['city']}</b><br>Wind Speed: {city['wind_speed']} km/h<br>Direction: {city.get('wind_direction', 'N/A')}<extra></extra>"
            ))
            
            # Add arrowhead as filled polygon
            frame_traces.append(go.Scattermapbox(
                lat=arrow['head']['lat'],
                lon=arrow['head']['lon'],
                mode='lines',
                line=dict(width=4, color='red'),
                fill='toself',
                fillcolor='red',
                showlegend=False,
                hovertemplate=f"<b>{city['city']}</b><br>Wind Speed: {city['wind_speed']} km/h<extra></extra>"
            ))
        
        frames.append(go.Frame(data=frame_traces, name=f'frame{frame_i}'))

    # Add initial static wind arrows to the base figure
    for city in valid_cities:
        arrow = create_wind_arrows(
            city['lat'], 
            city['lon'], 
            city['wind_speed'], 
            city['wind_degree'],
            scale=0.015
        )
        
        # Add arrow shaft
        fig.add_trace(go.Scattermapbox(
            lat=arrow['shaft']['lat'],
            lon=arrow['shaft']['lon'],
            mode='lines',
            line=dict(width=4, color='darkred'),
            name=f"Wind - {city['city']}",
            showlegend=False,
            hovertemplate=f"<b>{city['city']}</b><br>Wind Speed: {city['wind_speed']} km/h<br>Direction: {city.get('wind_direction', 'N/A')}<extra></extra>"
        ))
        
        # Add arrowhead as filled polygon
        fig.add_trace(go.Scattermapbox(
            lat=arrow['head']['lat'],
            lon=arrow['head']['lon'],
            mode='lines',
            line=dict(width=4, color='darkred'),
            fill='toself',
            fillcolor='darkred',
            showlegend=False,
            hovertemplate=f"<b>{city['city']}</b><br>Wind Speed: {city['wind_speed']} km/h<br>Direction: {city.get('wind_direction', 'N/A')}<extra></extra>"
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
            y=0.95,
            x=0.02,
            bgcolor='rgba(255,255,255,0.8)',
            bordercolor='gray',
            borderwidth=1,
            buttons=[
                dict(
                    label='🌬️ Flow Animation',
                    method='animate',
                    args=[None, dict(
                        frame=dict(duration=400, redraw=True),
                        fromcurrent=True,
                        mode='immediate',
                        transition=dict(duration=100)
                    )]
                ),
                dict(
                    label='⏹️ Stop',
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
            'text': "🌍 Real-time Weather AR Overlay - Israel",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16}
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
