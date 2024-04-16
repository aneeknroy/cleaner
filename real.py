import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from scipy import signal
import csv

import os
from glob import glob
import matplotlib.pyplot as plt


file = "realPPG/IF_3_gainCheck.csv"
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
        writer.writerow(['index', 'Raw_PPG1', 'Raw_PPG2'])

        for i in range(len(ppgOne)):
            raw1 = ppgOne[i] / (gainOne + (dacOne / 5) * (2 ** 16))
            raw2 = ppgTwo[i] / (gainTwo + (dacTwo / 5) * (2 ** 16))
            raw1_data.append(raw1)
            raw2_data.append(raw2)
            writer.writerow([i, raw1, raw2])

    # Plot the raw data
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(raw1_data)
    plt.title("RAW1 Data")
    plt.subplot(2, 1, 2)
    plt.plot(raw2_data)
    plt.title("RAW2 Data")
    plt.tight_layout()
    plt.show()


findRaw('temp')

