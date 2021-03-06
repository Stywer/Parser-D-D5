import requests
from bs4 import BeautifulSoup
import pandas as pd


def main():
    result = pd.DataFrame()

    links = []    # список ссылок
    url = 'https://dungeon.su/bestiary/'  # URL главное страницы

    # получение главной страницы
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    # поиск всех нужных элементов li на главноей странице
    ul = soup.find('ul', {'class': 'list-of-items col4 double'})
    a = ul.select('a[href^="/bestiary/"]')

    # заполнение списка ссылок
    for i in a:
        links.append(i['href'])

    # парсинг каждой ссылки из списка ссылок
    for link in links:
        res = link_parser(link)
        result = result.append(res, ignore_index=True)
    # выгрузка в excel
    with pd.ExcelWriter('result.xlsx') as writer:
        result.to_excel(writer, sheet_name='Sheet1')


# парсер самих страниц с чудовищами
def link_parser(link):
    # Все характеристики монстра
    name = ''
    characteristic = ''
    armor_class = ''
    hits = ''
    speed = ''
    strength = ''
    ability = ''
    physique = ''
    intellect = ''
    wisdom = ''
    charisma = ''
    damage_immunity = ''
    skills = ''
    feeling = ''
    languages = ''
    danger = ''
    abilities = ''
    is_player = ''
    actions = ''
    description = ''

    res = pd.DataFrame()

    # Обработка страницы
    link = 'https://dungeon.su' + link
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    name = soup.find('a', {'class': 'item-link'}).get_text()
    ul = soup.find('ul', {'class': 'params'})

    stats_list = stats(link)  # список статусов

    li = ul.select('li', limit=20)
    # print(name)
    for item in li:
        if "Класс доспеха:" in item.get_text():
            armor_class = item.get_text()[14: len(item.get_text())]
            # print(armor_class)
        if "Хиты:" in item.get_text():
            hits = item.get_text()[5: len(item.get_text())]
            # print(hits)
        if "Скорость:" in item.get_text():
            speed = item.get_text()[9: len(item.get_text())]
            # print(speed)
        if "Навыки:" in item.get_text():
            skills = item.get_text()[7: len(item.get_text())]
            # print(skills)
        if "Чувства:" in item.get_text():
            feeling = item.get_text()[8: len(item.get_text())]
            # print(feeling)
            """
            Тут твориться какая-то дичь. В item пропадает закрывающий тег </li> у языков, 
            поэтому парсится вообще весь текст со страницы
             
        if "Языки:" in item.get_text():
            languages = item.get_text()
            print(languages)
            """

        if "Опасность:" in item.get_text():
            danger = item.get_text()[10: len(item.get_text())]
            # print(danger)
        else:
            continue

    strength = stats_list[0]
    ability = stats_list[1]
    physique = stats_list[2]
    intellect = stats_list[3]
    wisdom = stats_list[4]
    charisma = stats_list[5]

    # Пришлось все, что ниже поля "Опасность" парсить отдельно, потому что, как я писал выше, пропадет тег </li>
    li = soup.find_all('li', {'class': 'subsection'}, limit=4)
    for item in li:
        if "Способности" in item.get_text():
            abilities = item.get_text()[11: len(item.get_text())]
            # print(abilities)
        if "Игровой персонаж" in item.get_text():
            is_player = item.get_text()[16: len(item.get_text())]
            # print(is_player)
        if "Действия" in item.get_text():
            actions = item.get_text()[8: len(item.get_text())]
            # print(actions)
        if "Описание" in item.get_text():
            if "См. дополнительно статью:" in item.get_text():
                continue
            description = item.get_text()[8: len(item.get_text())]
            # print(description)
    # Формирование таблиц в excel
    res = res.append(pd.DataFrame([[name, armor_class, hits, speed, strength, ability,
                                    physique, intellect, wisdom, charisma, skills, feeling,
                                    danger, abilities, is_player, actions, description]],
                                  columns=['name', 'armor_class', 'hits', 'speed', 'strength', 'ability',
                                           'physique', 'intellect', 'wisdom', 'charisma', 'skills', 'feeling',
                                           'danger', 'abilities', 'is_player', 'actions', 'description']),
                     ignore_index=True)
    # print("----")
    return res


# Заполнение списка статусов
def stats(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    stats_list = list(range(6))
    stats_list[0] = soup.find('div', {'title': 'Сила'}).get_text()[3:len(soup.find('div', {'title': 'Сила'}).get_text())]
    stats_list[1] = soup.find('div', {'title': 'Ловкость'}).get_text()[3:len(soup.find('div', {'title': 'Ловкость'}).get_text())]
    stats_list[2] = soup.find('div', {'title': 'Телосложение'}).get_text()[3:len(soup.find('div', {'title': 'Телосложение'}).get_text())]
    stats_list[3] = soup.find('div', {'title': 'Интеллект'}).get_text()[3:len(soup.find('div', {'title': 'Интеллект'}).get_text())]
    stats_list[4] = soup.find('div', {'title': 'Мудрость'}).get_text()[3:len(soup.find('div', {'title': 'Мудрость'}).get_text())]
    stats_list[5] = soup.find('div', {'title': 'Харизма'}).get_text()[3:len(soup.find('div', {'title': 'Харизма'}).get_text())]
    return stats_list


main()
