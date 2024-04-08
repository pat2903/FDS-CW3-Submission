import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_excel('NSS23_characteristic_workbook.xlsx', sheet_name=4, skiprows=2)

# list of themes
themes = [
    "Theme 1: Teaching on my course",
    "Theme 2: Learning opportunities",
    "Theme 3: Assessment and feedback",
    "Theme 4: Academic support",
    "Theme 5: Organisation and management",
    "Theme 6: Learning resources",
    "Theme 7: Student voice"
]

theme_labels = ["Teaching",
    "Learning \nopportunities",
    "Assessment \n& feedback",
    "Academic \nsupport",
    "Organisation \n& management",
    "Learning \nresources",
    "Student \nvoice"]

disability_means = []
no_disability_means = []
differences_in_mean = []

for theme in themes:
    disability_means.append(df[(df['Split'] == "Disability reported") & (df['Question Number'] == theme)]['Positvity measure (%)'].mean())
    no_disability_means.append(df[(df['Split'] == "No disability reported") & (df['Question Number'] == theme)]['Positvity measure (%)'].mean())

for i, theme in enumerate(themes):
    print(theme + ": " + str(disability_means[i] - no_disability_means[i]))

data = pd.DataFrame({
    'Theme': theme_labels,
    'Disability': disability_means,
    'No Disability': no_disability_means
})

# melt the df to long format
data_melted = pd.melt(data, id_vars='Theme', var_name='Disability Status', value_name='Positivity Measure (%)')

# plotting with Seaborn
plt.figure(figsize=(10,8))
sns.barplot(data=data_melted, x='Theme', y='Positivity Measure (%)', hue='Disability Status')
sns.set_style("whitegrid")
plt.grid(axis='y', alpha=0.5, linewidth=0.5, which='both', linestyle='-.')
plt.xlabel('Theme', fontsize=15)
plt.ylabel('Positivity Measure (%)', fontsize=15)
plt.title('Positivity Measure by Themes for Disability and No Disability', fontsize=15)
plt.legend(title='Disability Status', fontsize=12, title_fontsize=12)
plt.yticks(range(0, 101, 5), fontsize=12)
plt.xticks(fontsize=12)

plt.tight_layout()
plt.show()