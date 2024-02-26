import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal


# Load ECG data from CSV file
ecg_data = pd.read_csv("ppg_RED/red5_AR.csv")
noisy_ecg_1 = ecg_data["PPG1"].values
noisy_ecg_2 = ecg_data["PPG2"].values


# Sampling frequency (assuming it's known)
sampling_freq = 100  # Hz

#--------------------------------------------------------------------------------------------------------------


# Define Filter Parameters
# BANDPASS parameters

lowcut = 0.5                         # Lower Cutoff Frequency in Hz
highcut = 40.0                       # Higher Cutoff Frequency in Hz
nyquist_freq = 0.5 * sampling_freq   # Nyquist frequency in Hz
order = 4                            # Filter order

# Design Bandpass Filter
b, a = signal.butter(order, [lowcut / nyquist_freq, highcut / nyquist_freq], btype='band')

# Apply BandPass Filter to noisy ECG Signal
filtered_ecg_1 = signal.filtfilt(b, a, noisy_ecg_1)
filtered_ecg_2 = signal.filtfilt(b, a, noisy_ecg_2)

# Create a figure with subplots
fig, axs = plt.subplots(4, 1, figsize=(12, 10))

# PPG 1
# Plot original and filtered signals
axs[0].plot(ecg_data["VAL"], noisy_ecg_1, color='blue', label='Original PPG1')
axs[0].set_title('BANDPASS Original - PPG1 Signal')
axs[0].set_xlabel('Val (s)')
axs[0].set_ylabel('Amplitude')
axs[0].grid(True)


axs[1].plot(ecg_data["VAL"], filtered_ecg_1, color='green', label='Filtered PPG1')
axs[1].set_xlabel('Val (s)')
axs[1].set_ylabel('Amplitude')
axs[1].set_title('BANDPASS filtered - PPG1 Signal')
axs[1].grid(True)

# PPG 2
# Plot original and filtered signals
axs[2].plot(ecg_data["VAL"], noisy_ecg_2, color='blue', label='Original PPG2')
axs[2].set_title('HIGHPASS Original - PPG2 Signal')
axs[2].set_xlabel('Val (s)')
axs[2].set_ylabel('Amplitude')
axs[2].grid(True)


axs[3].plot(ecg_data["VAL"], filtered_ecg_2, color='red',label='Filtered PPG2')
axs[3].set_xlabel('Val (s)')
axs[3].set_ylabel('Amplitude')
axs[3].set_title('HIGHPASS filtered - PPG Signal')
axs[3].grid(True)

# Show the plot
plt.tight_layout()  # Adjust subplots to prevent overlap
plt.savefig('bandpass_graph.png')  # Save as PNG format
plt.show()