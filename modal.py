import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from glob import glob


# Function to extract features from a PPG window
def extract_features(signal, fs):
    # Calculate statistical features
    mean = np.mean(signal)
    std = np.std(signal)
    skew = np.mean((signal - mean) ** 3) / std ** 3
    kurt = np.mean((signal - mean) ** 4) / std ** 4

    # Calculate frequency-domain features
    fft_vals = np.abs(np.fft.fft(signal))
    fft_freqs = np.fft.fftfreq(len(signal), 1 / fs)
    mask = fft_freqs > 0
    fft_log = np.log(fft_vals[mask])
    spectral_entropy = -np.sum(fft_log * fft_vals[mask] / np.sum(fft_vals[mask]))

    # Calculate time-domain features
    signal_mag_area = np.sum(np.abs(signal))
    zero_crossing_rate = np.sum(np.abs(np.diff(np.sign(signal)))) / (len(signal) - 1)
    slope_transit_time = np.sum(np.abs(np.diff(signal))) / (len(signal) - 1)

    return [mean, std, skew, kurt, spectral_entropy, signal_mag_area, zero_crossing_rate, slope_transit_time]

# Function to preprocess and extract features from a PPG signal
def preprocess_signal(signal, fs, window_size, overlap):
    # Bandpass filter the signal
    nyquist_freq = 0.5 * fs
    low_cutoff = 0.5 / nyquist_freq
    high_cutoff = 8 / nyquist_freq
    order = 2
    normalized_low = low_cutoff / nyquist_freq
    normalized_high = high_cutoff / nyquist_freq
    b, a = butter(order, [normalized_low, normalized_high], btype='band')
    filtered_signal = filtfilt(b, a, signal)

    # Detrend and normalize the signal
    detrended_signal = filtered_signal - np.mean(filtered_signal)
    normalized_signal = detrended_signal / np.max(np.abs(detrended_signal))

    # Extract features from overlapping windows
    window_samples = int(window_size * fs)
    overlap_samples = int(overlap * window_samples)
    features = []
    for i in range(0, len(normalized_signal) - window_samples, window_samples - overlap_samples):
        window = normalized_signal[i:i + window_samples]
        features.append(extract_features(window, fs))

    return np.array(features)

# Load and preprocess the PPG data

greenPath = './ppg_GREEN/'
redPath = './ppg_RED/'
irPath = './ppg_IR/'

data_dir = 'ppg_GREEN'
fs = 100  # Assuming a sampling rate of 100 Hz
window_size = 5  # Window size in seconds
overlap = 0.5  # Overlap percentage

X = []
y = []

for file in glob(greenPath + '*.csv'):
    data = pd.read_csv(file)
    ppg_signal = data["PPG1"].values
    features = preprocess_signal(ppg_signal, fs, window_size, overlap)
    X.extend(features)

    # Manually label the windows (0 for clean, 1 for artifact)
    labels = [0] * len(features)  # Replace with manual labeling

    y.extend(labels)

X = np.array(X)
y = np.array(y)

# Split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a random forest classifier
rf_clf = RandomForestClassifier(n_estimators=100, random_state=42)
rf_clf.fit(X_train, y_train)

# Evaluate the model
y_pred = rf_clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print(f'Accuracy: {accuracy:.3f}')
print(f'Precision: {precision:.3f}')
print(f'Recall: {recall:.3f}')
print(f'F1-score: {f1:.3f}')

# Apply the model to new PPG signals for artifact removal
new_signal = ...  # Load a new PPG signal
new_features = preprocess_signal(new_signal, fs, window_size, overlap)
artifact_labels = rf_clf.predict(new_features)

# Reconstruct the denoised signal
denoised_signal = np.zeros_like(new_signal)
start_idx = 0
for i, label in enumerate(artifact_labels):
    window_samples = int(window_size * fs)
    if label == 0:  # Clean window
        denoised_signal[start_idx:start_idx + window_samples] = new_signal[start_idx:start_idx + window_samples]
    else:  # Artifact window
        # Apply signal reconstruction technique (e.g., interpolation)
        denoised_signal[start_idx:start_idx + window_samples] = np.interp(
            np.arange(start_idx, start_idx + window_samples),
            np.concatenate([[start_idx - 1], np.arange(start_idx + window_samples, len(new_signal))]),
            np.concatenate([[new_signal[start_idx - 1]], new_signal[start_idx + window_samples:]]))

    start_idx += window_samples - int(overlap * window_samples)