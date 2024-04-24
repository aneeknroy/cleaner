import sys
import os
import csv


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.signal import find_peaks, butter, filtfilt, medfilt, savgol_filter
from scipy import signal


def extract_DAC_GAIN(file_path):
     # Read the file using the determined delimiter
    data = pd.read_csv(file_path, delimiter=';', header=None, names=['Data'])

    count = 0

    # Initialize dictionaries to store the DAC values and PGA gain settings
    dac_values = []
    pga_gains = []
    
     # Iterate over each row in the data
    for index, row in data.iterrows():
        if count == 2:
            break

        # Check for DAC value and voltage
        if 'DAC Value' in row['Data']:
            # Extract the voltage
            voltage = float(row['Data'].split(':')[2].strip()[:-1])
            dac_values.append(voltage)
        
        # Check for PGA gain setting
        if 'PGA Gain Setting' in row['Data']:
            # Extract the gain value
            gain = int(row['Data'].split(':')[1].strip())
            pga_gains.append(gain)
            count += 1

    return dac_values, pga_gains

def findRaw(file, subjectName, folder):
    ppg_data = pd.read_csv(file)

    ppgOne = ppg_data["PPG1"].values
    ppgTwo = ppg_data["PPG2"].values
    
    print("about to extract")
    dacValues, gainValues = extract_DAC_GAIN(file)

    dacOne = dacValues[0]
    dacTwo = dacValues[1]

    gainOne = gainValues[0]
    gainTwo = gainValues[1]

    # Ensure the output folder exists
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Construct the full path for the output file
    outputFilePath = os.path.join(folder, 'RAW_' + subjectName + '.csv')

    # Create and write data to the CSV file
    with open(outputFilePath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['VAL', 'PPG1', 'PPG2', 'originalPPG1', 'originalPPG2'])

        for i in range(len(ppgOne)):
            raw1 = ppgOne[i] / (gainOne + (dacOne / 5) * (2 ** 16))
            raw2 = ppgTwo[i] / (gainTwo + (dacTwo / 5) * (2 ** 16))
            writer.writerow([i, raw1, raw2, ppgOne[i], ppgTwo[i]])

    return outputFilePath
    
