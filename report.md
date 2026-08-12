# EEG-Based Attention Analysis Using Biomedical Signal Processing

## Chapter 1 — Introduction
Electroencephalography (EEG) measures the electrical activity of the brain. This project aims to apply traditional biomedical signal processing techniques to analyze continuous EEG recordings and investigate attention-related frequency characteristics. The primary objective is to implement a complete pipeline (without machine learning) that transforms raw Biopac recordings into quantifiable attention indices, demonstrating the impact of signal preprocessing through a systematic ablation study.

## Chapter 2 — Background
The EEG signal is divided into standard frequency bands: Delta (0.5–4 Hz), Theta (4–8 Hz), Alpha (8–13 Hz), Beta (13–30 Hz), and Gamma (30–40 Hz). Attention and cognitive engagement are often associated with an increase in higher-frequency activity (Beta) relative to lower-frequency activity (Theta, Alpha). 
Welch's method for Power Spectral Density (PSD) estimation is utilized to extract these frequency characteristics by computing periodograms of overlapping windowed segments, reducing the variance compared to a standard periodogram.

## Chapter 3 — Methodology
- **Data Acquisition:** The EEG was recorded using a Biopac system at a sampling frequency of 250 Hz with 2 channels. Based on the experimental protocol, the continuous recording was systematically segmented: Baseline / Calibration (0–64 seconds) and Attention Task (194 seconds to end).
- **Preprocessing:** Linear detrending removed DC offsets and slow drifts.
- **Filtering:** A 4th-order zero-phase Butterworth band-pass filter (0.5–40 Hz) isolated the bands of interest, and a zero-phase 50 Hz notch filter mitigated mains power interference.
- **Artifact Detection:** An amplitude threshold of 100 μV was applied to 2-second epochs to reject artifacts like blinks.
- **Feature Extraction:** Welch's PSD (2-second windows) was computed. Absolute and relative band powers were extracted to calculate the Beta/Theta attention index.
- **Statistical Analysis:** Wilcoxon signed-rank tests evaluated the differences between the Baseline and Attention conditions.
- **Ablation Study:** The pipeline was executed with varying stages enabled (Raw, Detrended, Band-pass, Band-pass+Notch, Full) to quantify each stage's contribution to signal quality (RMS, 50Hz Power) and feature stability.

## Chapter 4 — Results
The complete dataset comprised 124,610 samples. Epoching into 2-second segments yielded 32 epochs for Baseline and 152 epochs for the Attention task. Given the high quality of the recording, 0 epochs were rejected by the 100 μV amplitude threshold.

### Statistical Comparison (Attention vs. Baseline)
For Channel 1, the calculated Beta/Theta indices were:
- **Baseline Mean:** 1.131
- **Attention Mean:** 1.105
- **Percentage Change:** -2.25%
- **Wilcoxon Statistic:** 200.0
- **p-value:** 0.239 (Not statistically significant)
- **Cohen's d Effect Size:** -0.278

*(See `tables/statistical_results.csv` and `results/band_power/beta_theta_comparison.png` for full details.)*

### Ablation Study Results
| Pipeline | RMS | Power 50Hz | % Rejected | Feature Variability (Beta) | Beta/Theta Mean |
|---|---|---|---|---|---|
| Raw | 2.916 | 0.01032 | 0.0 | 0.000431 | 1.194 |
| Detrended | 0.601 | 0.01032 | 0.0 | 0.000431 | 1.194 |
| Band-pass | 0.076 | 0.00009 | 0.0 | 0.000415 | 1.176 |
| Band-pass + Notch | 0.076 | 0.00002 | 0.0 | 0.000414 | 1.176 |
| Full pipeline | 0.076 | 0.00002 | 0.0 | 0.000414 | 1.176 |

## Chapter 5 — Discussion
The ablation study validates the effectiveness of the preprocessing stages. Detrending significantly reduced the signal RMS (2.916 to 0.601) by eliminating large DC offsets. The band-pass filter further reduced RMS (to 0.076) by confining the signal to physiological EEG ranges, and effectively attenuated 50Hz power. Adding the notch filter further suppressed 50Hz interference (from 0.00009 to 0.00002). Feature variability (variance of Beta power) decreased as preprocessing steps were added, confirming that preprocessing stabilizes frequency-domain features.
However, the statistical comparison of the Beta/Theta ratio showed a slight decrease (-2.25%) during the attention task, contrary to conventional expectations, but this change was not statistically significant (p = 0.239). This could indicate that the subject's cognitive state did not dramatically shift between the calibration phase and the attention task.

## Chapter 6 — Conclusion
A comprehensive biomedical signal processing pipeline was successfully implemented. Real Biopac EEG data was processed through detrending, filtering, epoching, and Welch's PSD to extract attention indices. The ablation study demonstrated that traditional filtering successfully suppresses noise and stabilizes features. While the attention index did not significantly increase in this specific unannotated recording, the methodological framework is robust, reproducible, and ready for further annotated clinical recordings.
