import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.proxy import Proxy, ProxyType

url_site = 'https://rezka.ag'
url_pagination = '?page={}&tab=all'
url_proxy = 'http://www.freeproxylists.net/'


def get_list_proxy(link: str) -> list:
    list_proxy = []
    res = requests.get(link)
    print(res.content)
    if res.status_code == 200:
        soup = BeautifulSoup(res.content, 'html.parser')
        tr_list = soup.findAll('tr', {'class': 'Odd'})
        list_proxy = [tr.find('a').text for tr in tr_list]
    return list_proxy


def get_genre_links(link: str) -> list:
    soup = get_soup(link)
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


def get_page_links(link: str) -> list:
    soup = get_soup(link)
    page_links = []
    if soup:
        pagination_div = soup.find('div', {'class': 'b-navigation'})
        a_list = pagination_div.findAll('a')
        pagination_number = a_list[-2].text
        page_links = [link + url_pagination.format(str(n)) for n in range(int(pagination_number))]
    return page_links


def get_films_links(link: str) -> list:
    soup = get_soup(link)
    films_links = []
    if soup:
        div_all = soup.findAll('div', {'class': 'b-content__inline_item'})
        films_links = [d['data-url'] for d in div_all]
    return films_links


def get_soup(link: str) -> str:
    soup = ''
    res = requests.get(link)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'html.parser')
    return soup
