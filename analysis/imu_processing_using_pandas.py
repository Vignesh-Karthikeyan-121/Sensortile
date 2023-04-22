import pandas as pd
import matplotlib.pyplot as plt
import math
import csv

#data = "C:/ST/Analysis/sensordata/sensortile/2023-04-16 08_48_02stile.csv"
data ="C:/Users/mahak/Desktop/BTP-2/Working/rawdata/IIIT_trail1_sun/sensordata/sensortile/2023-04-16 08_48_02stile.csv"
import pandas as pd

# Define the expected number of columns in the CSV file
expected_columns = 11

# Initialize an empty list to store valid lines
lines = []

# Open the CSV file and read each line
with open(data) as f:
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

# Read the CSV file using pandas
data = pd.DataFrame(lines, columns=['time', 'accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z', 'mag_x', 'mag_y', 'mag_z', 'pressure'])
data = data[71229:72082]

# num_columns = 12 # There should be 12 columns in the df.

# mask = 12 # create a mask/limit for the number of rows allowed.

# apply the mask to the dataframe to remove rows with length other than 12
# data = data.loc[mask]

# data = data[data.apply(lambda row: len(row.str.split(','))) == 12]
# print(type(data))

# Extract the sensor data
acc_x_values = pd.to_numeric(data['accel_x'])
#print(type(acc_x_values))
acc_y_values = pd.to_numeric(data['accel_y'])
acc_z_values = pd.to_numeric(data['accel_z'])
gyro_x_values = pd.to_numeric(data['gyro_x'])
gyro_y_values = pd.to_numeric(data['gyro_y'])
gyro_z_values = pd.to_numeric(data['gyro_z'])
mag_x_values = pd.to_numeric(data['mag_x'])
mag_y_values = pd.to_numeric(data['mag_y'])
mag_z_values = pd.to_numeric(data['mag_z'])
baro = pd.to_numeric(data['pressure'])

# Calculate the net acceleration
acc_net = [math.sqrt(acc_z**2 + acc_x**2 + acc_y**2) for acc_x, acc_y, acc_z in zip(acc_x_values, acc_y_values, acc_z_values)]

# Calculate the average values
acc_x_avg = acc_x_values.mean()
acc_y_avg = acc_y_values.mean()
acc_z_avg = acc_z_values.mean()
gyro_x_avg = gyro_x_values.mean()
gyro_y_avg = gyro_y_values.mean()
gyro_z_avg = gyro_z_values.mean()


# Print the results
print(f"Average Accelerometer X: {acc_x_avg}")
print(f"Average Accelerometer Y: {acc_y_avg}")
print(f"Average Accelerometer Z: {acc_z_avg}")
print(f"Average Gyroscope X: {gyro_x_avg}")
print(f"Average Gyroscope Y: {gyro_y_avg}")
print(f"Average Gyroscope Z: {gyro_z_avg}")

# Create a time axis for the data
time_axis = pd.Series(range(len(acc_x_values)))
#time_axis = range(len(acc_x_values))

# convert data axes to pandas series
acc_x_values = pd.Series(acc_x_values)
acc_y_values = pd.Series(acc_y_values)
acc_z_values = pd.Series(acc_z_values)
acc_net = pd.Series(acc_net)

gyro_x_values = pd.Series(gyro_x_values)
gyro_y_values = pd.Series(gyro_y_values)
gyro_z_values = pd.Series(gyro_z_values)
mag_x_values = pd.Series(mag_x_values)
mag_y_values = pd.Series(mag_y_values)
mag_z_values = pd.Series(mag_z_values)
acc_x_values = pd.Series(acc_x_values)

# adding extra simple hueristic processing on individual series

acc_net_sma = acc_net.rolling(window=30).mean()

# Plot the accelerometer data

plt.figure()
#plt.plot(time_axis.values, acc_x_values.values, label='Accelerometer X')
#plt.plot(time_axis.values, acc_y_values.values, label='Accelerometer Y')

#plt.plot(time_axis.values, acc_z_values.values, label='Accelerometer Z')
#plt.plot(time_axis.values, acc_net.values, label='Accelerometer NET')
plt.plot(time_axis.values, acc_net_sma.values, label='Accelerometer NET SMA')
plt.xlabel('data points')
plt.ylabel('Acceleration')
plt.title('Accelerometer Data')
plt.legend()

# Plot the gyroscope data
plt.figure()
plt.plot(time_axis.values, gyro_x_values.values, label='Gyroscope X')
plt.plot(time_axis.values, gyro_y_values.values, label='Gyroscope Y')
plt.plot(time_axis.values, gyro_z_values.values, label='Gyroscope Z')
plt.xlabel('data points')
plt.ylabel('Gyroscope')
plt.title('Gyroscope Data')
plt.legend()

# Plot the magnetometer data
plt.figure()
plt.plot(time_axis.values, mag_x_values.values, label='COMP X')
plt.plot(time_axis.values, mag_y_values.values, label='COMP Y')
plt.plot(time_axis.values, mag_z_values.values, label='COMP Z')
plt.xlabel('data points')
plt.ylabel('Magnetometer')
plt.title('Magnetometer Data')
plt.legend()

# Plot the Barometer data
plt.figure()
plt.plot(time_axis.values, baro.values, label='Pressure')
plt.xlabel('data points')
plt.ylabel('Pressure (KPa)')
plt.title('Pressure Data')
plt.legend()

# Show the plots
plt.show()
