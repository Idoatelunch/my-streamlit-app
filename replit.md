# Weather App Documentation

## Overview

This is a bilingual (English/Hebrew) weather application built with Streamlit that provides weather information for Israeli cities. The app offers both single-city weather views and multi-city comparison functionality, with support for real-time weather data visualization and wind pattern overlays.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application framework
- **UI Components**: Interactive widgets, charts (Plotly), and custom CSS styling
- **Internationalization**: Dual language support with separate modules for English (`main.py`) and Hebrew (`main_hebrew.py`)
- **Navigation**: Sidebar-based navigation with radio button selection between different views

### Backend Architecture
- **API Layer**: `WeatherAPI` class that interfaces with OpenWeatherMap API
- **Data Processing**: Utility functions for temperature conversion and forecast data processing
- **Mock Data**: Built-in fallback system for demonstration purposes when API is unavailable

### Data Management
- **Session State**: Streamlit session state for managing user preferences and favorites
- **Local Storage**: JSON-based persistence for favorite cities
- **In-Memory Processing**: Real-time data processing for weather comparisons and visualizations

## Key Components

### Core Application Files
- `app.py`: Main entry point with language selection and routing logic
- `main.py`: English version of the weather application
- `main_hebrew.py`: Hebrew version with translated interface
- `weather_api.py`: Weather data API interface with mock data support

### Utility Modules
- `utils.py`: Helper functions for data processing, city search, and temperature conversion
- `styles.py`: Custom CSS styling for enhanced UI appearance
- `hebrew_translations.py`: Complete Hebrew translation dictionary

### Visualization Components
- `comparison_dashboard.py`: Multi-city weather comparison interface
- `comparison_dashboard_hebrew.py`: Hebrew version of comparison dashboard
- `wind_visualization.py`: Advanced wind pattern and precipitation overlay visualization

### Data Structures
- **City Management**: Predefined list of Israeli cities with fuzzy search capability
- **Weather Icons**: Mapping system for weather condition visualization
- **Coordinate System**: Geographic coordinate management for wind visualization

## Data Flow

1. **User Interaction**: User selects language and navigation options through Streamlit interface
2. **City Selection**: Users can search cities using fuzzy matching or select from favorites
3. **API Requests**: Weather data fetched from OpenWeatherMap API or mock data source
4. **Data Processing**: Raw weather data converted to display format with proper unit conversions
5. **Visualization**: Processed data rendered through Plotly charts and Streamlit components
6. **State Management**: User preferences and selections stored in session state

## External Dependencies

### Primary Libraries
- **Streamlit**: Web application framework for interactive dashboards
- **Plotly**: Advanced charting and visualization library
- **Pandas**: Data manipulation and analysis
- **Requests**: HTTP client for API communication
- **FuzzyWuzzy**: Fuzzy string matching for city search
- **NumPy**: Numerical computing for wind calculations

### API Services
- **OpenWeatherMap API**: Primary weather data source with fallback to mock data
- **Geographic Coordinates**: Built-in coordinate system for Israeli cities

### Features
- Temperature unit conversion (Celsius/Fahrenheit)
- Real-time weather data with 5-day forecasts
- **Real-time Wind & Precipitation AR Overlay** with animated wind flow patterns
- Interactive wind direction visualization with flowing arrows
- Multi-city weather comparison dashboard
- Favorites management system
- Responsive design with custom styling
- Precipitation intensity visualization (rain/snow halos)
- Smooth wind animation controls

## Deployment Strategy

### Replit Environment
- **Runtime**: Python-based Streamlit application
- **Dependencies**: Managed through standard Python package management
- **Configuration**: Environment-based API key management
- **Scalability**: Stateless design suitable for cloud deployment

### Mock Data Strategy
- Built-in demonstration mode when API keys are unavailable
- Realistic weather data simulation for development and testing
- Graceful degradation when external services are unavailable

### Performance Considerations
- Session state management for efficient user experience
- Lazy loading of weather data to minimize API calls
- Caching strategies for frequently accessed city data
- Optimized chart rendering for smooth interactions

## Recent Changes

### January 19, 2025 - Real-time Wind & Precipitation AR Overlay Implementation
- ✅ Successfully implemented animated wind arrows showing real-time wind flow patterns
- ✅ Fixed arrow direction calculations to show proper wind flow instead of spinning in place
- ✅ Added precipitation overlay with blue halos for rain/snow visualization
- ✅ Enhanced animation controls with intuitive "Flow Animation" button
- ✅ Improved wind visualization with filled arrowheads for better visibility
- ✅ Multi-city wind data integration for comprehensive AR experience
- ✅ Resolved map rendering issues with proper arrow display