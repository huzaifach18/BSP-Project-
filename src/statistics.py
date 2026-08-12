import numpy as np
from scipy import stats

def compare_conditions(condition1_features, condition2_features):
    """
    Performs paired statistical analysis comparing two conditions (e.g. Baseline vs Attention).
    Uses Wilcoxon signed-rank test since EEG band powers are often non-normally distributed.
    
    Parameters:
    - condition1_features: array of shape (n_epochs_1,)
    - condition2_features: array of shape (n_epochs_2,)
    
    Returns:
    - stat: test statistic
    - p_val: p-value
    """
    # For paired tests, we need equal number of samples.
    # Since conditions might have different recording durations and rejected epochs,
    # we take the minimum number of epochs available from both conditions.
    n_min = min(len(condition1_features), len(condition2_features))
    
    if n_min < 5:
        # Not enough data for reliable statistics
        return np.nan, np.nan
        
    # We sample the first n_min epochs or we could do independent tests (Mann-Whitney U)
    # The prompt suggests "paired statistical analysis while accounting for the repeated nature of epochs."
    # We'll use the minimum length to pair them chronologically as a proxy for paired analysis within one subject.
    c1 = condition1_features[:n_min]
    c2 = condition2_features[:n_min]
    
    # Wilcoxon signed-rank test
    stat, p_val = stats.wilcoxon(c1, c2, nan_policy='omit')
    
    return stat, p_val

def compute_cohens_d(c1, c2):
    """
    Compute Cohen's d effect size for two groups.
    """
    n_min = min(len(c1), len(c2))
    if n_min < 2:
        return np.nan
    c1_sub = c1[:n_min]
    c2_sub = c2[:n_min]
    
    mean_diff = np.mean(c2_sub) - np.mean(c1_sub)
    pooled_std = np.sqrt((np.std(c1_sub, ddof=1)**2 + np.std(c2_sub, ddof=1)**2) / 2)
    
    if pooled_std == 0:
        return 0.0
    return mean_diff / pooled_std
