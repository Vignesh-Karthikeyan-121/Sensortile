import pandas as pd
import folium
from folium.plugins import PolyLineTextPath

# Read data from csv
df = pd.read_csv('C:/Users/mahak/Desktop/BTP-2/Working/rawdata/until_saturday_around_campus_data/Pollution_Sensing_IOT/sensordata/gpsdata/2023-04-15 17_42_20_187gps.csv')

# Drop rows with NaN values
df.dropna(inplace=True)

# Initialize map centered on first data point
m = folium.Map(location=[df.iloc[0]['LAT'], df.iloc[0][' LONG']], zoom_start=15)

# Add markers to map for each data point
for index, row in df.iterrows():
    if not pd.isna(row['LAT']) and not pd.isna(row[' LONG']):
        folium.Marker([row['LAT'], row[' LONG']],
                      popup=f"Time: {row[' ts']}<br>Lat: {row['LAT']}<br>Long: {row[' LONG']}").add_to(m)

# Extract timestamps and lat-long data as separate lists
time_stamps = df[' ts'].tolist()
lat_long = df[['LAT', ' LONG']].values.tolist()

# Remove any missing values from the lists
lat_long = [x for x in lat_long if all(x)]
time_stamps = [x for x in time_stamps if pd.notna(x)]

# Add path to map
path = []
for i in range(len(lat_long)):
    path.append(lat_long[i])
    folium.PolyLine(locations=path, color='red').add_to(m)
    
    if i > 0:
        PolyLineTextPath(
            polyline=path[-2:],
            line_color='red',
            line_opacity=0.7,
            line_weight=5,
            repeat=True,
            offset=6,
            text="▶",
            align='center',
        ).add_to(m)

# Save map as html file
m.save("gps_map.html")
