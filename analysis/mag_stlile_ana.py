import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the magnetometer data from a CSV file
data = pd.read_csv('magnetometer_data.csv')

# Pre-process the data
# Apply a low-pass filter to remove high-frequency noise
from scipy.signal import butter, filtfilt

def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y

cutoff_frequency = 5 # Hz
sampling_frequency = 100 # Hz
order = 2

# Apply filtering to each dimension of the data
filtered_data = np.zeros_like(data)
for i in range(3):
    filtered_data[:,i] = butter_lowpass_filter(data.iloc[:,i], cutoff_frequency, sampling_frequency, order)

# Analyze the data
# Compute the norm of the magnetic field to detect sudden changes
norm = np.linalg.norm(filtered_data, axis=1)

# Compute the gradient of the norm to detect sudden changes in the magnetic field
gradient = np.gradient(norm)

# Apply thresholding to detect events
threshold = 0.05 # Set a threshold to detect significant changes
events = np.where(np.abs(gradient) > threshold)[0]

# Plot the results
fig, ax = plt.subplots()
ax.plot(norm, label='Norm of filtered data')
ax.plot(gradient, label='Gradient')
ax.axhline(y=threshold, color='r', linestyle='--', label='Threshold')
ax.scatter(events, gradient[events], color='r', label='Events')
ax.legend()
plt.show()

# Interpret the results
# Compute the duration and magnitude of the events
event_durations = np.diff(events)
event_magnitudes = gradient[events[:-1]]

print('Detected %d events:' % len(event_durations))
for i in range(len(event_durations)):
    print('Event %d: duration = %.2f s, magnitude = %.2f' % (i+1, event_durations[i]/sampling_frequency, event_magnitudes[i]))