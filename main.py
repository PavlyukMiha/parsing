import random
from selenium.webdriver.common.by import By
from time import sleep

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import  csv
import re

CSV = 'kino.csv'
URL = 'https://www.kinopoisk.ru/top/navigator/m_act[egenre]/456%2C20%2C12%2C27%2C1747%2C15%2C9%2C28%2C25%2C26%2C1751/m_act[ecountry]/13%2C13/m_act[num_vote]/1980/m_act[is_film]/on/order/box/page/1/#results'
HEADERS = {
    'accept': 'ext/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
}

# with open('c.html', encoding='utf-8') as file:
#     src = file.read()

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    silki_l = []
    silki_d = []
    items = soup.find_all('div', class_ = 'item _NO_HIGHLIGHT_')

    for i in items:
        if i.find('a', class_ = 'movie-online-button movie-online-button_on_list-item js-ott-widget__button js-ott-widget__button_orange') != None or i.find('a', class_ = 'movie-online-button movie-online-button_on_list-item js-ott-widget__button js-ott-widget__button_blue js-ott-widget__button_svod'):
            silki_l.append({
                i.find('div', class_ = 'name').find('a').get('href')
            })


    for i in items:
        if i.find('a', class_ = 'movie-online-button movie-online-button_on_list-item js-ott-widget__button js-ott-widget__button_orange') == None and i.find('a', class_ = 'movie-online-button movie-online-button_on_list-item js-ott-widget__button js-ott-widget__button_blue js-ott-widget__button_svod') == None:
            silki_d.append({
                i.find('div', class_ = 'name').find('a').get('href')
            })


    return silki_d, silki_l

def get_content_l(html):
    soup = BeautifulSoup(html, 'html.parser')
    nam = []
    nam.append(
        {
            'title': soup.find('span', class_='styles_title__2l0HH').get_text(),
            'ocenka_kin': soup.find('span', class_='styles_value__3qmcr').get_text(),
            'ocenka_imdb': soup.find('span', class_='styles_valueSection__19woS').get_text(),
            'kol-vo_imdb': soup.find('span', class_='styles_count__gelnz').get_text(),
            'kol-vo_kin': soup.find('span', class_='styles_count__3hSWL').get_text(),
            'kinokrit_mir': soup.find_all('span', class_='styles_value__3qmcr')[2].get_text(),
            'god': soup.find('a', class_='styles_linkLight__1Nxon styles_link__1N3S2').get_text(),
            'strana': soup.find_all('div', class_='styles_rowLight__3uy9z styles_row__2ee6F')[1].get_text().rpartition('Страна')[2],
            'ganr': soup.find_all('div', class_='styles_rowLight__3uy9z styles_row__2ee6F')[2].get_text().rpartition('Жанр')[2].rpartition('слова')[0],
            'akt': ', '.join([ ' '.join(re.sub(r"(\w)([А-Я])", r"\1 \2", soup.find('ul', class_='styles_list__I97eu').get_text()).split()[::][i:i+2])[::] for i in range(0,len(re.sub(r"(\w)([А-Я])", r"\1 \2", soup.find('ul', class_='styles_list__I97eu').get_text()).split()),2)][::]),
            'resisor': soup.find_all('div', class_='styles_rowLight__3uy9z styles_row__2ee6F')[4].get_text().rpartition('Режиссер')[2],
            'scenariy': soup.find_all('div', class_='styles_rowLight__3uy9z styles_row__2ee6F')[5].get_text().rpartition('Сценарий')[2],
            'prod': soup.find_all('div', class_='styles_rowLight__3uy9z styles_row__2ee6F')[6].get_text().rpartition('Продюсер')[2].rpartition(', ...')[0],
            'operator': soup.find_all('div', class_='styles_rowLight__3uy9z styles_row__2ee6F')[7].get_text().rpartition('Оператор')[2],
            'kompozitor': soup.find_all('div', class_='styles_rowLight__3uy9z styles_row__2ee6F')[8].get_text().rpartition('Композитор')[2],
            'hydog': soup.find_all('div', class_='styles_rowLight__3uy9z styles_row__2ee6F')[9].get_text().rpartition('Художник')[2].rpartition(', ...')[0],
            'montag': soup.find_all('div', class_='styles_rowLight__3uy9z styles_row__2ee6F')[10].get_text().rpartition('Монтаж')[2],
            'budged': int(''.join(i for i in soup.find_all('div', class_='styles_rowLight__3uy9z styles_row__2ee6F')[11].get_text().rpartition('Бюджет$')[2] if i.isdigit())),
            'sbori_usa':int(''.join(i for i in soup.find_all('div', class_='styles_rowLight__3uy9z styles_row__2ee6F')[12].get_text().rpartition('= $')[2] if i.isdigit())),
            'sbori_mir':int(''.join(i for i in soup.find_all('div', class_='styles_rowLight__3uy9z styles_row__2ee6F')[13].get_text().rpartition('= $')[2] if i.isdigit())),
            'sbori_rus':int(''.join(i for i in soup.find_all('div', class_='styles_rowLight__3uy9z styles_row__2ee6F')[15].get_text().rpartition('= $')[2] if i.isdigit())),
            'premi_mir':soup.find_all('div', class_='styles_rowLight__3uy9z styles_row__2ee6F')[-5].get_text().rpartition('Премьера в мире')[2].rpartition(', ...')[0],
            'reliz': soup.find_all('div', class_='styles_rowLight__3uy9z styles_row__2ee6F')[-5].get_text().rpartition('Релиз на DVD')[2].rpartition(', «')[0],
            'reliz': soup.find_all('div', class_='styles_rowLight__3uy9z styles_row__2ee6F')[-4].get_text().rpartition('Релиз на DVD')[2].rpartition(', «')[0],
            'vozrast': soup.find_all('div', class_='styles_rowLight__3uy9z styles_row__2ee6F')[-3].get_text().rpartition('Возраст')[2],
            'mpaa': soup.find_all('div', class_='styles_rowLight__3uy9z styles_row__2ee6F')[-2].get_text().rpartition('Рейтинг MPAA')[2],
            'vremya': soup.find_all('div', class_='styles_rowLight__3uy9z styles_row__2ee6F')[-1].get_text().rpartition('Время')[2].rpartition(' мин.')[0]

        }
    )
    return nam

