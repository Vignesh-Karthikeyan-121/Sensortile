import numpy as np
import matplotlib.pyplot as plt
from pykalman import KalmanFilter
import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Load the GPS and IMU data from the CSV files
gps_data = pd.read_csv('gps_data.csv')
imu_data = pd.read_csv('imu_data.csv')

# Define the state vector
# In this example, we assume a 3D state vector [x, y, theta]
# where x and y are the position coordinates and theta is the heading angle
state_vector = np.array([0, 0, 0])

# Define the measurement matrix for GPS and IMU
# In this example, we assume that the GPS measurement is [x, y] and the IMU measurement is [theta]
gps_meas_matrix = np.array([[1, 0, 0], [0, 1, 0]])
imu_meas_matrix = np.array([[0, 0, 1]])

# Define the covariance matrices for the GPS and IMU measurements
gps_meas_covariance = np.array([[0.1, 0], [0, 0.1]])
imu_meas_covariance = np.array([[0.1]])

# Define the covariance matrix for the process noise
# This represents the uncertainty in the model prediction
process_noise_covariance = np.array([[0.1, 0, 0], [0, 0.1, 0], [0, 0, 0.1]])

# Define the initial state covariance matrix
# This represents the uncertainty in the initial state estimate
initial_state_covariance = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

# Create the Kalman filter object
kf = KalmanFilter(transition_matrices=np.eye(3),
                  observation_matrices=np.vstack((gps_meas_matrix, imu_meas_matrix)),
                  observation_covariance=np.diag(np.hstack((gps_meas_covariance.ravel(), imu_meas_covariance.ravel()))),
                  transition_covariance=process_noise_covariance,
                  initial_state_mean=state_vector,
                  initial_state_covariance=initial_state_covariance)

# Run the Kalman filter on the GPS and IMU data to estimate the position and orientation
# Note that we assume the GPS and IMU data are synchronized and sampled at the same rate
estimates, _ = kf.filter(np.hstack((gps_data[['x', 'y']].values, imu_data[['theta']].values)))

# Define a function to convert the orientation angle from radians to degrees
def rad2deg(rad):
    return rad * 180 / np.pi

# Get the estimated position and orientation from the EKF estimates
# Note that the orientation angle is in radians and needs to be converted to degrees
est_pos = estimates[:, :2]
est_orient = rad2deg(estimates[:, 2])

# Plot the GPS and estimated paths
plt.figure(figsize=(10, 8))
plt.plot(gps_data['x'], gps_data['y'], label='GPS path')
plt.plot(est_pos[:, 0], est_pos[:, 1], label='Estimated path')
plt.legend()
plt.xlabel('X position (m)')
plt.ylabel('Y position (m)')
plt.title('Vehicle path')
plt.show()

# Print the estimated position and orientation at the last time step
print("Estimated position: ", est_pos[-1])
print("Estimated orientation: ", est_orient[-1])

# Define the map projection
crs = ccrs.PlateCarree()

# Create a figure and axis for the map
fig = plt.figure(figsize=(12, 10))
ax = fig.add_subplot(1, 1, 1, projection=crs)

# Set the map extent to cover the GPS path
ax.set_extent([gps_data['longitude'].min()-0.01, gps_data['longitude'].max()+0.01,
               gps_data['latitude'].min()-0.01, gps_data['latitude'].max()+0.01],
              crs=cr
