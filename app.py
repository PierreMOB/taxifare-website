import streamlit as st
import datetime
import pandas as pd
import requests
import pydeck as pdk
import math

'''
# New-York Taxi Fare Prediction
'''

st.markdown('''
Please use our prediction model to estimate your taxi fare
''')

'''
## Here select your inputs :

### 1.date and time:
'''
col1, col2 = st.columns(2)

with col1:
    d = st.date_input("When is your trip ?", datetime.date(2019, 7, 6))

with col2:
    t = st.time_input('At what time?', datetime.time(8, 45))

st.write(f'Your trip is scheduled for {d} at {t}.')
date = f'{d} {t}'

'''
### 2. Locations :
'''

PLACES = {
    "JFK Airport": (40.6413, -73.7781),
    "LaGuardia Airport": (40.7769, -73.8740),
    "Times Square": (40.7580, -73.9855),
    "Empire State Building": (40.7484, -73.9857),
    "Central Park": (40.7829, -73.9654),
    "Brooklyn Bridge": (40.7061, -73.9969),
    "Grand Central": (40.7527, -73.9772),
    "Wall Street": (40.7060, -74.0088),
    "Bronx (Yankee Stadium)": (40.8296, -73.9262),
    "Queens (Flushing Meadows)": (40.7466, -73.8450),
    "Coney Island": (40.5755, -73.9707),
    "Brooklyn (Prospect Park)": (40.6602, -73.9690)}

col1, col2 = st.columns(2)
start = col1.selectbox("Départ", list(PLACES), index=0)
end = col2.selectbox("Arrivée", list(PLACES), index=2)

p_lat, p_lon = PLACES[start]
d_lat, d_lon = PLACES[end]

df = pd.DataFrame(
    {
        "lat": [p_lat, d_lat],
        "lon": [p_lon, d_lon],
        "color": ["#00C800", "#DC0000"],  # vert = pickup, rouge = dropoff
    }
)

st.map(df, color="color", size=80)
st.caption("🟢 Pickup · 🔴 Dropoff")

def manhattan_distance(start_lat: float, start_lon: float, end_lat: float, end_lon: float) -> float:
    """
    Calculate the Manhattan distance between in km two points on the earth (specified in decimal degrees).
    """
    earth_radius = 6371

    lat_1_rad, lon_1_rad = math.radians(start_lat), math.radians(start_lon)
    lat_2_rad, lon_2_rad = math.radians(end_lat), math.radians(end_lon)

    dlon_rad = lon_2_rad - lon_1_rad
    dlat_rad = lat_2_rad - lat_1_rad

    manhattan_rad = abs(dlon_rad) + abs(dlat_rad)
    manhattan_km = manhattan_rad * earth_radius

    return round(manhattan_km,2)

manhattan = manhattan_distance(p_lat, p_lon, d_lat, d_lon)
st.write('Estimated distance (km)', manhattan)


'''
### 3. Number of passengers
'''
passenger = st.number_input('Insert the passenger count', value=1, step=1)


'''
## Our Prediction
'''
url_mine = 'https://taxifare-401450345527.europe-west1.run.app/predict'
url = 'https://taxifare.lewagon.ai/predict'

params = {
        'pickup_datetime': date,
        'pickup_longitude': p_lon,
        'pickup_latitude': p_lat,
        'dropoff_longitude': d_lon,
        'dropoff_latitude': d_lat,
        'passenger_count': passenger
}

r = requests.get(url_mine, params=params)

st.success(f"Estimated fare : {r.json()['fare']:.2f} $")
