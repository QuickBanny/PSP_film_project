import asyncio
import time
from parse_data import *
from use_api import *

async def loop_genre(links: list):
    for link in links:
        if check_genre(link['name']):
            pass
        else:
            add_genre(link['name'])
        print(link)
        await parse_genre_pagination(link['url'])


async def parse_genre_pagination(link: str):
    for link_page in get_page_links(link):
        #await asyncio.sleep(1000)
        await parse_page_list_films(link_page)


async def parse_page_list_films(link: str):
    for link in get_films_links(link):
        await parse_film_page(link)


async def parse_film_page(link: str):
    print(link)
    print("DATA FILMS OK")
    return True

if __name__ == '__main__':
    #kinopoisk_link = 'https://www.kinopoisk.ru/lists/films/8/'
    hd_rezka = 'https://rezka.ag/films/'
    genre_links = get_genre_links(hd_rezka)
    asyncio.run(loop_genre(get_genre_links(hd_rezka)))