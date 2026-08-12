import numpy as np

# Define standard EEG frequency bands
BANDS = {
    'Delta': (0.5, 4),
    'Theta': (4, 8),
    'Alpha': (8, 13),
    'Beta': (13, 30),
    'Gamma': (30, 40)
}

def extract_band_powers(freqs, psds):
    """
    Calculates absolute and relative band powers from PSDs.
    
    Parameters:
    - freqs: numpy array of frequencies (from Welch's method)
    - psds: numpy array of PSDs, shape (n_epochs, n_channels, n_freqs)
    
    Returns:
    - band_powers: dict of absolute powers, e.g. {'Alpha': array(n_epochs, n_channels)}
    - relative_band_powers: dict of relative powers
    """
    if psds.size == 0:
        return {}, {}
        
    n_epochs, n_channels, _ = psds.shape
    band_powers = {band: np.zeros((n_epochs, n_channels)) for band in BANDS}
    relative_band_powers = {band: np.zeros((n_epochs, n_channels)) for band in BANDS}
    
    # Calculate frequency resolution
    df = freqs[1] - freqs[0]
    
    # Calculate absolute power for each band
    for band, (low, high) in BANDS.items():
        # Find frequency indices within the band
        idx_band = np.logical_and(freqs >= low, freqs <= high)
        
        # Integrate PSD over the frequency band (Simpson's rule or simple sum * df)
        # We use simple sum * df as a standard Riemann sum approach
        band_power = np.sum(psds[:, :, idx_band], axis=2) * df
        band_powers[band] = band_power
        
    # Calculate total power (0.5 to 40 Hz)
    idx_total = np.logical_and(freqs >= 0.5, freqs <= 40)
    total_power = np.sum(psds[:, :, idx_total], axis=2) * df
    
    # Calculate relative power
    for band in BANDS:
        relative_band_powers[band] = band_powers[band] / total_power
        
    return band_powers, relative_band_powers
