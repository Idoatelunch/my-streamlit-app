
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Weather App / אפליקציית מזג אוויר",
    page_icon="🌤️",
    layout="wide"
)

# Center content
st.markdown("""
<style>
    .centered {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 70vh;
        text-align: center;
    }
    .btn-container {
        display: flex;
        gap: 20px;
        margin-top: 20px;
    }
    .language-btn {
        padding: 10px 20px;
        font-size: 1.2rem;
        border-radius: 5px;
        cursor: pointer;
        text-decoration: none;
        background-color: #f0f2f6;
        color: #0e1117;
        border: 1px solid #dadce0;
        transition: all 0.3s;
    }
    .language-btn:hover {
        background-color: #e0e2e6;
    }
</style>
""", unsafe_allow_html=True)

# App content
st.markdown("""
<div class="centered">
    <h1>Welcome to the Israel Weather App</h1>
    <h1>ברוכים הבאים לאפליקציית מזג האוויר בישראל</h1>
    <p>Choose your preferred language / בחר את השפה המועדפת עליך</p>
    <div class="btn-container">
        <a href="?app=english" target="_self" class="language-btn">English 🇬🇧</a>
        <a href="?app=hebrew" target="_self" class="language-btn">עברית 🇮🇱</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Get the query parameter
query_params = st.query_params
app_version = query_params.get("app", "")

# Launch the selected app
if app_version == "english":
    import main as m
    m.main()
elif app_version == "hebrew":
    import main_hebrew as m
    m.main()
