import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
import csv
from io import StringIO

def process_ppg_data(csv_file):
    ppg_data = pd.read_csv(csv_file)

    ppgOne = ppg_data["PPG1"].values
    ppgTwo = ppg_data["PPG2"].values

    gainOne = ppg_data["GAIN1"].values[0]
    gainTwo = ppg_data["GAIN2"].values[0]

    dacOne = ppg_data["DAC1"].values[0]
    dacTwo = ppg_data["DAC2"].values[0]

    if dacOne == 0: 
        dacOne = 1

    if dacTwo == 0: 
        dacTwo = 1

    raw1_data = []
    raw2_data = []

    for i in range(len(ppgOne)):
        raw1 = ppgOne[i] / (gainOne + (dacOne / 5) * (2 ** 16))
        raw2 = ppgTwo[i] / (gainTwo + (dacTwo / 5) * (2 ** 16))
        raw1_data.append(raw1)
        raw2_data.append(raw2)

    return ppgOne, ppgTwo, raw1_data, raw2_data

# Now, define a function to apply bandpass filtering to the PPG data
def bandpass_filter(ppg_data):
    sampling_freq = 100  # Hz
    lowcut = 0.5                         # Lower Cutoff Frequency in Hz
    highcut = 35.0                       # Higher Cutoff Frequency in Hz
    nyquist_freq = 0.5 * sampling_freq   # Nyquist frequency in Hz
    order = 4                            # Filter order

    b, a = signal.butter(order, [lowcut / nyquist_freq, highcut / nyquist_freq], btype='band')

    filtered_ppg = signal.filtfilt(b, a, ppg_data)

    return filtered_ppg

# Now, modify your script to call these functions
def process_and_plot_data(file):
    ppgOne, ppgTwo, raw1_data, raw2_data = process_ppg_data(file)

    filtered_ppg1 = bandpass_filter(ppgOne)
    filtered_ppg2 = bandpass_filter(ppgTwo)

    plt.figure(figsize=(12, 8))

    plt.subplot(2, 1, 1)
    plt.plot(raw1_data, label='Raw PPG1')
    plt.plot(filtered_ppg1, label='Filtered PPG1')
    plt.legend()
    plt.title('PPG1 Data')

    plt.subplot(2, 1, 2)
    plt.plot(raw2_data, label='Raw PPG2')
    plt.plot(filtered_ppg2, label='Filtered PPG2')
    plt.legend()
    plt.title('PPG2 Data')

    plt.tight_layout()
    plt.show()

# Now you can call process_and_plot_data function from your PyQt application.
