import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate
import scipy.stats as stats
import os

# Load the dataset
os.chdir("C:/Users/ediaz/OneDrive - up.edu.mx/Research/Majo Favela/Python_MMP_2020")
dw = pd.read_csv('Bases/disability_work.csv')

# Create 'cause_dis' column
dw['cause_dis'] = 0
dw.loc[dw['cause_walk'] == 1, 'cause_dis'] = 1
dw.loc[dw['cause_see'] == 1, 'cause_dis'] = 1
dw.loc[dw['cause_learn'] == 1, 'cause_dis'] = 1
dw.loc[dw['cause_hear'] == 1, 'cause_dis'] = 1
dw.loc[dw['cause_dress'] == 1, 'cause_dis'] = 1
dw.loc[dw['cause_talk'] == 1, 'cause_dis'] = 1
dw.loc[dw['cause_ment'] == 1, 'cause_dis'] = 1
dw.loc[dw['cause_arm'] == 1, 'cause_dis'] = 1

# Create additional indicators
dw['sensory'] = ((dw['dis_see'] == 1) |
                 (dw['dis_hear'] == 1) |
                 (dw['dis_talk'] == 1)).astype(int)

dw['physical'] = ((dw['dis_walk'] == 1) |
                  (dw['dis_arm'] == 1) |
                  (dw['dis_dress'] == 1)).astype(int)

# Create combined indicators
dw['sensory_physical'] = dw['sensory'] * dw['physical']
dw['sensory_mental'] = dw['sensory'] * dw['dis_ment']
dw['sensory_intel'] = dw['sensory'] * dw['dis_learn']
dw['physical_mental'] = dw['physical'] * dw['dis_ment']
dw['physical_intel'] = dw['physical'] * dw['dis_learn']

# List of disability categories
cat_columns = ['dis_walk', 'dis_see', 'dis_arm', 'dis_learn', 'dis_hear', 'dis_dress', 'dis_talk', 'dis_ment']

# Tabulate 'cause_dis' by each disability category
for var in cat_columns:
    crosstab = pd.crosstab(dw['cause_dis'], dw[var])
    print(f'Tabulation of cause_dis by {var}:')
    print(tabulate(crosstab, headers='keys'))
    print('\n')

# Define the 'disability' column
dw['disability'] = ((dw['dis_walk'] == 1) | 
                    (dw['dis_see'] == 1) | 
                    (dw['dis_arm'] == 1) | 
                    (dw['dis_learn'] == 1) | 
                    (dw['dis_hear'] == 1) | 
                    (dw['dis_dress'] == 1) | 
                    (dw['dis_talk'] == 1) | 
                    (dw['dis_ment'] == 1)).astype(int)

# Summary statistics for demographic data by disability category
for cat in cat_columns:
    subset = dw[dw[cat] == 1]
    summary = subset[['age', 'children', 'female', 'married', 'isp', 'health_prob', 
                      'less_primary', 'primary', 'secondary', 'bac', 'higher', 'help_job']].describe()
    print(f'Summary statistics for {cat} == 1:')
    print(summary)
    print('\n')

# Preserve original DataFrame before melting
dw_preserved = dw.copy()

# Melt the DataFrame
dw = dw.melt(id_vars=['folioviv', 'foliohog', 'numren'], 
              value_vars=[col for col in dw.columns if col.startswith('dis_')],
              var_name='newvar', 
              value_name='value')

# Mostrar la tabulación
print(tabulate(dw['newvar'][dw['value'] == 1].value_counts().reset_index(), headers=['Disability', 'Count']))

# Restore the original DataFrame
dw = dw_preserved

# Calculate T-Statistics and P-Values (Optimized Code)
results_df = pd.DataFrame(columns=['Variable', 'T-Statistic', 'P-Value'])
variables = ['age', 'children', 'female', 'married', 'isp', 'health_prob', 
             'less_primary', 'primary', 'secondary', 'bac', 'higher', 'help_job']

group1 = dw[dw['disability'] == 1][variables].apply(pd.to_numeric, errors='coerce')
group2 = dw[dw['disability'] == 0][variables].apply(pd.to_numeric, errors='coerce')

t_stats, p_values = stats.ttest_ind(group1, group2, nan_policy='omit')

results_df = pd.DataFrame({
    'Variable': variables,
    'T-Statistic': t_stats,
    'P-Value': p_values
})

# Print the results
print(results_df)

# Summary statistics for work outcomes by each disability category
for cat in cat_columns:
    summary = dw[dw[cat] == 1][['work_lwk', 'job_seeking', 'work_dis', 
                                'subor', 'self_emp', 'informal', 'tempo']].describe()
    print(f"\nSummary statistics for work outcomes with {cat} == 1:")
    print(summary)

