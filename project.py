import streamlit as st
import math

# Function to calculate distance (Haversine formula)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2)**2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2)
    c = 2 * math.asin(math.sqrt(a))
    return R * c

# Sample rental data
rentals = [
    {"name": "Car Rental A", "lat": 17.385, "lon": 78.486, "type": "Car", "price": "₹1200/day"},
    {"name": "House Rental B", "lat": 17.400, "lon": 78.500, "type": "House", "price": "₹15,000/month"},
    {"name": "Car Rental C", "lat": 17.450, "lon": 78.480, "type": "Car", "price": "₹1500/day"},
    {"name": "House Rental D", "lat": 17.370, "lon": 78.490, "type": "House", "price": "₹12,000/month"}
]

# Streamlit UI
st.title("🏠🚗 Nearby Rental Service Finder")

st.write("Find rental houses or cars near your location!")

# User inputs
lat = st.number_input("Enter your latitude:", value=17.392, format="%.6f")
lon = st.number_input("Enter your longitude:", value=78.487, format="%.6f")
radius = st.slider("Search radius (km):", 1, 20, 5)

# Filter rentals
nearby = []
for r in rentals:
    dist = haversine(lat, lon, r["lat"], r["lon"])
    if dist <= radius:
        nearby.append((r, dist))

# Show results
if nearby:
    st.subheader("🔎 Nearby Rentals Found:")
    for r, dist in nearby:
        st.markdown(f"""
        **{r['name']}**  
        📍 Type: {r['type']}  
        💰 Price: {r['price']}  
        📏 Distance: {dist:.2f} km
        """)
else:
    st.warning("No rentals found in this area. Try increasing the radius.")

