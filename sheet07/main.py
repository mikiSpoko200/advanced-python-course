# -*- encoding: utf-8 -*-

"""
# Discussion of my design choices:

        Homework sheet suggested that we should use multithreading / multiprocessing approach, but in my opinion
    it's not really the right thing to in case of my program.
    I did some time profiling of my code from sheet06 and found that the application was clearly IO bound
    not CPU bound. Using multiprocessing would be the easiest solution each request gets it's new process
    but that would generate needless overhead of spawning multiple python interpreter processes both
    in regard to memory consumption and time needed for the OS to create these processes.
    Using multithreading could solve this issue - we could just spawn a new thread for each request,
    but this would force us to worry about thread synchronization which is very tricky to do right.
    Why use any of these technics if we can language feature designed for that specific purpose - asyncIO.

        AsyncIO allows us to make the most use of our single thread of execution by utilizing preemptive multitasking.
    That is different components of the program can yield their CPU time to other components if they are to hang
    on some long running computation that is IO bound like for example fetching data from the web or waiting for
    user input. Our single thread runs what's called a Event Loop. It's a mechanism that controls the flow of
    execution based on what jobs are available. Basic element of this system is a coroutine - a generalization
    of subroutine. The difference between the two is the ability of coroutine to stop it's execution
    at any given time - yield it's control - and be resumed in the future from the point where it stopped without
    loosing it's internal state. This allows the event loop to receive and distribute work to coroutines based on
    availability of resources they need to continue their execution. The networking is the prime use case
    for such mechanism. It not only allows us to be efficient with our CPU usage, but it also requires no
    synchronization unlike threads.

        Given all mentioned above I decide to deviate slightly from or original task by expanding the realm
    of multiprocessing techniques with asynchronous code.


# What changed from sheet06:

    Command line interface is the same with addition of one flag --try-sync which downloads webpages using
    standard blocking io for comparison. For remaining functionality please see sheet06_main.py's module docstring.

    Since I'll be reusing code from sheet06. I know that the mechanism for checking for changes
    works as intended. This allows me to focus on improving performance of my script by utilizing some form
    of multitasking approach.

    In order to really see the benefit of multitasking oriented application architecture we need to increase input size.
    I previously tested this script with at most 5 websites at once. The reason being that adding more websites
    would generate too much information to be reasonably processed by a person.

    From now on program will be logging all modifications to a log file and displaying only the number of pages
    that changed. That way we'll be able to focus on what really matters in this assignment.


# Comparison:

   (.venv) PS > py ex2_Depta_async.py --operation-mode text --config large_input.json --try-sync True
    Operation Mode      :: TEXT_MODE
    Input file          :: large_input.json
    Started fetching synchronously...
    Fetched 27 Websites.
    Finished synchronous work after 28.512279748916626s
    Started fetching asynchronously...
    Finished asynchronous work after 3.05753231048584s

    I think that these results speak for themselves.


# Learning resources:

    Video about threads and processes:
        https://youtu.be/qkugPXGeX58
    Video about thread synchronization and communication:
        https://youtu.be/_olNhuuRYxo

    Python asyncIO docs:
        https://docs.python.org/3/library/asyncio.html

    Distinction between coroutine and a generator:
        https://medium.com/analytics-vidhya/python-generators-coroutines-async-io-with-examples-28771b586578

TODO do more reading on:
    x86 LOCK prefix,
    interlocked exchange, interlocked increase, interlock compare exchange.
    asyncIO python,
    Thread safety,
    async vs threads -- which one I should use
"""


__AUTHOR__ = "Mikołaj Depta"
__VERSION__ = "0.1.0"


import asyncio
import urllib.request
from collections import defaultdict
import aiohttp
import datetime
import difflib
import codecs
import time
import urllib.request as req
import user_interface as ui
from json.decoder import JSONDecoder
from sheet06_main import (OperationMode, URL, WebsiteState, HTTPS_HEADER, DEFAULT_DATETIME_FORMAT)
from bs4 import BeautifulSoup
from typing import Optional, NamedTuple


DELAY = 10


class FetchInfo(NamedTuple):
    """Dataclass containing information on websites sources code and time at which it was fetched."""
    source: str
    timestamp: str


async def fetch_url(url: URL) -> FetchInfo:
    """Fetch website asynchronously."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return FetchInfo(
                codecs.decode(await response.read(), encoding="utf-8"),
                datetime.datetime.now().strftime(DEFAULT_DATETIME_FORMAT))


def create_tasks(urls: list[URL]) -> list[asyncio.Task]:
    """Schedule tasks that download specified websites."""
    return [asyncio.create_task(fetch_url(url)) for url in urls]


def remove_empty_lines(lines: list[str]) -> list[str]:
    """Remove lines consisting only from a newline character."""
    return list(filter(lambda line: line != "\n", lines))


def process_response(fetch_info: FetchInfo, operation_mode: OperationMode) -> WebsiteState:
    """Process website's source to be suitable for comparison for specified operation mode."""
    soup = BeautifulSoup(fetch_info.source, features="html.parser")
    data = soup.get_text() if operation_mode is OperationMode.TEXT_MODE else soup.prettify()
    lines = remove_empty_lines(data.splitlines(keepends=True))
    return WebsiteState(fetch_info.timestamp, lines, soup.title.string)


async def check_websites(
        urls: list[URL],
        website_state_lookup: dict[URL, Optional[WebsiteState]], *,
        operation_mode: OperationMode) -> None:
    """Download webpages asynchronously and compare for changes."""
    fetched_websites = await asyncio.gather(*create_tasks(urls))
    changed = 0
    for fetch_into, url in zip(fetched_websites, urls):
        prev_state = website_state_lookup[url]
        curr_state = process_response(fetch_into, operation_mode)
        if prev_state is None:
            ui.log_initial(curr_state)
        else:
            changes = list(difflib.unified_diff(
                prev_state.content, curr_state.content,
                "Previous version", "Current version",
                prev_state.check_timestamp, curr_state.check_timestamp,
                n=3
            ))
            if changes:
                changed += 1
                ui.log_changes(curr_state, changes)
        website_state_lookup[url] = curr_state
    ui.log_new(changed, len(urls))


def fetch_synchronous(urls):
    """Synchronous fetching prepared for reference."""
    websites = []
    for link in urls:
        request = req.Request(link, headers=HTTPS_HEADER)
        with urllib.request.urlopen(request) as response:
            websites.append(codecs.decode(response.read(), encoding="utf-8"))
    print(f"Fetched {len(websites)} Websites.")


async def main():
    config = ui.command_line_interface()
    ui.log_config(config)
    website_state_lookup: dict[URL, Optional[WebsiteState]] = defaultdict(lambda: None)
    with open(config.input, "r", encoding="utf-8") as urls_json:
        urls = JSONDecoder().decode(urls_json.read())["urls"]
        if config.run_sync:
            print(f"Started fetching synchronously...")
            start = time.time()
            fetch_synchronous(urls)
            print(f"Finished synchronous work after {time.time() - start}s")
            print(f"Started fetching asynchronously...")
            start = time.time()
            await asyncio.gather(*create_tasks(urls))
            print(f"Finished asynchronous work after {time.time() - start}s")
        else:
            while True:
                await check_websites(urls, website_state_lookup, operation_mode=config.operation_mode)
                await asyncio.sleep(DELAY)


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

