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
            background-color: #f0f2f6;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
        }
        .metric-label {
            font-size: 0.8rem;
            color: #666;
        }
        .metric-value {
            font-size: 1.5rem;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)
