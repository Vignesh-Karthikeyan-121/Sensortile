import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run_spectrogram(imu_data, sample_rate, window_size, overlap):
    # Convert window size and overlap from seconds to number of samples
    window_size_samples = int(window_size * sample_rate)
    overlap_samples = int(window_size_samples * overlap)

    # Apply windowing function
    window = np.hanning(window_size_samples).astype(imu_data.dtype)  # Convert window to the same data type as imu_data
    window = np.resize(window, imu_data.shape)  # Resize the window to match the shape of imu_data
    windowed_data = np.multiply(imu_data, window)
    
    # Calculate the number of windows
    num_windows = int((len(imu_data) - window_size_samples) / overlap_samples) + 1

    # Initialize the spectrogram matrix
    spectrogram = np.zeros((window_size_samples // 2 + 1, num_windows))

    # Calculate the spectrogram using FFT
    for i in range(num_windows):
        start_index = i * overlap_samples
        end_index = start_index + window_size_samples
        windowed_segment = windowed_data[start_index:end_index]
        spectrum = np.abs(np.fft.fft(windowed_segment)[:window_size_samples // 2 + 1])
        spectrogram[:, i] = spectrum

    # Convert the spectrogram to decibels (dB) for better visualization
    spectrogram = 20 * np.log10(spectrogram)

    # Create the time and frequency axes for the spectrogram
    time_axis = np.arange(window_size_samples / 2 + 1) / sample_rate
    frequency_axis = np.fft.fftfreq(window_size_samples, 1 / sample_rate)[:window_size_samples // 2 + 1]

    # Plot the spectrogram
    plt.figure(figsize=(10, 6))
    plt.imshow(spectrogram, aspect='auto', origin='lower', extent=[0, len(imu_data) / sample_rate, frequency_axis[0], frequency_axis[-1]])
    plt.colorbar(label='Magnitude (dB)')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.title('IMU Spectrogram')
    plt.show()

# Example usage
data = "C:/Users/mahak/Desktop/BTP-2/Working/rawdata/IIIT_trail1_sun/sensordata/sensortile/2023-04-16 08_48_02stile.csv"  # Replace with the path to your IMU data CSV file
window_size = 1  # Size of the window in seconds
overlap = 0.5  # Overlap between consecutive windows

# Load IMU data from CSV using pandas

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
imu_df = pd.DataFrame(lines, columns=['time', 'accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z', 'mag_x', 'mag_y', 'mag_z', 'pressure'])
imu_df['Timestamp'] = pd.to_datetime(imu_df['time'], format='%Y-%m-%d %H:%M:%S:%f')

imu_data = imu_df['accel_x'].values  # Replace 'IMU Reading' with the column name containing the IMU data

#sample_rate = imu_df.shape[0] / (imu_df['Timestamp'].iloc[-1] - imu_df['Timestamp'].iloc[0])
# Calculate the sample rate based on the time difference in seconds
time_diff = imu_df['Timestamp'].diff().mean().total_seconds()
sample_rate = int(1 / time_diff)


run_spectrogram(imu_data, sample_rate, window_size, overlap)
