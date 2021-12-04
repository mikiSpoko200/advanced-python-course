# -*- encoding: utf-8 -*-

"""
Design decisions:
    - I did some time profiling of my earlier solution. I found that requests took on average ten times more time
    than comparing. This shows that this app is clearly IO bound. This can be solved using asyncIO.

    This is lovely. This means we don't need to waste lots of memory for spawning multiple processes or
    managing synchronization of multiple threads.


Learning resources:
Video about threads and processes:
    https://youtu.be/qkugPXGeX58
Video about thread synchronization and communication:
    https://youtu.be/_olNhuuRYxo

Python asyncIO docs:
        https://docs.python.org/3/library/asyncio.html

Distinction between coroutine and a generator:
https://medium.com/analytics-vidhya/python-generators-coroutines-async-io-with-examples-28771b586578


-- notes on the above
accordingly to python glossary, https://docs.python.org/3/glossary.html
coroutines are:
> Coroutines are a more generalized form of subroutines.
> Subroutines are entered at one point and exited at another point.
> Coroutines can be entered, exited, and resumed at many different points.
> They can be implemented with the async def statement.

TODO:
    x86 LOCK prefix,
    interlocked exchange, interlocked increase, interlock compare exchange.
    asyncIO python,
    Thread safety,
    async vs threads -- which one I should use
"""


__AUTHOR__ = "Mikołaj Depta"
__VERSION__ = "0.1.0"


import asyncio
import aiohttp
import sheet06.user_interface
import sheet06.http_error_codes
from bs4 import BeautifulSoup
from typing import Optional
from sheet06.main import (OperationMode, URL, WebsiteState)


# Basic idea: We want to create a Task for every request
# and make it schedule itself again in the future.


async def get_contents(url: URL, *, operation_mode: OperationMode) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            soup = BeautifulSoup(await response.read())
            if operation_mode is OperationMode.TEXT_MODE:
                return soup.get_text()
            else:
                return soup.prettify()


def get_tasks(urls: list[URL], operation_mode: OperationMode) -> list[asyncio.Task]:
    """Schedules tasks that downloads and parses urls."""
    return [asyncio.create_task(get_contents(url, operation_mode=operation_mode)) for url in urls]


async def check_websites(
        urls: list[URL],
        website_state_lookup: dict[URL, Optional[WebsiteState]], *,
        operation_mode: OperationMode) -> None:
    contents = await asyncio.gather(get_tasks(urls, operation_mode))
    print(contents)


async def main():
    links = [
        'https://www.python.org/',
        'https://github.com/python/cpython/blob/3.10/Doc/library/asyncio.rst',
        'https://www.python.org/',
        'https://github.com/python/cpython/tree/3.10/Lib/asyncio/',
        'https://github.com/python/cpython/blob/3.10/Doc/library/asyncio.rst',
        'https://www.python.org/',
        'https://www.python.org/psf/donations/',
        'https://docs.python.org/3/bugs.html',
        'https://www.sphinx-doc.org/',
        'https://www.python.org/',
        'https://github.com/python/cpython/blob/3.10/Doc/library/asyncio.rst',
        'https://www.python.org/',
        'https://github.com/python/cpython/tree/3.10/Lib/asyncio/',
        'https://github.com/python/cpython/blob/3.10/Doc/library/asyncio.rst',
        'https://www.python.org/',
        'https://www.python.org/psf/donations/',
        'https://docs.python.org/3/bugs.html',
        'https://www.sphinx-doc.org/',
        'https://www.python.org/',
        'https://github.com/python/cpython/blob/3.10/Doc/library/asyncio.rst',
        'https://www.python.org/',
        'https://github.com/python/cpython/tree/3.10/Lib/asyncio/',
        'https://github.com/python/cpython/blob/3.10/Doc/library/asyncio.rst',
        'https://www.python.org/',
        'https://www.python.org/psf/donations/',
        'https://docs.python.org/3/bugs.html',
        'https://www.sphinx-doc.org/',
        'https://www.python.org/',
        'https://github.com/python/cpython/blob/3.10/Doc/library/asyncio.rst',
        'https://www.python.org/',
        'https://github.com/python/cpython/tree/3.10/Lib/asyncio/',
        'https://github.com/python/cpython/blob/3.10/Doc/library/asyncio.rst',
        'https://www.python.org/',
        'https://www.python.org/psf/donations/',
        'https://docs.python.org/3/bugs.html',
        'https://www.sphinx-doc.org/'
    ]
    await check_websites(links, OperationMode.TEXT_MODE)


asyncio.run(main())

