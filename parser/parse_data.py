import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.proxy import Proxy, ProxyType

url_site = 'https://rezka.ag'
url_pagination = '?page={}&tab=all'
url_proxy = 'http://www.freeproxylists.net/'

import urllib.request
import asyncio
import aiohttp


def get_list_proxy(link: str) -> list:
    list_proxy = []
    res = requests.get(link)
    print(res.content)
    if res.status_code == 200:
        soup = BeautifulSoup(res.content, 'html.parser')
        tr_list = soup.findAll('tr', {'class': 'Odd'})
        list_proxy = [tr.find('a').text for tr in tr_list]
    return list_proxy


def parse_genre(soup: str, link, loop):
    links_genre = []
    if soup:
        div_content = soup.find('div', {'class': "b-topnav__sub_inner"})
        ul = div_content.find('ul', {'class': 'left'})
        list_a = ul.findAll('a')
        for a in list_a:
            name = a.text
            links_genre.append({
                'name': name,
                'url': url_site + a['href']
            })
    return links_genre


def parse_pagination(soup: str, link: str, loop):
    page_links =[]
    if soup:
        pagination_div = soup.find('div', {'class': 'b-navigation'})
        if pagination_div:
            a_list = pagination_div.find_all('a')
            pagination_number = a_list[-2].text
            page_links = [link + url_pagination.format(str(n)) for n in range(int(pagination_number))]
    return page_links


def parse_films_link(soup: str, link: str, loop):
    films_links =[]
    if soup:
        div_all = soup.find_all('div', {'class': 'b-content__inline_item'})
        films_links = [d['data-url'] for d in div_all]
    return films_links


def parse_films(soup: str, link: str, loop):
    print(link)
    people_links = []
    films_obj = {}
    if soup:
        div_main = soup.find('div', {'class': 'b-post'})
        if div_main:
            try:
                title = div_main.find('div', {'class': 'b-post__title'}).text
            except:
                title = ''
            try:
                original_title = div_main.find('div', {'class': 'b-post__origtitle'}).text
            except:
                original_title = ''
            try:
                serial_type = div_main.find('div', {'class': 'b-post__infolast'}).text
            except:
                serial_type = ''

            tagline = ''
            production_year = ''
            country_list = ''
            genre_list = ''
            years_old = ''
            rating_kp = ''
            try:
                table_info = div_main.find('table', {'class': 'b-post__info'})
                all_tr_table = table_info.find_all('tr')
                try:
                    span_rating_kp = table_info.find('span', {'class': 'b-post__info_rates kp'})
                    rating_kp = span_rating_kp.find('span').text
                except:
                    rating_kp = ''


                for tr in all_tr_table:
                    td = tr.find_all('td')
                    if td[0].find('h2').text == 'Слоган':
                        tagline = td[1].text
                    elif td[0].find('h2').text == 'Дата выхода':
                        production_year = td[1].text
                    elif td[0].find('h2').text == 'Страна':
                        country_list = [a.text for a in td[1].find_all('a')]
                    elif td[0].find('h2').text == 'Режиссер':
                        director_link = td[1].find('a')['href']
                        people_links.append(director_link)
                    elif td[0].find('h2').text == 'Жанр':
                        genre_list = [g.text for g in td[1].find_all('span', {'itemprop': 'genre'})]
                    elif td[0].find('h2').text == 'Возраст':
                        years_old = td[1].find('span').text
                    elif td[0].find('h2').text == 'В ролях актеры':
                        people_links += [a['href'] for a in td[0].find_all('a')]
            except:
                pass

            description = div_main.find('div', {'class': 'b-post__description_text'}).text

            films_obj['title'] = title
            films_obj['original_title'] = original_title
            films_obj['serial_type'] = serial_type
            films_obj['rating_kp'] = rating_kp
            films_obj['tagline'] = tagline
            films_obj['production_year'] = production_year
            films_obj['country_list'] = country_list
            films_obj['genre_list'] = genre_list
            films_obj['years_old'] = years_old
            films_obj["description"] = description

            task_get_people = loop.create_task(parse_link(people_links))
            html_by_people = loop.run_until_complete(task_get_people)
            get_links(html_by_people, parse_film_people, people_links, loop)
            #print(films_obj)
        else:
            print('ERROR 503')
            print('Recursion')
            task_get_films_data = loop.create_task(parse_link([link]))
            films_data_htmls = loop.run_until_complete(task_get_films_data)
            get_links(films_data_htmls, parse_films, [link], loop)
    return films_obj


def parse_film_people(soup: str, link: str, loop):
    #print('Actors')
    print(link)
    return []


def get_links(soup: list, f, links: list, loop) -> list:
    res_links = []
    for i in range(len(soup)):
        paginations = f(soup[i], links[i], loop)
        res_links += paginations
    return res_links


def get_films_links(link: str) -> list:
    soup = get_soup(link)
    films_links = []
    if soup:
        div_all = soup.findAll('div', {'class': 'b-content__inline_item'})
        films_links = [d['data-url'] for d in div_all]
    return films_links


async def get_html(link: str, session):
    async with session.get(link) as response:
        resp = await response.text()
        return BeautifulSoup(resp, 'html.parser')


async def parse_link(links: list):
    async with aiohttp.ClientSession() as session:
        tasks = [get_html(link, session) for link in links]
        htmls = await asyncio.gather(*tasks, return_exceptions=True)
        return htmls