def get_content_d(html):
    soup = BeautifulSoup(html, 'html.parser')
    nam = []
    nam.append(
        {

            'title': soup.find('span', class_='styles_title__2l0HH').get_text(),
            'ocenka_kin': soup.find('span', class_='styles_value__3qmcr').get_text(),
            'ocenka_imdb': soup.find('span', class_='styles_valueSection__19woS').get_text(),
            'kol-vo_imdb': soup.find('span', class_='styles_count__gelnz').get_text(),
            'kol-vo_kin': soup.find('span', class_='styles_count__3hSWL').get_text(),
            'kinokrit_mir': soup.find_all('span', class_='styles_value__3qmcr')[2].get_text(),
            'god': soup.find('a', class_='styles_linkDark__3aytH styles_link__1N3S2').get_text(),
            'strana': soup.find_all('div', class_='styles_rowDark__2qC4I styles_row__2ee6F')[1].get_text().rpartition('Страна')[2],
            'ganr': soup.find_all('div', class_='styles_rowDark__2qC4I styles_row__2ee6F')[2].get_text().rpartition('Жанр')[2].rpartition('слова')[0],
            'akt': ', '.join([ ' '.join(re.sub(r"(\w)([А-Я])", r"\1 \2", soup.find('ul', class_='styles_list__I97eu').get_text()).split()[::][i:i+2])[::] for i in range(0,len(re.sub(r"(\w)([А-Я])", r"\1 \2", soup.find('ul', class_='styles_list__I97eu').get_text()).split()),2)][::]),
            'resisor': soup.find_all('div', class_='styles_rowDark__2qC4I styles_row__2ee6F')[4].get_text().rpartition('Режиссер')[2],
            'scenariy': soup.find_all('div', class_='styles_rowDark__2qC4I styles_row__2ee6F')[5].get_text().rpartition('Сценарий')[2],
            'prod': soup.find_all('div', class_='styles_rowDark__2qC4I styles_row__2ee6F')[6].get_text().rpartition('Продюсер')[2].rpartition(', ...')[0],
            'operator': soup.find_all('div', class_='styles_rowDark__2qC4I styles_row__2ee6F')[7].get_text().rpartition('Оператор')[2],
            'kompozitor': soup.find_all('div', class_='styles_rowDark__2qC4I styles_row__2ee6F')[8].get_text().rpartition('Композитор')[2],
            'hydog': soup.find_all('div', class_='styles_rowDark__2qC4I styles_row__2ee6F')[9].get_text().rpartition('Художник')[2].rpartition(', ...')[0],
            'montag': soup.find_all('div', class_='styles_rowDark__2qC4I styles_row__2ee6F')[10].get_text().rpartition('Монтаж')[2],
            'budged': int(''.join(i for i in soup.find_all('div', class_='styles_rowDark__2qC4I styles_row__2ee6F')[11].get_text().rpartition('Бюджет$')[2] if i.isdigit())),
            'sbori_usa':int(''.join(i for i in soup.find_all('div', class_='styles_rowDark__2qC4I styles_row__2ee6F')[12].get_text().rpartition('= $')[2] if i.isdigit())),
            'sbori_mir':int(''.join(i for i in soup.find_all('div', class_='styles_rowDark__2qC4I styles_row__2ee6F')[13].get_text().rpartition('= $')[2] if i.isdigit())),
            'sbori_rus':int(''.join(i for i in soup.find_all('div', class_='styles_rowDark__2qC4I styles_row__2ee6F')[15].get_text().rpartition('= $')[2] if i.isdigit())),
            'premi_mir':soup.find_all('div', class_='styles_rowDark__2qC4I styles_row__2ee6F')[-5].get_text().rpartition('Премьера в мире')[2].rpartition(', ...')[0],
            'reliz': soup.find_all('div', class_='styles_rowDark__2qC4I styles_row__2ee6F')[-5].get_text().rpartition('Релиз на DVD')[2].rpartition(', «')[0],
            'reliz': soup.find_all('div', class_='styles_rowDark__2qC4I styles_row__2ee6F')[-4].get_text().rpartition('Релиз на DVD')[2].rpartition(', «')[0],
            'vozrast': soup.find_all('div', class_='styles_rowDark__2qC4I styles_row__2ee6F')[-3].get_text().rpartition('Возраст')[2],
            'mpaa': soup.find_all('div', class_='styles_rowDark__2qC4I styles_row__2ee6F')[-2].get_text().rpartition('Рейтинг MPAA')[2],
            'vremya': soup.find_all('div', class_='styles_rowDark__2qC4I styles_row__2ee6F')[-1].get_text().rpartition('Время')[2].rpartition(' мин.')[0]

        }
    )
    return nam

