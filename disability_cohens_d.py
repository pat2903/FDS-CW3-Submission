import os
import pandas as pd
import numpy as np
from scipy.stats import norm

data_filepath = os.path.join(os.getcwd(), 'NSS23_characteristic_workbook.xlsx')

full_df = pd.read_excel(data_filepath, sheet_name=4, skiprows=2)

# filter full_df to try make it run faster
df = full_df[['Split', 'Positvity measure (%)']].copy()


disability_df = df[df['Split'] == "Disability reported"]['Positvity measure (%)'].copy()
no_disability_df = df[df['Split'] == "No disability reported"]['Positvity measure (%)'].copy()

def calculate_cohens_d(series1, series2):
    """Calculate Cohen's d for two series."""
    mean1, mean2 = series1.mean(), series2.mean()
    sd1, sd2 = series1.std(), series2.std()
    n1, n2 = len(series1), len(series2)
    pooled_sd = np.sqrt(((n1 - 1) * sd1 ** 2 + (n2 - 1) * sd2 ** 2) / (n1 + n2 - 2))
    d = (mean1 - mean2) / pooled_sd
    return d

def cohens_d_confidence_interval(d, n1, n2, alpha=0.05):
    """Calculate the confidence interval for Cohen's d."""
    SE = np.sqrt((n1 + n2) / (n1 * n2) + d ** 2 / (2 * (n1 + n2)))
    Z = norm.ppf(1 - alpha / 2)
    lower_bound = d - Z * SE
    upper_bound = d + Z * SE
    return lower_bound, upper_bound

# Example DataFrame
np.random.seed(42)  # For reproducible results

# Calculating Cohen's d
d = calculate_cohens_d(disability_df, no_disability_df)
print(f"Cohen's d: {d}")

# Calculating the confidence interval for Cohen's d
n1, n2 = len(disability_df), len(no_disability_df)
lower_bound, upper_bound = cohens_d_confidence_interval(d, n1, n2)
print(f"95% Confidence Interval for Cohen's d: [{lower_bound}, {upper_bound}]")

