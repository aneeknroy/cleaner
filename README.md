# Signal Processing Project

## Overview

This project focuses on processing signals using bandpass and highpass filters in Python. The goal is to determine various parameters such as AC amplitude, Perfusion Index (PI), and Morphology (Systolic Peak, Dichroitic notch, etc.) from the processed signals.

## Features

- **Signal Processing:** The project utilizes bandpass and highpass filters to process the input signals.
  
- **AC Amplitude:** Calculates the AC amplitude of the signal after processing.
  
- **Perfusion Index (PI):** Determines the Perfusion Index (PI) as a measure of peripheral perfusion.
  
- **Morphology Analysis:** Analyzes the morphology of the signal, including identifying features like Systolic Peak and Dichroitic notch.

## Technologies Used

- Python
- NumPy
- SciPy
- Matplotlib
- Pandas

## Usage

1. Install the required libraries using `pip install -r requirements.txt`.
2. Run the main script `signal_processing.py` to process the signals and analyze their parameters.
3. Modify the input signals or parameters as needed for your specific use case.

## Files Included

- `signal_processing.py`: Main script for signal processing and analysis.
- `requirements.txt`: List of required Python libraries.
- `sample_signals.csv`: Sample input signals for testing.

## Results

The project generates results such as AC amplitude, Perfusion Index (PI), and Morphology analysis of the input signals. These results can be used for further analysis or visualization.

## License

This project is licensed under the [MIT License](LICENSE).
