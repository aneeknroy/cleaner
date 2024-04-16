import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
import csv

import os
from glob import glob
import matplotlib.pyplot as plt
from io import StringIO


# TODO
# 1. change original PPG before being edited to go through bandpass/highpass
# 2. 

def process_and_add_columns(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()

    dac_values = []
    gain_settings = []

    for line in lines:
        if 'DAC Value' in line:
            # Example line: 'DAC Value: 20 Voltage: 0.10V\n'
            dac_value = int(line.split(':')[1].split(' ')[1])
            dac_values.append(dac_value)
        elif 'PGA Gain Setting' in line:
            # Example line: 'PGA Gain Setting: 3\n'
            gain_setting = int(line.split(':')[1].strip())
            gain_settings.append(gain_setting)

    data_start_index = lines.index('Sample Count,PPG 1,PPG 2,BioZ 1,BioZ 2\n')
    data_lines = lines[data_start_index:]

    data_str = ''.join(data_lines)
    data_df = pd.read_csv(StringIO(data_str))

    data_df['DAC1'] = dac_values[0]  
    data_df['DAC2'] = dac_values[1] 
    data_df['GAIN1'] = gain_settings[0]  # Assuming first Gain setting is GAIN1
    data_df['GAIN2'] = gain_settings[1]  # Assuming second Gain setting is GAIN2

    return data_df

##df = process_and_add_columns('sdData_IAN/2023-10-26-12-31-26.937.csv')
#print(df.head())


file = "realPPG/SB_3_gainCheck_GREEN.csv"
ppg_data = pd.read_csv(file)

ppgOne = ppg_data["PPG1"].values
ppgTwo = ppg_data["PPG2"].values


# Step 1 : Grab Gain & DAC from csv file

gainOne = ppg_data["GAIN1"].values[0]
print("GAIN One", gainOne)
gainTwo = ppg_data["GAIN2"].values[0]
print("GAIN Two", gainTwo)

dacOne = ppg_data["DAC1"].values[0]
print("DAC One", dacOne)
dacTwo = ppg_data["DAC2"].values[0]
print("DAC two", dacTwo)

 # Check if Dac = 0 then set to 1
if dacOne == 0: 
    dacOne = 1

if dacTwo == 0: 
    dacTwo = 1


# Step 2 : Input into Function

# Guidelines

# RAW1 = PPG1 / (gain1 + (dac1/ 5)*2^16 )
# RAW2 = PPG2 / (gain2 + (dac2/ 5)*2^16 )

def findRaw(outputName):
    outputName += '.csv'
    raw1_data = []
    raw2_data = []
    with open(outputName, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['index', 'Raw_PPG1', 'Raw_PPG2', 'originalPPG1', 'originalPPG2'])

        for i in range(len(ppgOne)):
            raw1 = ppgOne[i] / (gainOne + (dacOne / 5) * (2 ** 16))
            raw2 = ppgTwo[i] / (gainTwo + (dacTwo / 5) * (2 ** 16))
            raw1_data.append(raw1)
            raw2_data.append(raw2)
            writer.writerow([i, raw1, raw2, ppgOne[i], ppgTwo[i]])

   # Plot the raw data and original PPG data
    plt.figure(figsize=(12, 12))
    
    plt.subplot(4, 1, 1)
    plt.plot(raw1_data, label='Raw PPG1')
    plt.title("Raw PPG1 Data")
    plt.legend()
    
    plt.subplot(4, 1, 2)
    plt.plot(raw2_data, label='Raw PPG2')
    plt.title("Raw PPG2 Data")
    plt.legend()

    plt.subplot(4, 1, 3)
    plt.plot(ppgOne, label='Original PPG1')
    plt.title("Original PPG1 Data")
    plt.legend()

    plt.subplot(4, 1, 4)
    plt.plot(ppgTwo, label='Original PPG2')
    plt.title("Original PPG2 Data")
    plt.legend()

    plt.tight_layout()
    plt.show()



def bandpassRaw(file):
    # Load ECG data from CSV file
    ppg_data = pd.read_csv(file)
    noisy_ppg_1 = ppg_data["PPG1"].values
    noisy_ppg_2 = ppg_data["PPG2"].values

    print("NOISY PPG ONE TYPE ", type(noisy_ppg_1))
    print()



    # Sampling frequency (assuming it's known)
    sampling_freq = 100  # Hz

    #--------------------------------------------------------------------------------------------------------------


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
    #filtered_ppg_2 = signal.filtfilt(b, a, noisy_ppg_2)

    # Baseline Correction
    baseline_ppg_1 = signal.medfilt(filtered_ppg_1, kernel_size=51)  # Apply a median filter as a baseline
    corrected_ppg_1 = filtered_ppg_1 - baseline_ppg_1

    # Smoothing
    smoothed_ppg_1 = signal.savgol_filter(corrected_ppg_1, window_length=51, polyorder=3)

    # Create a figure with subplots
    fig, axs = plt.subplots(3, 1, figsize=(12, 10))

    


findRaw('temp')
bandpassRaw('realPPG/IF_3_gainCheck_GREEN.csv')
