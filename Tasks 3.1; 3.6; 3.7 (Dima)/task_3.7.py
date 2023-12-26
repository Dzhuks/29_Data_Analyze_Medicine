# ЗАДАНИЕ 3.7

import pandas as pd
from scipy.stats import pearsonr, spearmanr, mannwhitneyu, chi2_contingency, shapiro


def chi2_counting(first_cat, second_cat):
    # функция для подсчёта корреляции номинальных данных с номинальными

    temp_table = pd.crosstab(data[first_cat], data[second_cat])
    chi_2 = chi2_contingency(temp_table)
    return chi_2.statistic, chi_2.pvalue


def mannwhitneyu_counting(first_cat, second_cat):
    # функция для подсчёта корреляции количественных данных с номинальными

    mn = mannwhitneyu(first_cat, second_cat)
    cor, p_value = mn.statistic, mn.pvalue
    return cor, p_value


def pearsonr_counting(first_cat, second_cat):
    # функция для подсчёта корреляции количественных данных с количественными (с нормальным распределением данных)

    pr = pearsonr(first_cat, second_cat)
    cor, p_value = pr.statistic, pr.pvalue
    return cor, p_value


def spearmanr_counting(first_cat, second_cat):
    # функция для подсчёта корреляции количественных данных с количественными (с ненормальным распределением данных)

    sp = spearmanr(first_cat, second_cat)
    cor, p_value = sp.statistic, sp.pvalue
    return cor, p_value


data = pd.read_csv('../content/processed_data.csv', skipinitialspace=True)
data.columns = [i.replace(' ', '_').lower() for i in data.columns]
nominal = ['развитие_опп', 'пол', 'гб', 'сахарный_диабет', 'стенокардия', 'инфаркт_миокарда', 'мерцательная_аритмия',
           'желудочковая_экстрасистолия', 'а-в_блокада', 'блокада_ножек_пучка_гиса', 'хсн', 'нк', 'ар', 'аик', 'хбп']

answer = list()

for first_cat in data.columns:
    for second_cat in data.columns:
        if first_cat != second_cat:
            g1 = data[first_cat]
            g2 = data[second_cat]
            if first_cat in nominal and second_cat in nominal:
                # высчитывание корреляции для номинальные-номинальные
                cor, p_value = chi2_counting(first_cat, second_cat)
                answer.append([first_cat, second_cat, round(cor, 2), round(p_value, 3)])
            elif first_cat in nominal and second_cat not in nominal or first_cat not in nominal and second_cat in nominal:
                # высчитывание корреляции для количественные-номинальные
                try:
                    cor, p_value = mannwhitneyu_counting(g1, g2)
                    answer.append([first_cat, second_cat, round(cor, 2), round(p_value, 3)])
                except TypeError:
                    pass
            else:
                # высчитывание корреляции для количественные-количественные
                if shapiro(g1).pvalue >= 0.05 and shapiro(g2).pvalue >= 0.05:
                    # Данные распределены нормально
                    cor, p_value = pearsonr_counting(g1, g2)
                    answer.append([first_cat, second_cat, round(cor, 2), round(p_value, 3)])
                else:
                    # Данные распределены ненормально
                    cor, p_value = spearmanr_counting(g1, g2)
                    answer.append([first_cat, second_cat, round(cor, 2), round(p_value, 3)])

# фильтруем данные
new_answer = list()
for result in answer:
    if result[-2] != 0 and -1 <= result[-2] <= 1 and result[-1] <= 0.05 and result[-1] != 0:

        new_answer.append(result)

answer_df = pd.DataFrame(data=sorted(new_answer, key=lambda x: x[-2], reverse=True),
                         columns=['Показатель №1', 'Показатель №2', 'Значение корреляции', 'p-уровень'])

print(answer_df.head(10))
