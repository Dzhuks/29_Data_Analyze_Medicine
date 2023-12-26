import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sbn
from scipy import stats
import warnings

warnings.filterwarnings('ignore')


def check_normality(data):
    _, p_value_normality = stats.shapiro(data)
    if p_value_normality < 0.05:
        print("Данные распределены нормально")
    else:
        print("Данные распределены ненормально")


def check_hypothesis(group1, group2, method) -> None:
    if method == "Хи-квадрат":
        contigency_table = pd.crosstab(group1, group2)
        chi2 = stats.chi2_contingency(contigency_table)
        cor, pvalue = chi2.statistic, chi2.pvalue
    elif method == "Т-критерий Стьюдента":
        cor, pvalue = stats.ttest_ind(group1, group2, equal_var=False)
    elif method == "U-критерий Манна-Уитни":
        cor, pvalue = stats.mannwhitneyu(group1, group2)
    elif method == 'Спирмен':
        r = stats.spearmanr(group1, group2)
        cor, pvalue = r.statistic, r.pvalue
    cor = round(cor, 2)
    pvalue = round(pvalue, 4)
    print(f"корреляция={cor}, p-уровень={pvalue}")
    if pvalue < 0.05:
        print("Отвергнуть нулевую гипотезу")
    else:
        print("Мы не можем отвергнуть нулевую гипотезу")


df = pd.read_csv('../content/processed_data.csv', skipinitialspace=True, decimal=',', sep=',')

# Гипотеза №1 - Между возрастом пациента и длительностью операции существует зависимость
data = df[['возраст', 'длительность_операции']]
data['возраст'] = data['возраст'].astype(int)
data['длительность_операции'] = data['длительность_операции'].astype(float)
check_normality(data['возраст'])
check_normality(data['длительность_операции'])
check_hypothesis(data['возраст'], data['длительность_операции'], 'Спирмен')
'''При таком уровне значимости можно сделать вывод, что нету корреляции между фактором возрастом и риском развития ОПП'''


# Гипотеза №2 - Наличие хронической сердечной недостаточности влияют на риск развития ОПП
print('\n\n')
data = df[['хсн', 'развитие_опп']]
data['хсн'] = data['хсн'].astype(int)
data['развитие_опп'] = data['развитие_опп'].apply(lambda x: 1 if x == 'есть' else 0)
check_normality(data['хсн'])
check_normality(data['развитие_опп'])
check_hypothesis(data['хсн'], data['развитие_опп'], method='Т-критерий Стьюдента')
# sbn.boxplot(x='хсн', hue='развитие_опп', data=data)
# plt.show()

crosstab = pd.crosstab(index=data["развитие_опп"], columns=data["хсн"])
crosstab.plot.bar(rot=0)

''''''

# Гипотеза №3 - Есть корреляция между индексом массы тела и наличием опп
print('\n\n')
data = df[['развитие_опп', 'имт']]
data['развитие_опп'] = data['развитие_опп'].apply(lambda x: 1 if x == 'есть' else 0)
data['имт'] = data['имт'].astype(float)
check_normality(data['развитие_опп'])
check_normality(data['имт'])
check_hypothesis(data['имт'], data['развитие_опп'], method='Т-критерий Стьюдента')
sbn.boxplot(data=data, x='имт', hue='развитие_опп')
plt.show()


