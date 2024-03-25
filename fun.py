import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from scipy import signal
import matplotlib.pyplot as plt


# Define the neural network model
class PPGNet(nn.Module):
    def __init__(self):
        super(PPGNet, self).__init__()
        self.fc1 = nn.Linear(1000, 512)  # Input size 1000 (assuming sample size), output size 512
        self.fc2 = nn.Linear(512, 256)
        self.fc3 = nn.Linear(256, 1000)  # Output size 1 (clean PPG signal)

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

# Resize input tensor to match the expected input size of the model
noisy_ppg_tensor = noisy_ppg_tensor.view(1, -1)  # Reshape to 1x1000

# Instantiate the neural network model
model = PPGNet()

# Define loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Assuming you have clean PPG data for training
clean_ppg = preprocess_ppg("cleanPPG.csv")
clean_ppg_tensor = torch.tensor(clean_ppg, dtype=torch.float32)
clean_ppg_tensor = clean_ppg_tensor.unsqueeze(0)  # Add batch dimension

# Train the model
num_epochs = 100
for epoch in range(num_epochs):
    optimizer.zero_grad()
    outputs = model(noisy_ppg_tensor)
        
    loss = criterion(outputs, clean_ppg_tensor)
    loss.backward()
    optimizer.step()

    if (epoch+1) % 100 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item()}')

# Perform inference
clean_ppg_output = model(noisy_ppg_tensor)
print("Clean PPG Output shape:", clean_ppg_output.shape)
print("Clean PPG Output:", clean_ppg_output)


# Convert the tensors to numpy arrays for plotting
noisy_ppg_np = noisy_ppg_tensor.detach().cpu().numpy().flatten()
clean_ppg_output_np = clean_ppg_output.detach().cpu().numpy().flatten()

# Plotting
plt.figure(figsize=(15, 6))

# Plot the original noisy PPG data
plt.subplot(2, 1, 1)  # 2 rows, 1 column, 1st subplot
plt.plot(noisy_ppg_np, label='Original Noisy PPG', color='gray')
plt.title('Original Noisy PPG Data')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.grid(True)
plt.legend()

# Plot the cleaned PPG output from the model
plt.subplot(2, 1, 2)  # 2 rows, 1 column, 2nd subplot
plt.plot(clean_ppg_output_np, label='Cleaned PPG Output', color='blue')
plt.title('Cleaned PPG Output')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()


 # if noisy_ppg_tensor.size() == clean_ppg_tensor.size():
    #     print("Tensors have the same size.")
    # else:
    #     print("Tensors do not have the same size.")
    #     print("noisy ppg tensor size : ", noisy_ppg_tensor.size())
    #     print("clean ppg tensor size : ", clean_ppg_tensor.size())
