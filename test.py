
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

    # Initialize dictionaries to store the DAC values and PGA gain settings
    dac_values = [0,0]
    pga_gains = [0,0]
    
     # Iterate over each row in the data
    for index, row in data.iterrows():
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

    return dac_values, pga_gains

extract_DAC_GAIN('realPPG/2023-10-26-12-33-16.330.csv')