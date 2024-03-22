import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from scipy import signal

# Define the neural network model
class PPGNet(nn.Module):
    def __init__(self):
        super(PPGNet, self).__init__()
        self.fc1 = nn.Linear(1000, 512)  # Input size 1000 (assuming sample size), output size 512
        self.fc2 = nn.Linear(512, 256)
        self.fc3 = nn.Linear(256, 1)  # Output size 1 (clean PPG signal)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# Load PPG data and preprocess
def preprocess_ppg(csv_file):
    ppg_data = pd.read_csv(csv_file)
    noisy_ppg = ppg_data["PPG1"].values
    return noisy_ppg

# Convert data to PyTorch tensors and prepare for training
noisy_ppg = preprocess_ppg("ppg_GREEN/green1_AR.csv")
noisy_ppg_tensor = torch.tensor(noisy_ppg, dtype=torch.float32)
noisy_ppg_tensor = noisy_ppg_tensor.unsqueeze(0)  # Add batch dimension

# Instantiate the neural network model
model = PPGNet()

# Define loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Train the model
num_epochs = 1000
for epoch in range(num_epochs):
    optimizer.zero_grad()
    outputs = model(noisy_ppg_tensor)
    
    # Assuming you have clean PPG data for training
    clean_ppg = preprocess_ppg("cleanPPG.csv")
    clean_ppg_tensor = torch.tensor(clean_ppg, dtype=torch.float32)
    clean_ppg_tensor = clean_ppg_tensor.unsqueeze(0)  # Add batch dimension
    
    loss = criterion(outputs, clean_ppg_tensor)
    loss.backward()
    optimizer.step()

    if (epoch+1) % 100 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item()}')

# Perform inference
clean_ppg_output = model(noisy_ppg_tensor)
print("Clean PPG Output:", clean_ppg_output.item())
