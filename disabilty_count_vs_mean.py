import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

df = pd.read_excel('NSS23_characteristic_workbook.xlsx', sheet_name=5, skiprows=2)

# Strip common prefix from x-axis titles
df['Split'] = df['Split'].str.replace('The student has a mental health condition',
                                            'Mental Health',
                                      regex=False)
df['Split'] = df['Split'].str.replace('The student has a sensory, medical or physical impairment',
                                            'Sensory/ Medical/ Physical',
                                      regex=False)
df['Split'] = df['Split'].str.replace('The student has a social or communication impairment',
                                            'Social/ Communication',
                                      regex=False)
df['Split'] = df['Split'].str.replace('The student has cognitive or learning difficulties',
                                            'Cognitive/ Learning',
                                      regex=False)
df['Split'] = df['Split'].str.replace('The student has multiple or other impairments',
                                            'Multiple/ Other',
                                      regex=False)

df = df[df['Split'] != 'The student has no disability reported or an unknown disability type'].copy()

average_positivity = df.groupby('Split')['Positvity measure (%)'].mean().reset_index()
group_count = df['Split'].value_counts().reset_index()
group_count.columns = ['Split', 'Count']

# Merge mean data with count data
group_data = pd.merge(group_count, average_positivity, on='Split')

# Calculate Pearson correlation coefficient
correlation_coefficient, p_value = pearsonr(group_data['Count'], group_data['Positvity measure (%)'])

print("Correlation coefficient:", correlation_coefficient)
print("P-value:", p_value)

plt.figure(figsize=(10, 6))

# Plot the scatter plot
plt.scatter(group_data['Count']/1000, group_data['Positvity measure (%)'])
plt.xlabel('Count (thousands)', fontsize=15)
plt.ylabel('Mean Positivity Measure (%)', fontsize=15)
plt.title('Count vs. Mean Positivity Measure (%) by Disability Type', fontsize=17)

# Annotate each point with the disability type
for i, txt in enumerate(group_data['Split']):
    plt.annotate(txt, (group_data['Count'][i]/1000, group_data['Positvity measure (%)'][i]), fontsize=12)

plt.grid(True)
plt.tight_layout()
plt.show()
