import numpy as np
from src.preprocessing import detrend_data
from src.filtering import apply_bandpass_filter, apply_notch_filter
from src.artifact_detection import reject_artifacts_by_amplitude
from src.epoching import epoch_data
from src.psd_analysis import calculate_psd
from src.band_power import extract_band_powers
from src.attention_features import calculate_attention_indices

def run_ablation_pipeline(data, fs, config):
    """
    Runs the pipeline based on the specified configuration.
    
    config is a dict like:
    {'detrend': True, 'bandpass': True, 'notch': True, 'artifact': True}
    """
    processed = data.copy()
    
    # 1. Preprocessing
    if config['detrend']:
        processed = detrend_data(processed)
        
    if config['bandpass']:
        processed = apply_bandpass_filter(processed, 0.5, 40.0, fs)
        
    if config['notch']:
        processed = apply_notch_filter(processed, 50.0, fs)
        
    # Epoching
    epochs = epoch_data(processed, fs, epoch_length_sec=2)
    
    # Artifact Rejection
    if config['artifact']:
        clean_epochs, rejected = reject_artifacts_by_amplitude(epochs, threshold=100.0)
        pct_rejected = (len(rejected) / len(epochs)) * 100 if len(epochs) > 0 else 0
    else:
        clean_epochs = epochs
        pct_rejected = 0
        
    if len(clean_epochs) == 0:
        return None
        
    # Calculate metrics
    # RMS
    rms = np.sqrt(np.mean(clean_epochs**2))
    
    # 50 Hz Power
    # We calculate PSD specifically up to 60Hz to see 50Hz peak, even if bandpassed to 40Hz.
    # Actually, if we bandpass to 40Hz, the 50Hz power should be attenuated, but the notch
    # will attenuate it further. Let's calculate PSD up to Nyquist for this metric.
    freqs_full, psds_full = calculate_psd(clean_epochs, fs)
    idx_50 = np.logical_and(freqs_full >= 49, freqs_full <= 51)
    power_50hz = np.mean(np.sum(psds_full[:, :, idx_50], axis=2))
    
    # Feature variability (Standard deviation of Beta power as a proxy)
    band_powers, _ = extract_band_powers(freqs_full, psds_full)
    beta_power = band_powers['Beta']
    feature_variability = np.mean(np.std(beta_power, axis=0))
    
    # Beta/Theta Attention Index
    attention_indices = calculate_attention_indices(band_powers)
    beta_theta_mean = np.mean(attention_indices['Beta/Theta'])
    
    return {
        'RMS': rms,
        'Power_50Hz': power_50hz,
        'Pct_Rejected': pct_rejected,
        'Feature_Variability': feature_variability,
        'Beta_Theta_Mean': beta_theta_mean
    }

def generate_ablation_results(baseline_data, attention_data, fs):
    """
    Runs the full ablation study over 5 configurations.
    """
    configs = {
        'Raw': {'detrend': False, 'bandpass': False, 'notch': False, 'artifact': False},
        'Detrended': {'detrend': True, 'bandpass': False, 'notch': False, 'artifact': False},
        'Band-pass': {'detrend': True, 'bandpass': True, 'notch': False, 'artifact': False},
        'Band-pass + Notch': {'detrend': True, 'bandpass': True, 'notch': True, 'artifact': False},
        'Full pipeline': {'detrend': True, 'bandpass': True, 'notch': True, 'artifact': True}
    }
    
    results = []
    
    for name, config in configs.items():
        # Run on attention data for the metrics
        metrics = run_ablation_pipeline(attention_data, fs, config)
        if metrics:
            metrics['Pipeline'] = name
            metrics.update(config)
            results.append(metrics)
            
    return results
