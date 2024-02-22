import numpy as np
import pandas as pd

# Load PPG data from CSV file
def load_ppg_data(csv_file):
    # Assuming CSV file has columns: 'timestamp', 'ppg_value'
    data = pd.read_csv(csv_file)
    timestamps = data['VAL']
    ppg_values = data['PPG1']
    return timestamps, ppg_values

# Remove DC component from PPG signal
def remove_dc_component(ppg_values):
    dc_component = np.mean(ppg_values)  # Calculate mean as DC component
    ppg_ac = ppg_values - dc_component
    return ppg_ac

# Calculate AC component using peak-to-peak method
def calculate_ac_component(ppg_ac):
    ac_component = np.ptp(ppg_ac)  # Peak-to-peak amplitude
    return ac_component

# AC represents the pulsatile physiological waveform attributed to cardiac synchronous changes in the blood volume with each heart beat

if __name__ == "__main__":
    # Load PPG data
    timestamps, ppg_values = load_ppg_data("ppg_GREEN/green1_AR.csv")

    # Remove DC component
    ppg_ac = remove_dc_component(ppg_values)

    # Calculate AC component
    ac_component = calculate_ac_component(ppg_ac)
    
    print("AC Component:", ac_component)
