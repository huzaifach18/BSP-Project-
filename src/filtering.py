import numpy as np
from scipy.signal import butter, filtfilt, iirnotch

def apply_bandpass_filter(data, lowcut, highcut, fs, order=4):
    """
    Applies a zero-phase Butterworth band-pass filter.
    Zero-phase filtering (filtfilt) avoids phase distortion.
    
    Parameters:
    - data: numpy array of shape (channels, samples)
    - lowcut: lower cutoff frequency in Hz
    - highcut: upper cutoff frequency in Hz
    - fs: sampling frequency in Hz
    - order: order of the Butterworth filter
    """
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    filtered_data = filtfilt(b, a, data, axis=-1)
    return filtered_data

def apply_notch_filter(data, freq, fs, quality_factor=30):
    """
    Applies a zero-phase IIR notch filter to remove specific interference (e.g., 50 Hz power-line).
    
    Parameters:
    - data: numpy array of shape (channels, samples)
    - freq: frequency to remove in Hz
    - fs: sampling frequency in Hz
    - quality_factor: Q-factor of the filter
    """
    b, a = iirnotch(freq, quality_factor, fs)
    filtered_data = filtfilt(b, a, data, axis=-1)
    return filtered_data
