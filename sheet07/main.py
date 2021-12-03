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


import argparse
import threading
import asyncio
import urllib.parse
import os
from typing import NamedTuple
from time import time


async def main():
    start = time()
    urls = [
        r"https://www.python.org/dev/peps/pep-0289/",
        r"https://www.python.org/dev/peps/pep-0342/",
        r"https://www.python.org/dev/peps/pep-0380/",
        r"https://www.python.org/dev/peps/pep-0492/",
        r"https://www.python.org/dev/peps/pep-0255/"
    ]
    urls = map(lambda x: urllib.parse.urlsplit(x), urls)
    ports = [443 if url.scheme == "https" else 80 for url in urls]
    readers = []
    for url, port in zip(urls, ports):
        reader, writer = await asyncio.open_connection(url.hostname, port, ssl=port == 443, )
        query = (
            f"HEAD {url.path or '/'} HTTP/1.0\r\n"
            f"Host: {url.hostname}\r\n"
            f"\r\n"
        )

        writer.write(query.encode('latin-1'))
        while True:
            line = await reader.readline()
            if not line:
                break

            line = line.decode('latin1').rstrip()
            if line:
                print(f'HTTP header> {line}')

        # Ignore the body, close the socket
        writer.close()



asyncio.run(main())

