import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal

def process_ppg(csv_file):
    # Load ECG data from CSV file
    ppg_data = pd.read_csv(csv_file)
    noisy_ppg_1 = ppg_data["PPG1"].values

    # Sampling frequency (assuming it's known)
    sampling_freq = 100  # Hz

    # Define Filter Parametersff
    # BANDPASS parameters
    lowcut = 0.5                         # Lower Cutoff Frequency in Hz
    highcut = 35.0                       # Higher Cutoff Frequency in Hz
    nyquist_freq = 0.5 * sampling_freq   # Nyquist frequency in Hz
    order = 4                            # Filter order

    # Design Bandpass Filter
    b, a = signal.butter(order, [lowcut / nyquist_freq, highcut / nyquist_freq], btype='band')

    # Apply BandPass Filter to noisy ECG Signal
    filtered_ppg_1 = signal.filtfilt(b, a, noisy_ppg_1)

    # Baseline Correction
    baseline_ppg_1 = signal.medfilt(filtered_ppg_1, kernel_size=51)  # Apply a median filter as a baseline
    corrected_ppg_1 = filtered_ppg_1 - baseline_ppg_1

    # Smoothing
    smoothed_ppg_1 = signal.savgol_filter(corrected_ppg_1, window_length=51, polyorder=3)

    # Plotting
    fig, axs = plt.subplots(3, 1, figsize=(12, 10))

    # PPG 1
    # Plot original and filtered signals
    axs[0].plot(ppg_data["VAL"], noisy_ppg_1, color='blue', label='Original PPG1')
    axs[0].set_title('BANDPASS Original - PPG1 Signal')
    axs[0].set_xlabel('Val (s)')
    axs[0].set_ylabel('Amplitude')
    axs[0].grid(True)

    axs[1].plot(ppg_data["VAL"], filtered_ppg_1, color='green', label='Filtered PPG1')
    axs[1].set_xlabel('Val (s)')
    axs[1].set_ylabel('Amplitude')
    axs[1].set_title('BANDPASS filtered - PPG1 Signal')
    axs[1].grid(True)

    axs[2].plot(ppg_data["VAL"], smoothed_ppg_1, color='purple', label='Corrected & Smoothed PPG1')
    axs[2].set_title('BANDPASS Corrected & Smoothed - PPG1 Signal')
    axs[2].set_xlabel('Val (s)')
    axs[2].set_ylabel('Amplitude')
    axs[2].grid(True)

    plt.tight_layout()  # Adjust subplots to prevent overlap
    plt.savefig('bandpass_graph.png')  # Save as PNG format
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <csv_file>")
        sys.exit(1)
    csv_file = sys.argv[1]
    process_ppg(csv_file)
