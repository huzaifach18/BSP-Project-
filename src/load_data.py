import numpy as np
import os
import mne

def load_eeg_data(filepath, sampling_rate=250.0):
    """
    Loads the EEG data.
    Since we have BSP_PROJECT_iKRRRR.txt containing two columns of data,
    we'll load it using numpy.
    """
    print(f"Loading data from {filepath}...")
    
    # Check if the file is txt, edf or mat. We will prioritize txt for simplicity 
    # since it directly contains the raw samples.
    if filepath.endswith('.txt'):
        data = np.loadtxt(filepath)
        if data.shape[1] == 2:
            data = data.T # shape should be (channels, samples)
    elif filepath.endswith('.edf'):
        raw = mne.io.read_raw_edf(filepath, preload=True, verbose='ERROR')
        data = raw.get_data()
        sampling_rate = raw.info['sfreq']
    else:
        raise ValueError("Unsupported file format. Please use .txt or .edf")
        
    print(f"Data shape: {data.shape}")
    print(f"Sampling frequency: {sampling_rate} Hz")
    
    # Calculate duration
    duration = data.shape[1] / sampling_rate
    print(f"Total duration: {duration:.2f} seconds ({duration/60:.2f} minutes)")
    
    return data, sampling_rate

def segment_conditions(data, sampling_rate):
    """
    Segment the data based on the user's provided exact timings:
    - 0 to 64 seconds: Baseline / Calibration
    - 64 to 194 seconds: Eyes Closed (Relaxed)
    - 194 seconds to end: Attention Task
    """
    baseline_start = 0
    baseline_end = int(64 * sampling_rate)
    
    eyes_closed_start = int(64 * sampling_rate)
    eyes_closed_end = int(194 * sampling_rate)
    
    attention_start = int(194 * sampling_rate)
    
    baseline_data = data[:, baseline_start:baseline_end]
    
    if data.shape[1] > eyes_closed_end:
        eyes_closed_data = data[:, eyes_closed_start:eyes_closed_end]
        attention_data = data[:, attention_start:]
    else:
        # If the recording is shorter, adjust
        eyes_closed_data = None
        attention_data = data[:, baseline_end:]

    return {
        'baseline': baseline_data,
        'eyes_closed': eyes_closed_data,
        'attention': attention_data
    }
