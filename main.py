import requests
from bs4 import BeautifulSoup


def main():
    links = []    # массив ссылок
    url = 'https://dungeon.su/bestiary/'  # URL главное страницы

    # получение главной страницы
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    # поиск всех нужных элементов li на главноей странице
    ul = soup.find('ul', {'class': 'list-of-items col4 double'})
    a = ul.select('a[href^="/bestiary/"]')

    # заполнение массива ссылок
    for i in a:
        links.append(i['href'])

    # парсинг каждой ссылки из массива ссылок
    for link in links:
        link_parser(link)


# парсер самих страниц с чудовищами
def link_parser(link):
    name = ''
    abilities = ''
    actions = ''
    description = ''

    link = 'https://dungeon.su' + link
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    name = soup.find('a', {'class': 'item-link'}).get_text()
    ul = soup.find('ul', {'class': 'params'})
    for li in ul:
        li = soup.find('li', {'class': 'subsection'})
        print(li.get_text())

main()
