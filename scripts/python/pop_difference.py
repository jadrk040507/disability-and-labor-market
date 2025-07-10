import pandas as pd
import scipy.stats as stats
from tabulate import tabulate
from pathlib import Path

# Repository root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Load the datasets from each year

b2020 = pd.read_csv(BASE_DIR / 'data' / 'processed' / 'disability_work_edit_2020.csv')
b2022 = pd.read_csv(BASE_DIR / 'data' / 'processed' / 'disability_work_edit_2022.csv')

cols = ['dis_walk', 'dis_see', 'dis_arm', 'dis_learn', 'dis_hear',
        'dis_learn', 'dis_dress', 'dis_talk', 'dis_ment', 'physical',
        'sensory', 'disability', 'exp', 'married', 'female', 'isp', 
        'cause_dis', 'age', 'health_prob', 'work_lwk', 'less_primary', 
        'primary', 'secondary', 'bac', 'higher', 'htrab',
        'leg_ben', 'extra_ben']

# "['mandatory', 'benefit', 'l_other'] not in index"


mean2020 = b2020[cols].mean()
mean2022 = b2022[cols].mean()

tstat, pvalue = stats.ttest_ind(b2020[cols], b2022[cols], nan_policy='omit')
    
summary = pd.DataFrame(
    {
     'Mean 2020': mean2020,
     'Mean 2022': mean2022,
     't-statistic': tstat,
     'p-value': pvalue
     })

print(tabulate(summary, headers = summary.columns))


# Test for sinco

b2020_preserved = b2020.copy()
b2022_preserved = b2022.copy()

b2020 = b2020.melt(id_vars=['folioviv', 'foliohog', 'numren'], 
                          value_vars='sinco',
                          value_name='sinco_value')
b2020 = b2020.pivot_table(index=['folioviv', 'foliohog', 'numren'], 
                                         columns='sinco_value', 
                                         aggfunc=lambda x: 1,
                                         fill_value=0).loc[:, 'variable']

b2022 = b2022.melt(id_vars=['folioviv', 'foliohog', 'numren'], 
                          value_vars='sinco',
                          value_name='sinco_value')
b2022 = b2022.pivot_table(index=['folioviv', 'foliohog', 'numren'], 
                                         columns='sinco_value', 
                                         aggfunc=lambda x: 1,
                                         fill_value=0).loc[:, 'variable']

b2020.columns = [f'sinco_{i}' for i in range(1, 10)]
b2022.columns = [f'sinco_{i}' for i in range(1, 10)]

mean2020 = b2020.mean()
mean2022 = b2022.mean()

tstats, pvalues = stats.ttest_ind(b2020[1:], b2022[1:], nan_policy='omit')

sinco = pd.DataFrame({
    'Mean 2020': mean2020,
    'Mean 2022': mean2022,
    't-statistic': tstats,
    'p-value': pvalues
}, index=b2020.columns)

summary = pd.concat([summary, sinco])

# Return to original DataFrame

b2020 = b2020_preserved
b2022 = b2022_preserved


# # Test for scian
# I don't know the classification for scian used
# b2020 = b2020.melt(id_vars=['folioviv', 'foliohog', 'numren'], 
#                           value_vars='scian',
#                           value_name='scian_value')

# b2020 = b2020.pivot_table(index=['folioviv', 'foliohog', 'numren'], 
#                                          columns='scian_value', 
#                                          aggfunc=lambda x: 1,
#                                          fill_value=0).loc[:, 'variable']

# b2022 = b2022.melt(id_vars=['folioviv', 'foliohog', 'numren'], 
#                           value_vars='scian',
#                           value_name='scian_value')

# b2022 = b2022.pivot_table(index=['folioviv', 'foliohog', 'numren'], 
#                                          columns='scian_value', 
#                                          aggfunc=lambda x: 1,
#                                          fill_value=0).loc[:, 'variable']


# b2020.columns = [f'scian{i}' for i in range(1, 11)]
# b2022.columns = [f'scian{i}' for i in range(1, 11)]

# mean2020 = b2020.mean()
# mean2022 = b2022.mean()

# tstats, pvalues = stats.ttest_ind(b2020[1:], b2022[1:], nan_policy='omit')

# scian = pd.DataFrame({
#     'Mean 2020': mean2020,
#     'Mean 2022': mean2022,
#     't-statistic': tstats,
#     'p-value': pvalues
# }, index=b2020.columns)

# summary = pd.concat([summary, scian])

# b2020 = b2020_preserved
# b2022 = b2022_preserved

# Return to original DataFrame


print(tabulate(summary))
