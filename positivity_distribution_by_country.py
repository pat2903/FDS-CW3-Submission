import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

# we only want the countries
df = pd.read_excel('NSS23_Summary_Registered_Full-time.xlsx', sheet_name=2, skiprows=3)
countries = ['England', 'Scotland', 'Wales', 'Northern Ireland']
df = df[df['Provider name'].isin(countries)]
df = df[df['Level of study'].str.startswith('All undergraduates')]

plt.figure(figsize=(12, 8))  

df_agg = df.groupby(['Provider name', 'Question'], as_index=False)['Positivity measure (%)'].mean().reset_index()

sns.boxplot(data=df_agg, x='Provider name', y='Positivity measure (%)', hue='Provider name')

plt.yticks(fontsize=16) 

plt.yticks(np.arange(0, 110, 10))
plt.xticks(fontsize=16)

plt.title('Positivity Measure Distribution by Country', fontsize=20)
plt.tight_layout()  
plt.xlabel('Constituent Country', fontsize=18)
plt.ylabel('Positivity measure (%)', fontsize=18)

plt.ylim(0, 100) 
plt.grid(axis='y', linestyle='--', linewidth=0.5, color='gray')  # Adding grid lines for better readability

plt.show()