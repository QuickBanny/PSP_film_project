import asyncio
import time
from parse_data import *
from use_api import *
from datetime import datetime


def genre_db(genre_objects: list):
    for genre in genre_objects:
        if check_genre(genre['name']):
            pass
        else:
            add_genre(genre['name'])


def films_db(films_objects: list):
    pass


def main():
    hd_rezka = ['https://rezka.ag/films/']
    loop = asyncio.get_event_loop()
    try:
        task_get_genre_link = loop.create_task(parse_link(hd_rezka))
        genre_htmls = loop.run_until_complete(task_get_genre_link)
        genre_obj = get_links(genre_htmls, parse_genre, hd_rezka, loop)

        genre_db(genre_obj)
        genre_links = [f['url'] for f in genre_obj]
        task_get_pagination_links = loop.create_task(parse_link(genre_links))
        pagination_htmls = loop.run_until_complete(task_get_pagination_links)
        paginations_links = get_links(pagination_htmls, parse_pagination, genre_links, loop)

        task_get_films_links = loop.create_task(parse_link(paginations_links))
        films_htmls = loop.run_until_complete(task_get_films_links)
        films_links = get_links(films_htmls, parse_films_link, paginations_links, loop)

        task_get_films_data = loop.create_task(parse_link(films_links))
        films_data_htmls = loop.run_until_complete(task_get_films_data)

        get_links(films_data_htmls, parse_films, films_links, loop)
        print(len(films_links))
    finally:
        pass
       # loop.close()


if __name__ == '__main__':
    start = datetime.now()
    main()
    finish = datetime.now()
    res = finish - start
    print('Script time: ', res)