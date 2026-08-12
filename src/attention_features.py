import numpy as np

def calculate_attention_indices(band_powers):
    """
    Calculates EEG-derived engagement/attention indices.
    
    Parameters:
    - band_powers: dict containing absolute (or relative) band powers.
    
    Returns:
    - indices: dict containing 'Beta/Theta' and 'Beta/(Theta+Alpha)' ratios.
               Shapes will be (n_epochs, n_channels).
    """
    if not band_powers:
        return {}
        
    theta = band_powers['Theta']
    beta = band_powers['Beta']
    alpha = band_powers['Alpha']
    
    # Add a small epsilon to prevent division by zero
    eps = 1e-10
    
    beta_theta_ratio = beta / (theta + eps)
    beta_theta_alpha_ratio = beta / (theta + alpha + eps)
    
    return {
        'Beta/Theta': beta_theta_ratio,
        'Beta/(Theta+Alpha)': beta_theta_alpha_ratio
    }
