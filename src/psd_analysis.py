import numpy as np
from scipy import signal

def calculate_psd(epochs, fs, nperseg=None):
    """
    Calculates the Power Spectral Density (PSD) using Welch's method for a set of epochs.
    
    Parameters:
    - epochs: numpy array of shape (n_epochs, channels, epoch_samples)
    - fs: sampling frequency
    - nperseg: length of each segment for Welch's method. Defaults to half the epoch length.
    
    Returns:
    - freqs: Array of sample frequencies
    - psd: numpy array of shape (n_epochs, channels, len(freqs)) representing PSD
    """
    if epochs.size == 0:
        return np.array([]), np.array([])
        
    n_epochs, n_channels, n_samples = epochs.shape
    
    if nperseg is None:
        nperseg = min(n_samples, int(fs * 1.0)) # 1 second windows by default if possible
        
    # Initialize empty array for PSDs
    # We need to know the number of frequency bins first
    f, _ = signal.welch(epochs[0, 0, :], fs, nperseg=nperseg)
    n_freqs = len(f)
    
    psds = np.zeros((n_epochs, n_channels, n_freqs))
    
    for i in range(n_epochs):
        for c in range(n_channels):
            f, pxx = signal.welch(epochs[i, c, :], fs, nperseg=nperseg)
            psds[i, c, :] = pxx
            
    return f, psds
