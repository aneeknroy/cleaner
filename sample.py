import numpy as np
import matplotlib.pyplot as plt

# Generate synthetic PPG data
t = np.linspace(0, 10, 1000)  # Time vector
baseline = 1.0  # Baseline signal level
amplitude = 0.5  # Pulse amplitude
frequency = 1.0  # Pulse frequency
ppg_signal = baseline + amplitude * np.sin(2 * np.pi * frequency * t)

# Add noise to the signal
noise_level = 0.1
noisy_ppg_signal = ppg_signal + np.random.normal(scale=noise_level, size=len(t))

# Plot the synthetic PPG data
plt.figure(figsize=(10, 5))
plt.plot(t, noisy_ppg_signal, label='Noisy PPG Signal', color='blue')
plt.plot(t, ppg_signal, label='Clean PPG Signal', linestyle='--', color='red')
plt.title('Synthetic PPG Data')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)
plt.show()
