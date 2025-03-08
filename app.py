import streamlit as st

# Always set page config first before any other Streamlit commands
st.set_page_config(
    page_title="Weather App / אפליקציית מזג אוויר",
    page_icon="🌤️",
    layout="wide"
)

# Get the query parameter
query_params = st.query_params
app_version = query_params.get("app", "")

# Based on the version parameter, either show language selector or load the specific app
if app_version in ["english", "hebrew"]:
    # If language is already selected, import the appropriate module
    if app_version == "english":
        import main as m
        m.main()
    elif app_version == "hebrew":
        import main_hebrew as m
        m.main()
else:

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

    # Language selection screen
    st.markdown('<div class="centered">', unsafe_allow_html=True)

    st.title("Weather App / אפליקציית מזג אוויר 🌤️")
    st.subheader("Please select your language / בחר את השפה שלך")

    st.markdown('<div class="btn-container">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("English"):
            st.query_params["app"] = "english"
            st.rerun()
    with col2:
        if st.button("עברית"):
            st.query_params["app"] = "hebrew"
            st.rerun()

    st.markdown('</div></div>', unsafe_allow_html=True)