import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from scipy import signal
import csv

import os
from glob import glob
import matplotlib.pyplot as plt


file = "IF_1_gainCheck.csv"
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
    with open(outputName, 'a', newline='') as file:
        data = []
        ct = 0
        writer = csv.writer(file)

        for i in ppgOne:
            data.append([ct, i / (gainOne + (dacOne/ 5)*(2**16) )])

        writer.writerows(data)

findRaw('temp')

