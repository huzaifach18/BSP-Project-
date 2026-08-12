import numpy as np
from scipy import signal

def detrend_data(data):
    """
    Removes the DC offset and slow linear drift from the EEG data using linear detrending.
    
    Parameters:
    - data: numpy array of shape (channels, samples)
    
    Returns:
    - detrended_data: numpy array of shape (channels, samples)
    """
    # scipy.signal.detrend removes linear trend along the specified axis (default axis=-1)
    detrended_data = signal.detrend(data, axis=-1, type='linear')
    return detrended_data
