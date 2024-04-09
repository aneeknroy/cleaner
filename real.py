import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from scipy import signal

import os
from glob import glob
import matplotlib.pyplot as plt



ppg_data = pd.read_csv(file)
noisy_ppgOne = ppg_data["PPG1"].values


# Step 1 : Grab Gain & DAC from csv file


# Step 2 : Input into Function

# Guidelines

# RAW1 = PPG1 / (gain1 + (dac1/ 5)*2^16 )
# RAW2 = PPG2 / (gain2 + (dac2/ 5)*2^16 )