# Summary statistics for work outcomes with no disability
summary_no_disability = dw[dw['disability'] == 0][['work_lwk', 'job_seeking', 'work_dis', 
                                                   'subor', 'self_emp', 'informal', 'tempo']].describe()
print("\nSummary statistics for work outcomes with no disability:")
print(summary_no_disability)

# Summary statistics excluding those with later-onset disabilities
summary_exclude_late_onset = dw[(dw['disability'] == 1) & (dw['cause_dis'] == 1)][
    ['age', 'children', 'female', 'married', 'isp', 'health_prob', 'less_primary', 'primary', 
     'secondary', 'bac', 'higher', 'help_job']].describe()
print("\nSummary statistics excluding those with later-onset disabilities:")
print(summary_exclude_late_onset)

# Understanding onsets: tabulate cause by type for each disability category
for cat in cat_columns:
    cause_summary = dw[dw[cat] == 1]['cause_dis'].value_counts()
    print(f"\nTabulate cause_dis for disability category {cat}:")
    print(cause_summary)

# Summary statistics for work income by each disability category
for cat in cat_columns:
    income_summary = dw[(dw[cat] == 1) & (dw['work_lwk'] == 1)][
        ['hours_wk', 'wage', 'work_inc', 'dis_ben', 'htrab', 'no_pay', 'no_wage']].describe()
    print(f"\nSummary statistics for work income with disability category {cat}:")
    print(income_summary)

# Summary statistics for work income with no disability
income_nodis_summary = dw[dw['disability'] == 0][['hours_wk', 'wage', 'work_inc', 'dis_ben', 'htrab', 'no_pay', 'no_wage']].describe()
print(income_nodis_summary)


# Categorizing sinco
# category_map = {
#     "2": "Professionals and technicians",
#     "3": "Auxiliary in administrative activity",
#     "4": "Commercial and sales employees",
#     "5": "Personal services and security",
#     "6": "Workers in primary sector",
#     "7": "Artisans",
#     "8": "Industrial machinery operators, assemblers, drivers",
#     "9": "Industrial low-skill workers",
#     "0": "Foreign workers"
# }

# # Extraer el primer carácter y mapearlo a las categorías
# dw['sinco'] = dw['sinco'].astype(str).str[0].map(category_map)
dw['sinco'] = (dw['sinco'].astype(str).str[0]).apply(pd.to_numeric, errors='coerce')
# dw['scian'] = dw['scian'].astype(str).apply(lambda s: pd.to_numeric(s[:2], errors='coerce') if (pd.to_numeric(s[:2], errors='coerce') >= 10) & (pd.to_numeric(s[:2], errors='coerce') <= 10) else pd.to_numeric(s[:1], errors='coerce'))


# Preserve the original DataFrame
dw_preserved = dw.copy()

# Filter the DataFrame for ages between 20 and 50
dw = dw[(dw['age'] > 20) & (dw['age'] < 50)]

# T-test for 'exp' by disability status
# Check if 'exp' and 'disability' columns exist in the DataFrame
if 'exp' in dw.columns and 'disability' in dw.columns:
    group1 = dw[dw['disability'] == 1]['exp'].dropna()
    group2 = dw[dw['disability'] == 0]['exp'].dropna()

    t_stat, p_value = stats.ttest_ind(group1, group2, nan_policy='omit')
    print(f'T-test results: T-Statistic = {t_stat}, P-Value = {p_value}')

    # Histogram of 'exp' by disability status
    plt.figure(figsize=(12, 6))
    sns.histplot(data=dw, x='exp', hue='disability')
    plt.title('Histogram of exp by Disability Status')
    plt.xlabel('exp')
    plt.ylabel('Frequency')
    plt.show()
else:
    print("'exp' or 'disability' column is missing from the DataFrame.")

# Restore the original DataFrame
dw = dw_preserved

# Create and replace the education variable
dw['educ'] = np.where(dw['illiterate'] == 1, 0,
                      np.where(dw['less_primary'] == 1, 0,
                               np.where(dw['primary'] == 1, 6,
                                        np.where(dw['secondary'] == 1, 9,
                                                 np.where(dw['bac'] == 1, 12,
                                                          np.where(dw['higher'] == 1, 15, np.nan))))))

# Display the first few rows to verify
print(dw[['illiterate', 'less_primary', 'primary', 'secondary', 'bac', 'higher', 'educ']].head())

dw.to_csv('Bases/disability_work_edit.csv')
