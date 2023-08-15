import pandas as pd
import folium
from datetime import datetime, timedelta

time_format = "%Y-%m-%d %H:%M:%S"
# Read data from csv
address_prefix='C:/Users/mahak/Desktop/BTP-2/Working/rawdata/IIIT_trail1_sun/sensordata/gpsdata/'
filename="2023-04-16 08_50_34_182gps.csv"
#print(filename[:-4])
df = pd.read_csv(address_prefix+filename)
df = df[78:85]
print(df)
# Drop rows with NaN values
df.dropna(inplace=True)

# Initialize map centered on first data point
m = folium.Map(location=[df.iloc[0]['LAT'], df.iloc[0][' LONG']], zoom_start=15)


# Add markers to map for each data point
for index, row in df.iterrows():
    if not pd.isna(row['LAT']) and not pd.isna(row[' LONG']):
        # convert the time string to a datetime object
        time_obj = datetime.strptime(row[' ts'], time_format)

        # add 5 hours and 30 minutes to the datetime object
        new_time_obj = time_obj + timedelta(hours=5, minutes=30)

        # convert the datetime object back to a string
        new_time_string = datetime.strftime(new_time_obj, time_format)
        folium.Marker([row['LAT'], row[' LONG']],
                      popup=f"Time: {new_time_string}<br>Lat: {row['LAT']}<br>Long: {row[' LONG']}").add_to(m)

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

# Add an extra marker with a different color
#LAT=28.549244
#LONG=77.184658
#folium.Marker(LAT,LONG,
#              popup=f"Time: {df.iloc[-1][' ts']}<br>Lat: {df.iloc[-1]['LAT']}<br>Long: {df.iloc[-1][' LONG']}",
#              icon=folium.Icon(color='green')).add_to(m)

m.save(filename+"_plot"+".html")

#exit()
events = "C:/Users/mahak/Desktop/BTP-2/Working/rawdata/events.csv"
df = pd.read_csv(events)
for index, row in df.iterrows():
    if not pd.isna(row['LAT']) and not pd.isna(row['LONG']):
        folium.Marker([row['LAT'], row['LONG']],
                      icon=folium.Icon(color='green'),
                      popup=f"Label: {row['label']}").add_to(m)

# Save map as html file
m.save(filename+"_plot"+".html")
