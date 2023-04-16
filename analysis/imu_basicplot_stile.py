import csv
import matplotlib.pyplot as plt
import math
# Open the CSV file and read the data
with open('myfile15_03_2023_010151.txt', 'r') as csvfile:
    imu_data = csv.reader(csvfile)
    #print(type(imu_data))

    # Skip the header row
    next(imu_data)

    # Initialize variables for calculating the average values
    acc_x_total = 0
    acc_y_total = 0
    acc_z_total = 0
    gyro_x_total = 0
    gyro_y_total = 0
    gyro_z_total = 0
    count = 0

    # Initialize lists for each sensor value
    acc_x_values = []
    acc_y_values = []
    acc_z_values = []
    acc_net = []
    gyro_x_values = []
    gyro_y_values = []
    gyro_z_values = []
    gyro_net = []
    mag_x_values = []
    mag_y_values = []
    mag_z_values = []
    mag_net = []
    baro = []

    # Iterate through each row of data
    for row in imu_data:
        #print(type(row))
        # Convert the values to float
        acc_x = float(row[1])
        acc_y = float(row[2])
        acc_z = float(row[3])
        gyro_x = float(row[4])
        gyro_y = float(row[5])
        gyro_z = float(row[6])
        mag_x = float(row[7])
        mag_y = float(row[8])
        mag_z = float(row[9])
        baro_val = float(row[10])
        print(type(acc_x))

        acc_x_values.append(acc_x)
        acc_y_values.append(acc_y)
        acc_z_values.append(acc_z)
        acc_net.append(math.sqrt(acc_z**2+acc_x**2+acc_y**2))
        gyro_x_values.append(gyro_x)
        gyro_y_values.append(gyro_y)
        gyro_z_values.append(gyro_z)
        mag_x_values.append(mag_x)
        mag_y_values.append(mag_y)
        mag_z_values.append(mag_z)
        baro.append(baro_val)
        

        # Add the values to the running totals
        acc_x_total += acc_x
        acc_y_total += acc_y
        acc_z_total += acc_z
        gyro_x_total += gyro_x
        gyro_y_total += gyro_y
        gyro_z_total += gyro_z
        count += 1

    # Calculate the average values
    acc_x_avg = acc_x_total / count
    acc_y_avg = acc_y_total / count
    acc_z_avg = acc_z_total / count
    gyro_x_avg = gyro_x_total / count
    gyro_y_avg = gyro_y_total / count
    gyro_z_avg = gyro_z_total / count

    # Print the results
    print(f"Average Accelerometer X: {acc_x_avg}")
    print(f"Average Accelerometer Y: {acc_y_avg}")
    print(f"Average Accelerometer Z: {acc_z_avg}")
    print(f"Average Gyroscope X: {gyro_x_avg}")
    print(f"Average Gyroscope Y: {gyro_y_avg}")
    print(f"Average Gyroscope Z: {gyro_z_avg}")

    # Create a time axis for the data
time_axis = [i for i in range(len(acc_x_values))]

# Plot the accelerometer data
plt.figure()
plt.plot(time_axis, acc_x_values, label='Accelerometer X')
plt.plot(time_axis, acc_y_values, label='Accelerometer Y')
plt.plot(time_axis, acc_z_values, label='Accelerometer Z')
plt.plot(time_axis, acc_net, label='Accelerometer NET')
plt.xlabel('data points')
plt.ylabel('Acceleration')
plt.title('Accelerometer Data')
plt.legend()

# Plot the gyroscope data
plt.figure()
plt.plot(time_axis, gyro_x_values, label='Gyroscope X')
plt.plot(time_axis, gyro_y_values, label='Gyroscope Y')
plt.plot(time_axis, gyro_z_values, label='Gyroscope Z')
plt.xlabel('data points')
plt.ylabel('Gyroscope')
plt.title('Gyroscope Data')
plt.legend()


# Plot the magnetometer data
plt.figure()
plt.plot(time_axis, mag_x_values, label='COMP X')
plt.plot(time_axis, mag_y_values, label='COMP Y')
plt.plot(time_axis, mag_z_values, label='COMP Z')
plt.xlabel('data points')
plt.ylabel('Magnetometer')
plt.title('Magnetometer Data')
plt.legend()

# Plot the Barometer data
plt.figure()
plt.plot(time_axis, baro, label='Pressure')
plt.xlabel('data points')
plt.ylabel('Pressure (KPa)')
plt.title('Pressure Data')
plt.legend()

# Show the plots
plt.show()
##############################

