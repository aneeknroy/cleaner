import numpy as np
import pandas as pd

# Load the CSV file into a pandas DataFrame
df = pd.read_csv("ppg_AR/green1_AR.csv")

# Calculate the mean of the PPG values (DC component)
dc_component = df['PPG1'].mean()

# Subtract the DC component from each PPG value to get the AC component
df['AC'] = df['PPG1'] - dc_component

# Print the DataFrame with AC component added
print(df)