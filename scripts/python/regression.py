import pandas as pd
import numpy as np
import scipy.stats as stats
from tabulate import tabulate
import statsmodels.api as sm
from pathlib import Path

# Repository root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Load the dataset files

b2020 = pd.read_csv(BASE_DIR / 'data' / 'processed' / 'disability_work_2020.csv')
b2022 = pd.read_csv(BASE_DIR / 'data' / 'processed' / 'disability_work_2022.csv')

b2020['l_other'] = np.where(b2020['other'] != 0, np.log(b2020['other']), 0)
b2022['l_other'] = np.where(b2022['other'] != 0, np.log(b2022['other']), 0)

b2020['disability'] = np.where(b2020[['dis_walk', 'dis_see', 'dis_arm', 'dis_learn', 'dis_hear',
        'dis_learn', 'dis_dress', 'dis_talk', 'dis_ment']].sum(axis=1) != 0, 1, 0)
b2022['disability'] = np.where(b2022[['dis_walk', 'dis_see', 'dis_arm', 'dis_learn', 'dis_hear',
        'dis_learn', 'dis_dress', 'dis_talk', 'dis_ment']].sum(axis=1) != 0, 1, 0)


b2020['mandatory'] = (b2020[['secondary', 'bac', 'higher']].sum(axis=1) != 0).astype(int)
b2022['mandatory'] = (b2022[['secondary', 'bac', 'higher']].sum(axis=1) != 0).astype(int)


# cols = ['dis_walk', 'dis_see', 'dis_arm', 'dis_learn', 'dis_hear',
#         'dis_learn', 'dis_dress', 'dis_talk', 'dis_ment', 'physical',
#         'sensory', 'disability', 'exp', 'married', 'female', 'isp', 
#         'cause_dis', 'age', 'health_prob', 'dis_ben']


cols = ['dis_walk', 'dis_see', 'dis_arm', 'dis_learn', 'dis_hear',
        'dis_learn', 'dis_dress', 'dis_talk', 'dis_ment', 'disability', 'exp', 'married', 'female', 'isp', 
        'age', 'health_prob', 'dis_ben']

mean2020 = b2020[cols].mean()
mean2022 = b2022[cols].mean()

t_stats, p_values = stats.ttest_ind(b2020[cols], b2022[cols])
    
summary = pd.DataFrame(
    {
     'Mean 2020': mean2020,
     'Mean 2022': mean2022,
     't-statistic': t_stats,
     'p-value': p_values
     })

print(tabulate(summary, headers = summary.columns))

cols = ['children', 'married', 'isp', 'dis_walk', 'dis_see', 'dis_arm', 
        'dis_learn', 'dis_hear', 'dis_dress', 'dis_talk', 'dis_ment', 
        'married', 'female', 'age',  'l_other', 'mandatory', 'dis_ben']

# Regression 2020
dep = b2020['work_lwk']
X = b2020[cols]
X['children'] = pd.to_numeric(X['children'], errors='coerce')
X = X.fillna(0)

modelo2020 = sm.Probit(dep, X).fit()

modelo2020.params

# Regression 2022
dep = b2022['work_lwk']
X = b2022[cols]
X['children'] = pd.to_numeric(X['children'], errors='coerce')
X = X.fillna(0)

modelo2022 = sm.Probit(dep, X).fit()

modelo2020.params

# Pooled regression
b2020['2022'] = 0
b2022['2022'] = 1
df = pd.concat([b2020, b2022], ignore_index=True)

dep = df['work_lwk']
X = df[cols + ['2022']]
X['children'] = pd.to_numeric(X['children'], errors='coerce')
X = X.fillna(0)

modelo_pooled = sm.Probit(dep, X).fit()
modelo_pooled.params
modelo_pooled.summary()

# # Pooled regression with interaction terms

col = cols + ['2022'] + ['disability']

df['disability_2022'] = df['disability'] * df['2022']

dep = df['work_lwk']
X = df[col + ['disability_2022']]
X['children'] = pd.to_numeric(X['children'], errors='coerce')
X = X.fillna(0)

modelo_pooled = sm.Probit(dep, X).fit()
modelo_pooled.params
modelo_pooled.summary()
