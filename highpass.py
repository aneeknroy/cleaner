import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal


# Load PPG data from CSV file
ppg_data = pd.read_csv("ppg_Green/green2_AR.csv")
noisy_ppg_1 = ppg_data["PPG1"].values
noisy_ppg_2 = ppg_data["PPG2"].values

# Sampling frequency (assuming it's known)
sampling_freq = 100  # Hz

#--------------------------------------------------------------------------------------------------------------


# Define Filter Parameters
# HIGHPASS parameters

cutoff = 0.5                # Cutoff Frequency in Hz
nyquist_freq = 0.5 * sampling_freq   # Nyquist frequency in Hz
order = 4                   # Filter order

#--------------------------------------------------------------------------------------------------------------
b, a = signal.butter(order, cutoff / nyquist_freq, btype='high')

# Apply highpass filter to PPG signal
filtered_ppg_1 = signal.filtfilt(b, a, noisy_ppg_1)
filtered_ppg_2 = signal.filtfilt(b, a, noisy_ppg_2)

# Baseline Correction
baseline_ppg_1 = signal.medfilt(filtered_ppg_1, kernel_size=51)  # Apply a median filter as a baseline
corrected_ppg_1 = filtered_ppg_1 - baseline_ppg_1

# Smoothing
smoothed_ppg_1 = signal.savgol_filter(corrected_ppg_1, window_length=51, polyorder=3)

# Plot corrected and smoothed signals
# axs[1].plot(ppg_data["VAL"], smoothed_ppg_1, color='green', label='Corrected & Smoothed PPG1')
# axs[1].set_title('HIGHPASS Corrected & Smoothed - PPG1 Signal')
# axs[1].set_xlabel('Val (s)')
# axs[1].set_ylabel('Amplitude')
# axs[1].grid(True)




# Create a figure with subplots
fig, axs = plt.subplots(3, 1, figsize=(12, 10))

# PPG 1
# Plot original and filtered signals
axs[0].plot(ppg_data["VAL"], noisy_ppg_1, color='blue', label='Original PPG1')
axs[0].set_title('HIGHPASS Original - PPG1 Signal')
axs[0].set_xlabel('Val (s)')
axs[0].set_ylabel('Amplitude')
axs[0].grid(True)


axs[1].plot(ppg_data["VAL"], filtered_ppg_1, color='red',label='Filtered PPG1')
axs[1].set_xlabel('Val (s)')
axs[1].set_ylabel('Amplitude')
axs[1].set_title('HIGHPASS filtered - PPG1 Signal')
axs[1].grid(True)

axs[2].plot(ppg_data["VAL"], smoothed_ppg_1, color='green', label='Corrected & Smoothed PPG1')
axs[2].set_title('HIGHPASS Corrected & Smoothed - PPG1 Signal')
axs[2].set_xlabel('Val (s)')
axs[2].set_ylabel('Amplitude')
axs[2].grid(True)


# PPG 2
# Plot original and filtered signals
# axs[2].plot(ppg_data["VAL"], noisy_ppg_2, color='blue', label='Original PPG2')
# axs[2].set_title('HIGHPASS Original - PPG2 Signal')
# axs[2].set_xlabel('Val (s)')
# axs[2].set_ylabel('Amplitude')
# axs[2].grid(True)


# axs[3].plot(ppg_data["VAL"], filtered_ppg_2, color='green',label='Filtered PPG2')
# axs[3].set_xlabel('Val (s)')
# axs[3].set_ylabel('Amplitude')
# axs[3].set_title('HIGHPASS filtered - PPG Signal')
# axs[3].grid(True)


# Show the plot
plt.tight_layout()  # Adjust subplots to prevent overlap
plt.savefig('highpass_graph.png')  # Save as PNG format
plt.show()