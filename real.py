import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from scipy import signal

import os
from glob import glob
import matplotlib.pyplot as plt


file = "IF_1_gainCheck.csv"
ppg_data = pd.read_csv(file)

ppgOne = ppg_data["PPG1"].values
ppgTwo = ppg_data["PPG2"].values


# Step 1 : Grab Gain & DAC from csv file

gainOne = ppg_data["GAIN1"].values
gainTwo = ppg_data["GAIN2"].values

dacOne = ppg_data["DAC1"].values
dacTwo = ppg_data["DAC2"].values



# Step 2 : Input into Function

# Guidelines

# RAW1 = PPG1 / (gain1 + (dac1/ 5)*2^16 )
# RAW2 = PPG2 / (gain2 + (dac2/ 5)*2^16 )

def findRaw():
    rawOne = []
    rawTwo = []
    for i,j in ppgOne, ppgTwo:
        rawOne.append( i / (gainOne + (dacOne/ 5)*2^16 ))
        rawTwo.append( j / (gainTwo + (dacTwo/ 5)*2^16 ))
    print(rawOne)



