"""
Написать программу, которая скачивает изображения с заданных URL-адресов и
сохраняет их на диск. Каждое изображение должно сохраняться в отдельном
файле, название которого соответствует названию изображения в URL-адресе.
� Например URL-адрес: https://example/images/image1.jpg -> файл на диске:
image1.jpg
� Программа должна использовать многопоточный, многопроцессорный и
асинхронный подходы.
� Программа должна иметь возможность задавать список URL-адресов через
аргументы командной строки.
� Программа должна выводить в консоль информацию о времени скачивания
каждого изображения и общем времени выполнения программы.
"""

import requests
import threading
import time
from multiprocessing import Process
import asyncio
import aiohttp
import aiofiles

urls = [
    'https://sportishka.com/uploads/posts/2022-11/1667575953_58-sportishka-com'
    '-p-dostoprimechatelnosti-yekb-oboi-64.jpg',
    'https://mykaleidoscope.ru/x/uploads/posts/2022-09/1663330714_17-'
    'mykaleidoscope-ru-p-yekaterinburg-stolitsa-urala-krasivo-18.jpg',
]


def thread_download(url):
    response = requests.get(url)
    filename = 'threading_' + url.replace('https://', '').replace('.',
                                                                  '_').replace(
        '/', '') + '.jpg'

    with open(filename, "wb") as f:
        f.write(response.content)
        print(
            f" Многопоточный метод скачал {url} за {time.time() - start_time:.2f} секунды")


def multi_download(url):
    response = requests.get(url)
    filename = 'multiprocessing_' + url.replace('https://', '').replace('.',
                                                                        '_').replace(
        '/', '') + '.jpg'

    with open(filename, "wb") as f:
        f.write(response.content)
        print(
            f" Многопроцессорный метод скачал {url} за {time.time() - start_time:.2f} секунды")


async def async_download(url):
    async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(url) as response:
            # img = await response.content.read()
            filename = 'asyncio_' + url.replace('https://', '').replace('.',
                                                                        '_').replace(
                '/', '') + '.jpg'
            f = await aiofiles.open(filename, mode='wb')
            await f.write(await response.read())
            await f.close()

            print(
                f" Асинхронный метод скачал {url} за {time.time() - start_time:.2f} секунды")


async def main():
    tasks = []
    for url in urls:
        task = asyncio.ensure_future(async_download(url))
        tasks.append(task)
    await asyncio.gather(*tasks)


start_time = time.time()
if __name__ == '__main__':
    threads = []
    processes = []
    tasks = []

    start_time_all = time.time()

    start_time = time.time()
    for url in urls:
        thread = threading.Thread(target=thread_download, args=[url])
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()

    for url in urls:
        process = Process(target=multi_download, args=(url,))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()

    start_time = time.time()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

    print(
        f" Общее время работы программы: {time.time() - start_time_all:.2f} секунды")
