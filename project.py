import streamlit as st
import requests
from streamlit_js_eval import get_geolocation

# Function to get address from lat/lon (Google Maps API)
def get_address_google(lat, lon, api_key):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&key={api_key}"
    response = requests.get(url).json()
    if response["status"] == "OK":
        return response["results"][0]["formatted_address"]
    else:
        return "Address not found"

st.title("🏠🚗 Nearby Rental Finder (with Google Maps Live Location)")

st.write("Find rentals using **Live GPS Location** or by typing an **Area/City Name**")

option = st.radio("Choose Location Input Method:", ["📍 Use Live Location (GPS)", "⌨️ Enter Area/City Name"])

user_lat, user_lon, address = None, None, None

# Option 1: Live GPS Location
if option == "📍 Use Live Location (GPS)":
    loc = get_geolocation()   # fetch GPS from browser
    if loc:
        user_lat, user_lon = loc["coords"]["latitude"], loc["coords"]["longitude"]

        # ⚠️ Replace with your Google Maps API key
        GOOGLE_API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"
        address = get_address_google(user_lat, user_lon, GOOGLE_API_KEY)

        st.success(f"✅ Live Location: {address} (Lat: {user_lat}, Lon: {user_lon})")

# Option 2: Area/City Name
else:
    area = st.text_input("Enter Area or City Name (e.g., Hyderabad, Mumbai):")
    if area:
        GOOGLE_API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={area}&key={GOOGLE_API_KEY}"
        response = requests.get(url).json()
        if response["status"] == "OK":
            user_lat = response["results"][0]["geometry"]["location"]["lat"]
            user_lon = response["results"][0]["geometry"]["location"]["lng"]
            address = response["results"][0]["formatted_address"]
            st.success(f"✅ Location found: {address}")
        else:
            st.error("❌ Location not found. Try another area.")
