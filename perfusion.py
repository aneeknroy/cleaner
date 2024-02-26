import pandas as pd
import numpy as np
from scipy.signal import find_peaks


# CODE TO CALCULATE THE Perfusion Index given the PPG Values

# Load CSV data
data = pd.read_csv("ppg_IR/ir5_AR.csv")
ppg_signal = data['PPG1']


# Find peaks and troughs-------------------------------------------------------------------------------
peaks, _ = find_peaks(ppg_signal)  # Adjust height threshold as needed
print('Peaks :', peaks)

troughs, _ = find_peaks(-ppg_signal)  # Detect troughs by inverting signal
print("Troughs : ", troughs, "\n")

#-------------------------------------------------------------------------------------------------------


# Calculate Pulse Amplitude ----------------------------------------------------------------------------
if len(peaks) > 0 and len(troughs) > 0:
    pulse_amplitude = ppg_signal[peaks].mean() - ppg_signal[troughs].mean()
else:
    pulse_amplitude = np.nan

print("Pulse Amplitude : ", pulse_amplitude, "\n")

#-------------------------------------------------------------------------------------------------------

# Calculate Baseline Amplitude -------------------------------------------------------------------------
baseline_amplitude = ppg_signal.mean()
print("Baseline Amplitude : ", baseline_amplitude, "\n")

#-------------------------------------------------------------------------------------------------------

# Calculate Perfusion Index
# Compute Perfusion Index
if not np.isnan(pulse_amplitude) and not np.isnan(baseline_amplitude):
    perfusion_index = (pulse_amplitude / baseline_amplitude) * 100
else:
    perfusion_index = np.nan

print("Perfusion Index:", perfusion_index)

