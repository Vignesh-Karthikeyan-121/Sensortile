import pandas as pd 
import csv
address="2023-04-15 04_44_18stile.csv"
#address_prefix=
#df = pd.read_csv("2023-04-15 04_44_18stile.csv")
#df.head()
#with open(address, 'r') as file:
#  csvreader = csv.reader(file)

#  for row in csvreader:
#    print(row[0])

import pandas as pd

# Define the expected number of columns in the CSV file
expected_columns = 11

# Initialize an empty list to store valid lines
lines = []

# Open the CSV file and read each line
with open(address) as f:
    for i, line in enumerate(f):
        # Skip the first row (header)
        if i == 0:
            continue
        # Split the line into fields
        fields = line.strip().split(',')
        # Check if the line has the expected number of fields
        if len(fields) == expected_columns:
            # Append the line to the list of valid lines
            lines.append(fields)
        elif len(fields) > expected_columns:
            # If there are too many fields, take the first n fields and skip the rest
            lines.append(fields[:expected_columns])
        else:
            # If there are too few fields, skip the line
            continue

# Convert the list of valid lines into a Pandas dataframe
df = pd.DataFrame(lines, columns=['time', 'accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z', 'mag_x', 'mag_y', 'mag_z', 'pressure'])
print(df)
# Convert the 'time' column to datetime format
df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S:%f')

# Calculate the refresh rate
refresh_rate = (df['time'].iloc[-1] - df['time'].iloc[0]) / (len(df) - 1)
print(refresh_rate)
print(f"The refresh rate is {1/refresh_rate.total_seconds()} Hertz")
# Calculate the consecutive time differences
time_diffs = df['time'].diff()

# Print the time differences
print(time_diffs)