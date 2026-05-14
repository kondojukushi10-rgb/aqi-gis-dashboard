# import streamlit as st

# st.title("GIS Streamlit Practice")

# name = st.text_input("Write your name")

# if name:
#     st.success(f"Welcome {name}!")

# age = st.slider("Select Age", 1, 100, 25)

# st.write("Your age is:", age)

# import streamlit as st
# import pandas as pd
# import plotly.express as px

# st.title("Pandas + Plotly Practice")

# # Sample DataFrame
# df = pd.DataFrame({
#     "City": ["Hyderabad", "Delhi", "Mumbai"],
#     "Population": [10, 32, 20]
# })

# st.dataframe(df)

# # Plotly Chart
# fig = px.bar(df, x="City", y="Population")

# st.plotly_chart(fig)

import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

# -----------------------------
# CONFIGURATION
# -----------------------------

API_TOKEN = st.secrets["API_KEY"]

# -----------------------------
# STREAMLIT UI
# -----------------------------

st.title("🌍 Live Air Quality GIS Dashboard")

city = st.text_input(
    "Enter City Name",
    value="Hyderabad"
)

# -----------------------------
# API REQUEST
# -----------------------------

if st.button("Get Air Quality"):

    url = f"https://api.waqi.info/feed/{city}/?token={API_TOKEN}"

    response = requests.get(url)

    data = response.json()

    # -----------------------------
    # CHECK API STATUS
    # -----------------------------

    if data["status"] == "ok":

        aqi = data["data"]["aqi"]

        lat = data["data"]["city"]["geo"][0]
        lon = data["data"]["city"]["geo"][1]

        station = data["data"]["city"]["name"]

        # -----------------------------
        # DISPLAY AQI INFO
        # -----------------------------

        st.subheader(f"📍 Station: {station}")

        st.metric("Air Quality Index (AQI)", aqi)

        # AQI Categories
        if aqi <= 50:
            st.success("Good Air Quality")
            marker_color = "green"

        elif aqi <= 100:
            st.warning("Moderate Air Quality")
            marker_color = "orange"

        else:
            st.error("Poor Air Quality")
            marker_color = "red"

        # -----------------------------
        # CREATE GIS MAP
        # -----------------------------

        m = folium.Map(
            location=[lat, lon],
            zoom_start=10
        )

        folium.Marker(
            [lat, lon],
            popup=f"AQI: {aqi}",
            tooltip=station,
            icon=folium.Icon(color=marker_color)
        ).add_to(m)

        # Display map
        st_folium(m, width=700, height=500)

    else:
        st.error("City not found or API issue.")