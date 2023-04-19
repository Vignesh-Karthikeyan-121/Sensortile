import pandas as pd
import folium

# Read data from csv
address_prefix='C:/Users/mahak/Desktop/BTP-2/Working/rawdata/IIIT_trail1_sun/sensordata/gpsdata/'
filename="2023-04-16 08_50_34_182gps.csv"
#print(filename[:-4])
df = pd.read_csv(address_prefix+filename)
df = df[0:2]
print(df)
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

# Save map as html file
m.save(filename+"_plot"+".html")
