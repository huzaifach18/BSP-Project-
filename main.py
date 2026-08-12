import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from src.load_data import load_eeg_data, segment_conditions
from src.preprocessing import detrend_data
from src.filtering import apply_bandpass_filter, apply_notch_filter
from src.artifact_detection import reject_artifacts_by_amplitude
from src.epoching import epoch_data
from src.psd_analysis import calculate_psd
from src.band_power import extract_band_powers
from src.attention_features import calculate_attention_indices
from src.statistics import compare_conditions, compute_cohens_d
from src.ablation import generate_ablation_results

# Define directories
BASE_DIR = r"c:\Users\chhuz\OneDrive\Desktop\BSP Projects\EEG_Attention_Project"
RESULTS_DIR = os.path.join(BASE_DIR, "results")
DIRS = {
    "raw_plots": os.path.join(RESULTS_DIR, "raw_plots"),
    "filtered_plots": os.path.join(RESULTS_DIR, "filtered_plots"),
    "psd": os.path.join(RESULTS_DIR, "psd"),
    "band_power": os.path.join(RESULTS_DIR, "band_power"),
    "ablation": os.path.join(RESULTS_DIR, "ablation"),
    "tables": os.path.join(BASE_DIR, "tables")
}

def create_dirs():
    for d in DIRS.values():
        os.makedirs(d, exist_ok=True)

def plot_raw(data, fs, condition_name):
    time = np.arange(data.shape[1]) / fs
    plt.figure(figsize=(12, 6))
    for i in range(data.shape[0]):
        plt.plot(time, data[i] + i * 200, label=f'Channel {i+1}') # Offset for visibility
    plt.title(f'Raw EEG Data - {condition_name}')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude (a.u.)')
    plt.legend()
    plt.savefig(os.path.join(DIRS["raw_plots"], f'raw_{condition_name}.png'))
    plt.close()

def plot_psd(freqs, psds, condition_name):
    mean_psd = np.mean(psds, axis=0) # Average across epochs
    plt.figure(figsize=(10, 6))
    for i in range(mean_psd.shape[0]):
        plt.plot(freqs, mean_psd[i], label=f'Channel {i+1}')
    plt.title(f'Power Spectral Density - {condition_name}')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power (uV^2/Hz)')
    plt.xlim(0, 45)
    plt.legend()
    plt.savefig(os.path.join(DIRS["psd"], f'psd_{condition_name}.png'))
    plt.close()

def process_condition(data, fs, name):
    print(f"\n--- Processing {name} ---")
    plot_raw(data, fs, name)
    
    # Preprocessing
    detrended = detrend_data(data)
    bandpassed = apply_bandpass_filter(detrended, 0.5, 40, fs)
    filtered = apply_notch_filter(bandpassed, 50, fs)
    
    # Plot filtered
    time = np.arange(filtered.shape[1]) / fs
    plt.figure(figsize=(12, 6))
    for i in range(filtered.shape[0]):
        plt.plot(time, filtered[i] + i * 200, label=f'Channel {i+1}')
    plt.title(f'Filtered EEG Data - {name}')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude (a.u.)')
    plt.legend()
    plt.savefig(os.path.join(DIRS["filtered_plots"], f'filtered_{name}.png'))
    plt.close()
    
    # Epoching
    epochs = epoch_data(filtered, fs, epoch_length_sec=2)
    print(f"Total epochs generated: {len(epochs)}")
    
    # Artifact Rejection
    clean_epochs, rejected = reject_artifacts_by_amplitude(epochs, threshold=100.0)
    print(f"Rejected epochs: {len(rejected)} ({len(rejected)/len(epochs)*100:.1f}%)")
    
    # PSD
    freqs, psds = calculate_psd(clean_epochs, fs)
    plot_psd(freqs, psds, name)
    
    # Band Powers & Features
    abs_powers, rel_powers = extract_band_powers(freqs, psds)
    features = calculate_attention_indices(abs_powers)
    
    return {
        'clean_epochs': clean_epochs,
        'abs_powers': abs_powers,
        'rel_powers': rel_powers,
        'features': features
    }

def main():
    create_dirs()
    print("Starting EEG Attention Analysis Pipeline...")
    
    # 1. Load Data
    filepath = r"c:\Users\chhuz\OneDrive\Desktop\BSP Projects\BSP_PROJECT_iKRRRR.txt"
    data, fs = load_eeg_data(filepath)
    
    # 2. Segment Data
    segments = segment_conditions(data, fs)
    
    # 3. Process Conditions
    results = {}
    for name in ['baseline', 'attention']:
        if segments[name] is not None:
            results[name] = process_condition(segments[name], fs, name)
            
    # 4. Statistical Comparison
    if 'baseline' in results and 'attention' in results:
        print("\n--- Statistical Comparison (Attention vs Baseline) ---")
        
        # Compare Beta/Theta for Channel 1 (index 0)
        baseline_bt_ch1 = results['baseline']['features']['Beta/Theta'][:, 0]
        attention_bt_ch1 = results['attention']['features']['Beta/Theta'][:, 0]
        
        stat, p_val = compare_conditions(baseline_bt_ch1, attention_bt_ch1)
        effect_size = compute_cohens_d(baseline_bt_ch1, attention_bt_ch1)
        
        stats_res = {
            "Metric": ["Beta/Theta (Ch1)"],
            "Baseline Mean": [np.mean(baseline_bt_ch1)],
            "Attention Mean": [np.mean(attention_bt_ch1)],
            "Percentage Change": [((np.mean(attention_bt_ch1) - np.mean(baseline_bt_ch1)) / np.mean(baseline_bt_ch1)) * 100],
            "Wilcoxon Stat": [stat],
            "p-value": [p_val],
            "Cohen's d": [effect_size]
        }
        df_stats = pd.DataFrame(stats_res)
        df_stats.to_csv(os.path.join(DIRS["tables"], "statistical_results.csv"), index=False)
        print(df_stats)
        
        # Plot comparison
        plt.figure(figsize=(8, 6))
        plt.boxplot([baseline_bt_ch1, attention_bt_ch1], labels=['Baseline', 'Attention'])
        plt.title('Beta/Theta Ratio Comparison (Ch 1)')
        plt.ylabel('Beta/Theta Ratio')
        plt.savefig(os.path.join(DIRS["band_power"], 'beta_theta_comparison.png'))
        plt.close()

    # 5. Ablation Study
    print("\n--- Running Ablation Study ---")
    ablation_results = generate_ablation_results(segments['baseline'], segments['attention'], fs)
    df_ablation = pd.DataFrame(ablation_results)
    
    # Reorder columns for readability
    cols = ['Pipeline', 'detrend', 'bandpass', 'notch', 'artifact', 'RMS', 'Power_50Hz', 'Pct_Rejected', 'Feature_Variability', 'Beta_Theta_Mean']
    df_ablation = df_ablation[cols]
    
    df_ablation.to_csv(os.path.join(DIRS["ablation"], "ablation_table.csv"), index=False)
    print("Ablation table saved.")
    
    print("\nPipeline Complete!")

if __name__ == "__main__":
    main()
