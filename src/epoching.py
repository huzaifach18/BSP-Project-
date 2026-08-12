import numpy as np

def epoch_data(data, fs, epoch_length_sec=2, overlap_sec=0):
    """
    Divides continuous data into smaller epochs (windows).
    
    Parameters:
    - data: numpy array of shape (channels, samples)
    - fs: sampling frequency
    - epoch_length_sec: length of each epoch in seconds
    - overlap_sec: overlap between consecutive epochs in seconds
    
    Returns:
    - epochs: numpy array of shape (n_epochs, channels, epoch_samples)
    """
    epoch_samples = int(epoch_length_sec * fs)
    overlap_samples = int(overlap_sec * fs)
    step_samples = epoch_samples - overlap_samples
    
    n_channels, n_samples = data.shape
    
    # Calculate number of full epochs possible
    n_epochs = (n_samples - epoch_samples) // step_samples + 1
    
    if n_epochs <= 0:
        return np.array([])
        
    epochs = np.zeros((n_epochs, n_channels, epoch_samples))
    
    for i in range(n_epochs):
        start_idx = i * step_samples
        end_idx = start_idx + epoch_samples
        epochs[i, :, :] = data[:, start_idx:end_idx]
        
    return epochs
