# ЗАДАНИЕ 3.6
import pandas as pd


def make_prediction_to_diagnosis(skf):
    # устанавливаем стадию хбп у пациента
    if g1[0] <= skf <= g1[1]:
        return 'Стадия C1-C2'
    elif g2[1] < skf < g1[0]:
        return 'Стадия C1-С2'
    elif skf <= g2[1]:
        return 'Стадия C3'
    return 'Пациенты без ХБП'


def check_diagnosis(cols):
    # проверяем адекватность поставлxенного диагноза
    vals = cols.values
    if vals[0] == vals[1]:
        return 'Диагноз поставлен правильно'
    return 'Диагноз возможно поставлен некорректно'


# Загружаем и делаем предобработку данных
# скф_расч., 90-120 (параметр, по которому определяется стадия хбп)
df = pd.read_csv('../content/processed_data.csv', skipinitialspace=True, decimal=',', sep=',')
df.columns = [i.replace(' ', '_').lower() for i in df.columns]

data = df[['развитие_опп', 'хбп', 'скф_расч']]
data['скф_расч'] = data['скф_расч'].astype(float)
# удаляем всех пациентов у которых нет опп
data = data[(data['развитие_опп'] == 'есть')]

# узнаем примерные рамки параметра скф по поставленной стадии
d = round(data.groupby(['хбп']).agg({'скф_расч': 'describe'})['скф_расч'], 2)
twenty_five = d['25%'].values
mean = d['mean'].values
seventy_five = d['75%'].values

g1 = [twenty_five[0], seventy_five[0]]
g2 = [twenty_five[1], seventy_five[1]]

# делаем колонку предположительного диагноза
data['предположительный_диагноз'] = data['скф_расч'].apply(lambda x: make_prediction_to_diagnosis(x))
# сравниваем колонку преположительного диагноза и хбп.
# Если диагноз подтверждается: Диагноз поставлен правильно
# Иначе: Диагноз возможно поставлен некорректно
data['адекватность_диагноза'] = data[['предположительный_диагноз', 'хбп']].apply(lambda x: check_diagnosis(x), axis=1)

print(data[['адекватность_диагноза', 'хбп', 'предположительный_диагноз']])
