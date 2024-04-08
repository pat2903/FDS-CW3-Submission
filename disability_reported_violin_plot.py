import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

df_uk = pd.read_excel('NSS23_characteristic_workbook.xlsx', sheet_name=4, skiprows=2)

average_positivity = df_uk.groupby('Split')['Positvity measure (%)'].mean().reset_index()

plt.figure(figsize=(10, 6))

for y in range(0, 101, 10):
    plt.axhline(y=y, color='grey', linestyle='--', linewidth=0.5)

sns.violinplot(data=df_uk, x='Split', y='Positvity measure (%)')
plt.xticks(rotation=0)
plt.yticks(np.arange(0, 101, 10))
plt.ylim(0, 100)
plt.title('Positivity Measure (%) Distribution by Disability Reported', fontsize=15)
plt.ylabel('Positivity Measure (%)', fontsize=15)
plt.xlabel('')
plt.tick_params(axis='both', labelsize=12)

plt.show()


