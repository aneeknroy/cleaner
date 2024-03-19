import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from scipy import signal



# TODO - make this more accurate - add parameters to peak 2 peak in order stop the values getting   
#        skewed by a very large peak therefore messing up the whole entire AC_Componenet

def bandpass(csv_file):
        # Load ECG data from CSV file
        ppg_data = pd.read_csv(csv_file)
        noisy_ppg_1 = ppg_data["PPG1"].values

        # Sampling frequency (assuming it's known)
        sampling_freq = 100  # Hz

        # Define Filter Parameters
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
        
        return smoothed_ppg_1


# Remove DC component from PPG signal
def remove_dc_component(ppg_values):
    dc_component = np.mean(ppg_values)  # Calculate mean as DC component
    ppg_ac = ppg_values - dc_component
    return ppg_ac

# Calculate AC component using peak-to-peak method
def calculate_ac_component(ppg_ac):
    peaks, _ = find_peaks(ppg_ac)  # Adjust height threshold as needed
    troughs, _ = find_peaks(-ppg_ac)  # Detect troughs by inverting signal
    ac_component = ppg_ac[peaks].mean() - ppg_ac[troughs].mean()
    return ac_component

# AC represents the pulsatile physiological waveform attributed to cardiac synchronous changes in the blood volume with each heart beat

if __name__ == "__main__":
    # Load PPG data
    bandPPG = bandpass("ppg_GREEN/green5_AR.csv")


    # Remove DC component
    ppg_ac = remove_dc_component(bandPPG)

    # Calculate AC component
    ac_component = calculate_ac_component(ppg_ac)
    
    print("AC Component:", ac_component)

