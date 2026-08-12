import numpy as np

def reject_artifacts_by_amplitude(epochs, threshold=100.0):
    """
    Identifies and rejects epochs where the absolute amplitude exceeds a given threshold.
    Since we only have 2 channels, ICA is not reliable. Amplitude thresholding is a robust
    alternative for removing blinks or large movement artifacts.
    
    Parameters:
    - epochs: numpy array of shape (n_epochs, channels, samples)
    - threshold: amplitude threshold (in the same units as the EEG data, typically microvolts)
    
    Returns:
    - clean_epochs: array with rejected epochs removed
    - rejected_indices: list of indices of the rejected epochs
    """
    if epochs.size == 0:
        return epochs, []
        
    rejected_indices = []
    clean_epochs_list = []
    
    for i, epoch in enumerate(epochs):
        # Check if any channel in this epoch exceeds the threshold
        if np.any(np.abs(epoch) > threshold):
            rejected_indices.append(i)
        else:
            clean_epochs_list.append(epoch)
            
    clean_epochs = np.array(clean_epochs_list) if len(clean_epochs_list) > 0 else np.array([])
    return clean_epochs, rejected_indices
