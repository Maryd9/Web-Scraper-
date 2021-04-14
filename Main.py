import bs4
from requests import get
from pandas import DataFrame

# Нужный нам сайт
url = r"http://lib.ru/PROZA/"

try:
    # Получаем данные с сайта
    response = get(url)
except:
    print("Не удалось загрузить веб-страницу")
    exit()
# Запись полученного результата в переменную
html = response.text
# Преобразуем и найдем основной тэг, где лежат данные
bs = bs4.BeautifulSoup(html, features="html.parser")
li = bs.find_all("li")
# Создаем табличку, куда будем складывать полученные данные
df = DataFrame(columns=["Размер", "Автор"])

# Запись будет производится с первой строчки
i = 1
j = 1
# Извлечение нужных данных и сразу запись в датафрейм
for l in li:
    if 6 < i < 221:
        size = l.find("small")
        b = size.find("b")
        if b != None:
            b.decompose()
        size = l.find_all("small")[0].get_text()
        author = l.find_all("b")[0].get_text()
        df.loc[j] = size, author
        j += 1
    i += 1
df = df.to_string()
# Выводим то, что получилось
print(df)