def bandpass(csv_file, folder, subjectName):
    # Ensure the folder exists
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Load PPG data from CSV file
    ppg_data = pd.read_csv(csv_file)
    noisy_ppg_1 = ppg_data["PPG1"].values
    noisy_ppg_2 = ppg_data["PPG2"].values

    sampling_freq = 100 # Hz

    lowcut = 0.5                         # Lower Cutoff Frequency in Hz
    highcut = 35.0                       # Higher Cutoff Frequency in Hz
    nyquist_freq = 0.5 * sampling_freq   # Nyquist frequency in Hz
    order = 4                            # Filter order

    # Design Bandpass Filter
    b, a = signal.butter(order, [lowcut / nyquist_freq, highcut / nyquist_freq], btype='band')

    # Apply HighPass Filter to noisy ECG Signal
    filtered_ppg_1 = signal.filtfilt(b, a, noisy_ppg_1)
    filtered_ppg_2 = signal.filtfilt(b, a, noisy_ppg_2)


    # Baseline Correction
    baseline_ppg_1 = signal.medfilt(filtered_ppg_1, kernel_size=51)  # Apply a median filter as a baseline
    corrected_ppg_1 = filtered_ppg_1 - baseline_ppg_1

    baseline_ppg_2 = signal.medfilt(filtered_ppg_2, kernel_size=51)  # Apply a median filter as a baseline
    corrected_ppg_2 = filtered_ppg_2 - baseline_ppg_2

    # Smoothing
    smoothed_ppg_1 = signal.savgol_filter(corrected_ppg_1, window_length=51, polyorder=3)
    smoothed_ppg_2 = signal.savgol_filter(corrected_ppg_2, window_length=51, polyorder=3)

    # Remove the DC Component
    dc_component1 = np.mean(smoothed_ppg_1)
    dc_component2 = np.mean(smoothed_ppg_2)

    ppg_ac1 = smoothed_ppg_1 - dc_component1
    ppg_ac2 = smoothed_ppg_2 - dc_component2


    # Calculate the AC Component
    peaks1, _ = find_peaks(ppg_ac1)  # Adjust height threshold as needed
    troughs1, _ = find_peaks(-ppg_ac1)  # Detect troughs by inverting signal
    ac_component1 = ppg_ac1[peaks1].mean() - ppg_ac1[troughs1].mean()

    peaks2, _ = find_peaks(ppg_ac2)  # Adjust height threshold as needed
    troughs2, _ = find_peaks(-ppg_ac2)  # Detect troughs by inverting signal
    ac_component2 = ppg_ac2[peaks2].mean() - ppg_ac2[troughs2].mean()

    # Calculate Pulse Amplitude
    if len(peaks1) > 0 and len(troughs1) > 0:
        pulse_amplitude1 = smoothed_ppg_1[peaks1].mean() - smoothed_ppg_1[troughs1].mean()
    else:
        pulse_amplitude1 = np.nan
    
    if len(peaks2) > 0 and len(troughs2) > 0:
        pulse_amplitude2 = smoothed_ppg_2[peaks2].mean() - smoothed_ppg_2[troughs2].mean()
    else:
        pulse_amplitude2 = np.nan

    # Calculate Baseline Amplitude
    baseline_amplitude1 = smoothed_ppg_1.mean()
    baseline_amplitude2 = smoothed_ppg_2.mean()

    # Calculate Perfusion Index
    if not np.isnan(pulse_amplitude1) and not np.isnan(baseline_amplitude1):
        perfusion_index1 = (pulse_amplitude1 / baseline_amplitude1) * 100
    else:
        perfusion_index1 = np.nan

     # Calculate Perfusion Index
    if not np.isnan(pulse_amplitude2) and not np.isnan(baseline_amplitude2):
        perfusion_index2 = (pulse_amplitude2 / baseline_amplitude2) * 100
    else:
        perfusion_index2 = np.nan

    acComponents = []
    perfComponents = []

    acComponents.append(ac_component1)
    acComponents.append(ac_component2)

    perfComponents.append(perfusion_index1)
    perfComponents.append(perfusion_index2)

    # Create DataFrame for CSV output
    output_data = pd.DataFrame({
        'VAL': range(len(noisy_ppg_1)),
        'PPG1': noisy_ppg_1,
        'smoothPPG1': smoothed_ppg_1,
        'PPG2': noisy_ppg_2,
        'smoothPPG2': smoothed_ppg_2
    })

    # Save to CSV
    output_csv_path = os.path.join(folder, 'ppg_data_processed_' + subjectName + '_BANDPASS.csv')
    output_data.to_csv(output_csv_path, index=False)

    # Plotting the results
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))

    # PPG1 Plots
    axs[0, 0].plot(ppg_data["VAL"], noisy_ppg_1, color='blue', label='Original PPG1')
    axs[0, 0].set_title('Original PPG1 Signal')
    axs[0, 1].plot(ppg_data["VAL"], smoothed_ppg_1, color='red', label='Smoothed PPG1')
    axs[0, 1].set_title('Smoothed PPG1 Signal')

    # PPG2 Plots
    axs[1, 0].plot(ppg_data["VAL"], noisy_ppg_2, color='blue', label='Original PPG2')
    axs[1, 0].set_title('Original PPG2 Signal')
    axs[1, 1].plot(ppg_data["VAL"], smoothed_ppg_2, color='red', label='Smoothed PPG2')
    axs[1, 1].set_title('Smoothed PPG2 Signal')

    # Labeling and saving
    for ax in axs.flat:
        ax.set(xlabel='Time (s)', ylabel='Amplitude')
        ax.legend()
        ax.grid(True)

    plt.tight_layout()
    plt.savefig(os.path.join(folder, 'bandpass_graphs_' + subjectName + '.png'))  # Save the plot to the specified folder
    plt.show()

    return output_csv_path, acComponents, perfComponents



def process_ppg(csv_file, folder, subjectName):

    output_csv_path, acComponentsOriginal, perfComponentsOriginal = bandpass(csv_file, folder, subjectName)
    print("originalBandpass completed")
    rawFilePath = findRaw(csv_file, subjectName, folder)
    print("raw file path found")
    print(rawFilePath)
    print("  ")
    output_csv_pathRAW, acComponentsRAW, perfComponentsRAW = bandpass(rawFilePath, folder, subjectName+'RAW_')
    print("RETURNING RESULTSDF")
    return results_df


    

def main():
    if len(sys.argv) < 4:
        print("Usage: python script.py <csv_file> <output_folder> <subject_name>")
        sys.exit(1)
    csv_file = sys.argv[1]
    output_folder = sys.argv[2]
    subject_name = sys.argv[3]

    try:
        process_ppg(csv_file, output_folder, subject_name)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    results_df = main()

