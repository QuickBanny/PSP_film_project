import asyncio
from datetime import datetime
from use_api import *
from parse_data import *


async def loop_genre(semaphrone, genre: dict):
    res_page_links = []
    async with semaphrone:
        if check_genre(genre['name']):
            pass
        else:
            add_genre(genre['name'])
        print(genre)
        #res = get_links(genre['url'], parse_pagination)
        #res_page_links += res
    #print(res_page_links)
        #task_parse_genre_pagination = asyncio.create_task(parse_genre_pagination(link['url']))
        #return await parse_genre_pagination(link['url'])


async def parse_genre_pagination(link: str):
    return [1, 2, 3]
    #links_paginations = get_page_links(link)
    #return await parse_page_list_films(link_page)


async def parse_page_list_films(link: str):
    ##async with semaphrone:
    return await asyncio.wait([parse_film_page(link) for link in get_films_links(link)])
    #for link in get_films_links(link):
    #    #task_parse_film_page = asyncio.create_task(parse_film_page(link))
    #    await parse_film_page(link)

async def parse_film_page(link: str):
    async with semaphrone:
        print(link)
        print("DATA FILMS OK")
        #async with asyncio.Semaphore(1000):
        return True


async def main(genre_objects: list):
    mySemaphore = asyncio.Semaphore(50)
    await asyncio.wait([loop_genre(mySemaphore, genre) for genre in genre_objects])


if __name__ == '__main__':
    start = datetime.now()
    hd_rezka = ['https://rezka.ag/films/']
    genre_obj = get_links(hd_rezka, parse_genre)
    #asyncio.run(loop_genre(get_genre_links(hd_rezka)[0:1]))
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(genre_obj))
    finish = datetime.now()
    res = finish - start
    print('Script time: ', res)
    loop.close()