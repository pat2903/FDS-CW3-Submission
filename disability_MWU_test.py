import pandas as pd
import os
from scipy.stats import mannwhitneyu

data_filepath = os.path.join(os.getcwd(), 'NSS23_characteristic_workbook.xlsx')

full_df = pd.read_excel(data_filepath, sheet_name=4, skiprows=2)

# filter full_df to try make it run faster
df = full_df[['Split', 'Positvity measure (%)']].copy()


disability_df = df[df['Split'] == "Disability reported"]['Positvity measure (%)'].copy()
no_disability_df = df[df['Split'] == "No disability reported"]['Positvity measure (%)'].copy()


# Perform the Mann-Whitney U test
stat, p = mannwhitneyu(disability_df, no_disability_df)

print(f'Statistics={stat}, p={p}')

# Interpret the results
alpha = 0.05
if p > alpha:
    print('Same distribution (fail to reject H0)')
else:
    print('Different distribution (reject H0)')