import streamlit as st

def apply_custom_styles():
    """Apply custom CSS styles to the Streamlit app"""
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stButton>button {
            width: 100%;
        }
        .weather-card {
            background-color: var(--background-color);
            border: 1px solid var(--secondary-background-color);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        
        .weather-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        /* Dark mode support */
        [data-theme="dark"] .weather-card {
            background-color: #262730;
            border-color: #404040;
            color: #ffffff;
        }
        
        /* Light mode fallback */
        [data-theme="light"] .weather-card {
            background-color: #ffffff;
            border-color: #e6e6e6;
            color: #000000;
        }
        
        /* Auto-detect system theme */
        @media (prefers-color-scheme: dark) {
            .weather-card {
                background-color: #262730 !important;
                border-color: #404040 !important;
                color: #ffffff !important;
            }
        }
        
        @media (prefers-color-scheme: light) {
            .weather-card {
                background-color: #ffffff !important;
                border-color: #e6e6e6 !important;
                color: #000000 !important;
            }
        }
        .metric-label {
            font-size: 0.8rem;
            color: #666;
        }
        .metric-value {
            font-size: 1.5rem;
            font-weight: bold;
        }
        /* Favorite button styles */
        .stButton>button:hover {
            background-color: #f0f2f6;
        }
        .favorites-section {
            margin-top: 2rem;
            padding: 1rem;
            border-radius: 10px;
            background-color: #f8f9fa;
        }
        
        /* Enhanced dark mode support for all elements */
        @media (prefers-color-scheme: dark) {
            .favorites-section {
                background-color: #1e1e1e !important;
                border: 1px solid #404040;
            }
            
            /* Fix metric cards in dark mode */
            .metric-container {
                background-color: #262730 !important;
                border: 1px solid #404040 !important;
                border-radius: 8px;
                padding: 1rem;
            }
            
            /* Better text contrast */
            .metric-label {
                color: #cccccc !important;
            }
            
            /* Improved button styling for dark mode */
            .stButton > button {
                background-color: #262730 !important;
                color: #ffffff !important;
                border: 1px solid #404040 !important;
            }
            
            .stButton > button:hover {
                background-color: #404040 !important;
                border-color: #606060 !important;
            }
        }
        
        /* Light mode enhancements */
        @media (prefers-color-scheme: light) {
            .metric-container {
                background-color: #ffffff;
                border: 1px solid #e6e6e6;
                border-radius: 8px;
                padding: 1rem;
            }
        }
        
        /* Weather cards specific improvements */
        .weather-card h4 {
            margin-top: 0;
            margin-bottom: 1rem;
            font-weight: 600;
        }
        
        .weather-card p {
            margin: 0.5rem 0;
            line-height: 1.4;
        }
        </style>
    """, unsafe_allow_html=True)