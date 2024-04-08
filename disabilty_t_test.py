from scipy import stats
import os
import pandas as pd


data_filepath = os.path.join(os.getcwd(), 'NSS23_characteristic_workbook.xlsx')

full_df = pd.read_excel(data_filepath, sheet_name=4, skiprows=2)

# filter full_df to try make it run faster
df = full_df[['Split', 'Positvity measure (%)']].copy()

disability_df = pd.Series(df[df['Split'] == "Disability reported"]['Positvity measure (%)']).copy()
no_disability_df = pd.Series(df[df['Split'] == "No disability reported"]['Positvity measure (%)']).copy()

# # Take a sample of 10,000 from each dataframe
# sample_disability_df = disability_df.sample(n=500, random_state=42)
# sample_no_disability_df = no_disability_df.sample(n=500, random_state=42)

t_statistic, p_value = stats.ttest_ind(disability_df, no_disability_df, equal_var=True)

# Print the results
print("t-statistic:", t_statistic)
print("p-value:", p_value)



