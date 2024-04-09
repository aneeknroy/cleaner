import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from scipy import signal

import os
from glob import glob
import matplotlib.pyplot as plt



ppg_data = pd.read_csv(file)
noisy_ppgOne = ppg_data["PPG1"].values


# Step 1 : Grad Gain & DAC from csv file