html = get_html(URL).text
silki_d, silki_l = get_content(html)
film=[]
print(silki_d)
print(silki_l)
for i in range(0,len(silki_l)):
    html = get_html(''.join(silki_l[i])).text
    film.append(get_content_l(html))
    sleep(random.randrange(10, 20))

for i in range(0,len(silki_d)):
    html = get_html(''.join(silki_d[i])).text
    film.append(get_content_d(html))
    sleep(random.randrange(10, 20))

def save(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название', 'Оценка_кинопоиска', 'Оценка_imdb', 'кол-во_imdb', 'кол-во_киноп', 'рейтинг_кинокритиков', 'год', 'страна', 'актеры', 'режиссер', 'сценаристы', 'продюссеры', 'оператор', 'композитор', 'художник', 'монтаж', 'бджет', 'сборы_США', 'сборы_мир', 'сборы_Россия', 'премьера', 'релиз', 'возраст_огранич', 'mpaa', 'время'])
        for item in items:
            writer.writerow([film['title'],film['ocenka_kin'],film['ocenka_imdb'],film['kol-vo_imdb'],film['kol-vo_kin'],film['kinokrit_mir'],film['god'],film['strana'],film['ganr'],film['akt'],film['resisor'],film['scenariy'],film['prod'],film['operator'],film['kompozitor'],film['hydog'],film['montag'],film['budged'],film['sbori_usa'],film['sbori_mir'],film['sbori_rus'],film['premi_mir'],film['reliz'],film['vozrast'],film['mpaa'],film['vremya']])

def parser():
    PAGE = 10
    html = get_html(URL)
    if html.status_code == 200:
        kino = []
        for page in range(1, PAGE):
            print(f'Парсинг страницы: {page}')
            html = get_html(URL, params={'page': page})
            kino.extend(get_content(html.text))
            save(kino, CSV)
            sleep(random.randrange(5, 10))
        pass
    else:
        print('Error')

parser()

