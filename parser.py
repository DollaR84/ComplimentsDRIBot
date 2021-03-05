"""
Parser module for bot.

Created on 03.03.2021

@author: Ruslan Dolovanyuk

"""

import os
import aiohttp
import asyncio

import multiprocessing as mp
from itertools import repeat

from bs4 import BeautifulSoup


class URL:
    BASE = 'https://smsta.ru/m/sms/'
    FUN = 'm_fun'
    EROTIC = 'm_erotic'

    def __call__(self):
        urls = [
            ''.join([URL.BASE, URL.FUN]),
            ''.join([URL.BASE, URL.EROTIC]),
        ]
        return urls


class Headers:
    def __call__(self):
        headers = {
            'User-Agent': 'Mozilla/5.0; Windows 8.1; rv:55.0; Firefox/55.0'
        }
        return headers


__urls__ = URL()
__headers__ = Headers()


async def load(client, url):
    result = None
    async with client.get(url) as response:
        if 200 == response.status:
            result = await response.read()
    return result


async def get_pages(urls, pages):
    """Load pages from site."""
    async with aiohttp.ClientSession() as client:
        coroutines = [load(client, url) for url in urls]
        completed, pending = await asyncio.wait(coroutines)
        for item in completed:
            result = item.result()
            pages.append(result)
    await asyncio.sleep(0.3)


def parse(page, ):
    """Parsing data from loaded pages."""
    bs = BeautifulSoup(page, 'html.parser')
    result = {'posts': [], 'entries': [], 'urls': []}
    content = bs.find('div', {'id': 'content'})
    for post in content.find_all('div', {'class': 'post_03'}):
        result['posts'].append(post.find('div').text.strip())
    for entry in content.find('div', {'class': 'entry'}).find_all('p'):
        for span in entry.find_all('span'):
            span.decompose()
        result['entries'].append(entry.text.strip())
    for link in content.find('nav', {'class': 'list_00'}).find('div', {'class': 'list_03'}).find_all('a'):
        result['urls'].append(link.get('href'))
    return result


def get_data():
    """Load, parse and return data from site."""
    data = []
    pages = []
    asyncio.run(get_pages(__urls__(), pages))
    with mp.Pool(processes=mp.cpu_count()) as pool:
        results = pool.map(parse, pages)
    data.extend([item for result in results for item in result['posts']])
    data.extend([item for result in results for item in result['entries']])
    pages.clear()
    urls = [''.join([URL.BASE, url]) for result in results for url in result['urls']]
    asyncio.run(get_pages(urls, pages))
    with mp.Pool(processes=mp.cpu_count()) as pool:
        results = pool.map(parse, pages)
    data.extend([item for result in results for item in result['posts']])
    data.extend([item for result in results for item in result['entries']])
    return data


def main():
    data = get_data()
    with open(os.path.join('debug', 'compliments.log'), 'w', encoding='utf-8') as fout:
        for item in data:
            fout.write(f'{item}\n***\n')


if '__main__' == __name__:
    main()
