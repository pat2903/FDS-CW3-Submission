import pandas as pd

import seaborn as sns
import numpy as np
from typing import final
import matplotlib.pyplot as plt

df_uk = pd.read_excel('NSS23_characteristic_workbook.xlsx', sheet_name=5, skiprows=2)

# Strip common prefix from x-axis titles
df_uk['Split'] = df_uk['Split'].str.replace('The student has a mental health condition',
                                            'Mental Health',
                                            regex=False)
df_uk['Split'] = df_uk['Split'].str.replace('The student has a sensory, medical or physical impairment',
                                            'Sensory/\nMedical/\nPhysical',
                                            regex=False)
df_uk['Split'] = df_uk['Split'].str.replace('The student has a social or communication impairment',
                                            'Social/\nCommunication',
                                            regex=False)
df_uk['Split'] = df_uk['Split'].str.replace('The student has cognitive or learning difficulties',
                                            'Cognitive/\nLearning',
                                            regex=False)
df_uk['Split'] = df_uk['Split'].str.replace('The student has multiple or other impairments',
                                            'Multiple/\nOther',
                                            regex=False)
df_uk['Split'] = df_uk['Split'].str.replace('The student has no disability reported or an unknown disability type',
                                            'No Disability/\nUnknown',
                                            regex=False)

print(df_uk['Split'].unique())

average_positivity = df_uk.groupby('Split')['Positvity measure (%)'].mean().reset_index()

group_statistics = df_uk.groupby('Split')['Positvity measure (%)'].describe()
print(group_statistics.to_string(columns=None))

plt.figure(figsize=(12, 8))

for y in range(0, 101, 10):
    plt.axhline(y=y, color='grey', linestyle='--', linewidth=0.5)

sns.boxplot(data=df_uk, x='Split', y='Positvity measure (%)', showfliers=False)
plt.yticks(np.arange(0, 101, 10), fontsize=15)
plt.ylim(0, 100)
plt.title('Positivity Measure (%) Distribution by Disability Type', fontsize=17)
plt.xlabel('Disability Type', fontsize=17)
plt.ylabel('Positivity Measure (%)', fontsize=17)
plt.tick_params(axis='both', labelsize=15)

plt.tight_layout()
plt.show()


