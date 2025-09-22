import streamlit as st
import math
import requests

# Function to calculate distance (Haversine formula)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2)**2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2)
    c = 2 * math.asin(math.sqrt(a))
    return R * c

# Function to get address from lat/lon (reverse geocoding)
def get_address(lat, lon):
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
        response = requests.get(url, headers={"User-Agent": "streamlit-app"}).json()
        return response.get("display_name", "Address not found")
    except:
        return "Error fetching address"

# Sample rental data
rentals = [
    {"name": "Car Rental A", "lat": 17.385, "lon": 78.486, "type": "Car", "price": "₹1200/day"},
    {"name": "House Rental B", "lat": 17.400, "lon": 78.500, "type": "House", "price": "₹15,000/month"},
    {"name": "Car Rental C", "lat": 17.450, "lon": 78.480, "type": "Car", "price": "₹1500/day"},
    {"name": "House Rental D", "lat": 17.370, "lon": 78.490, "type": "House", "price": "₹12,000/month"}
]

st.title("🏠🚗 Nearby Rental Finder")

st.write("Find rental houses or cars by using **Live Location** or typing an **Area/City Name**")

option = st.radio("Choose Location Input Method:", ["📍 Use Live Location", "⌨️ Enter Area/City Name"])

user_lat, user_lon = None, None

# Option 1: Live Location
if option == "📍 Use Live Location":
    if st.button("Get My Live Location"):
        try:
            res = requests.get("https://ipinfo.io/json").json()
            loc = res["loc"].split(",")
            user_lat, user_lon = float(loc[0]), float(loc[1])
            address = get_address(user_lat, user_lon)
            st.success(f"✅ Location detected: {address}")
        except:
            st.error("Could not fetch live location automatically.")

# Option 2: Area/City Name
else:
    area = st.text_input("Enter Area or City Name (e.g., Hyderabad, Mumbai):")
    if area:
        try:
            url = f"https://nominatim.openstreetmap.org/search?format=json&q={area}"
            response = requests.get(url, headers={"User-Agent": "streamlit-app"}).json()
            if response:
                user_lat, user_lon = float(response[0]["lat"]), float(response[0]["lon"])
                st.success(f"✅ Location found: {response[0]['display_name']}")
            else:
                st.error("❌ Location not found. Try another area.")
        except:
            st.error("⚠️ Error fetching location data.")

# Search nearby rentals
if user_lat and user_lon:
    radius = st.slider("Search radius (km):", 1, 20, 5)
    nearby = []
    for r in rentals:
        dist = haversine(user_lat, user_lon, r["lat"], r["lon"])
        if dist <= radius:
            nearby.append((r, dist))

    if nearby:
        st.subheader("🔎 Nearby Rentals:")
        for r, dist in nearby:
            st.markdown(f"""
            **{r['name']}**  
            📍 Type: {r['type']}  
            💰 Price: {r['price']}  
            📏 Distance: {dist:.2f} km
            """)
    else:
        st.warning("No rentals found nearby. Try increasing the radius.")
