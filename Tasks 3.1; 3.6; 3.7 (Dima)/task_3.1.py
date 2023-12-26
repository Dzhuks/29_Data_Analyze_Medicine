# ЗАДАНИЕ 3.1

import pandas as pd
import numpy as np
import warnings


def count_percentage(category: str, temp_df: pd.DataFrame):
    '''
        category - название колонки, процент которой будет вычисляться
        temp_df - временный датасет только с двумся колонками: развитие_опп, одина из ['сахарный_диабет', 'гб', 'наличие_хбп']
    '''

    # преобразование датасета, чтобы остались только те, у кого есть хроническое заболевание
    temp_df[category] = temp_df[category].apply(lambda x: 1 if x == 1 else np.NaN)
    temp_df = temp_df.dropna(axis=0)

    # подсчёт количества пациентов, которые имеют/не имеют ОПП
    data = temp_df.groupby(['развитие_опп']).agg({category: 'count'})

    # высчитывание процента пациентов, которые имеют/не имеют ОПП
    answer = [category]
    summ = sum(list(data[category]))
    for en, j in enumerate(data[category]):
        answer.append(f'{list(data[category].index)[en]} ОПП - {round(j / summ * 100, 2)}%')

    '''
        возвращаем список, который содержит следующую информацию: 
        answer[0] - название хронической болезни
        answer[1] - процент пациентов, которые болеют хронически и имеют ОПП
        answer[2] - процент пациентов, которые болеют хронически, но не имеют ОПП
    '''
    return answer


warnings.filterwarnings('ignore')

# загрузка и предобработка данных
df = pd.read_csv('../content/processed_data.csv', skipinitialspace=True, sep=',')
df.columns = [i.replace(' ', '_').lower() for i in df.columns]

# создание новой колонки с бинарным типом данных
df['наличие_хбп'] = df['хбп'].apply(lambda x: 0 if x == 'Пациенты без ХБП' else 1)

# цикл по всем необходимым хроническим болезням
for categ in ['сахарный_диабет', 'гб', 'наличие_хбп']:
    print(*count_percentage(categ, df[[categ, 'развитие_опп']]))
