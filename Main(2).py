# Другая реализация парсера с использованием регуярных выражений и более красивым выводом полученных данных

import re, numpy, bs4
from requests import get
from pandas import DataFrame

l1 = []
l2 = []
l3 = []
res = [l1, l2, l3]
resSize = ''
resRate = ''

url = r"http://lib.ru/PROZA/"

try:
    response = get(url)  # загрузим веб-страницу
except:
    print("Не удалось загрузить веб-страницу")
    exit()

html = response.text
bs = bs4.BeautifulSoup(html, features="html.parser")
num = bs.find_all('small')
authors = bs.find_all('b')
df = DataFrame(columns=["Размер", "Rate", "Автор"])

# Обработка столбцов с размером и оценкой
cnt = 0
for i in num:
    b = i.find('b')
    if b != None:
        b.extract()
        cnt += 1
        if 7 < cnt < 222:
            t = i.text
            # Поиск значения в круглых скобках
            resSize = re.search(r"[^[]*\(([^]]*)\)", t)
            if resSize:
                resSize = resSize.groups()[0]
                # Обработка исключительного значения
                if resSize != '291k':
                    # Избавление от пробела '\xa0' преобразованием
                    l1.append(int(resSize))
                else:
                    l1.append(resSize)
            # Поиск значения в квадратных скобках
            resRate = re.search(r"[^[]*\[([^]]*)\]", t)
            if resRate:
                resRate = resRate.groups()[0]
                l2.append(int(resRate))
                # Избавление от пробела '\xa0' преобразованием
            else:
                l2.append(' ')

# Обработка столбца с именами авторов
cnt = 0
for j in authors:
    cnt += 1
    if 23 < cnt < 451 and (cnt % 2) == 0:
        l3.append(j.text)

# Запись в датафрейм
iDF = 1
for a in range(len(res)):
    if a != 1:
        for a1 in range(len(res[a])):
            df.loc[iDF] = res[a][a1], res[a + 1][a1], res[a + 2][a1]
            iDF += 1
    else:
        break

print(df)
