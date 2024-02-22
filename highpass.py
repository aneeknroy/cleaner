import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal


# Load ECG data from CSV file
ecg_data = pd.read_csv("ppg_Green/green1_AR.csv")
noisy_ecg = ecg_data["PPG1"].values

# Sampling frequency (assuming it's known)
sampling_freq = 100  # Hz

#--------------------------------------------------------------------------------------------------------------


# Define Filter Parameters
# HIGHPASS parameters

cutoff = 0.5                # Cutoff Frequency in Hz
nyquist_freq = 0.5 * sampling_freq   # Nyquist frequency in Hz
order = 2                   # Filter order

# Design highpass Filter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal


# Load ECG data from CSV file
ecg_data = pd.read_csv("ppg_GREEN/green2_AR.csv")
noisy_ecg = ecg_data["PPG1"].values

# Sampling frequency (assuming it's known)
sampling_freq = 100  # Hz

#--------------------------------------------------------------------------------------------------------------


# Define Filter Parameters
# BANDPASS parameters

lowcut = 0.5                # Lower Cutoff Frequency in Hz
highcut = 40.0              # Higher Cutoff Frequency in Hz
nyquist_freq = 0.5 * 1000   # Nyquist frequency in Hz
order = 2                   # Filter order

# Design Bandpass Filter
b, a = signal.butter(order, [lowcut / nyquist_freq, highcut / nyquist_freq], btype='band')

# Apply BandPass Filter to noisy ECG Signal
filtered_ecg = signal.filtfilt(b, a, noisy_ecg)

# Create a figure with subplots
fig, axs = plt.subplots(2, 1, figsize=(10, 8))

# Plot original and filtered signals
axs[0].plot(ecg_data["VAL"], noisy_ecg, color='blue', label='Original PPG')
axs[0].set_title('HIGHPASS Original - PPG Signal')
axs[0].set_xlabel('Val (s)')
axs[0].set_ylabel('Amplitude')
axs[0].grid(True)


axs[1].plot(ecg_data["VAL"], filtered_ecg, color='red',label='Filtered PPG')
axs[1].set_xlabel('Val (s)')
axs[1].set_ylabel('Amplitude')
axs[1].set_title('HIGHPASS filtered - PPG Signal')
axs[1].grid(True)

# Show the plot
plt.tight_layout()  # Adjust subplots to prevent overlap
plt.show()