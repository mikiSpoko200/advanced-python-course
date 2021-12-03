#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Exercise 2. Implement a website monitoring system that checks if a page has changed its content.
We assume that our program can monitor more than one page; we also assume that checking takes
place periodically (e.g. every 1 minute).
In this task we assume that page layout changes rarely, only individual elements of this layout are
changed, so if the program detects a change, it must return only what has changed.


PLEASE NOTE:
    This script has an command line interface - please type --help / -h to see more.
    This script requires two external modules to be installed:
        - BeautifulSoup4 - pip install bs4
        - termcolor      - pip install termcolor
    I supplied both virtual environment (.venv) containing said modules and a requirements.txt file.


Program description:
    
    This program tracks 'changes' in websites on 60s basis.
    Command line interface expects a literal that represents the mode of operation in which the script
    should function.
    Currently there are two separate modes of operation:
        - TEXT_MODE     -- annotated by either "text" or "t"
        - LAYOUT_MODE   -- annotated by either "layout" or "l"
    note: input is case insensitive.
    See definition of OperationMode enum for more info.

    User can also specify the file from which urls should be pulled. (.json format)
    expected format:
    {
        "urls": [
            "url1",
            "url2",
            "url3",
            ...
        ]
    }

    I prepared few sample files text.json and layout.json both are somewhat suitable
    for specific types of operation.

    Modes of operation differ in terms of what content do they check.
        - TEXT_MODE     -- checks only for changes in pages text
        - LAYOUT_MODE   -- detects both changes in text and in it's layout on the page (HTML)
                           this can cause output to be very verbose so caution is advised.
    
    Webpage is represented by it's title parsed from HTMl on initial parsing and it's not updated even if title changes.

    In my implementation I use std lib module called sched which exposes
    a general purpose blocking (by default) event loop.

    Alternative solution to that would be using signal module which provides us with functionality
    there we could use
    signal.setitimer(signal.ITIMER_REAL, 60) -- this would every 60s schedule SIGALRM signal.
    We could than add a signal handler with
    signal.signal(signal.SIGALRM, <our function for checking webpages>)

    But this unfortunately does not work under windows since windows does not provide SIGALRM signal.


Regarding testing:
    I found it very difficult to find a reliable website that can be used for testing.
    Since test's must be reproducible and there wasn't any specification regarding the exact format
    I took a liberty and decided that I'll test script manually and in the process came up with the urls
    supplied in the filed mentioned above.


What I learned for this lab:
    For quite some time a wanted to get into parallel/concurrent programming.
    I had a vague notion of the meaning of terms such as process, thread, coroutine
    asynchronous programming in particular term asyncIO which prevents programs from stalling
    on long IO operations such as awaiting for user input or network request.
    However due to time constraints and fact that sheet 7 is about making this solution multi threaded
    I settled on a synchronous blocking solution.

    My learning resources:
    introduction to asyncio in python:
     - https://www.youtube.com/watch?v=3mb9jFAHRfw&ab_channel=PyConAU
    MSDN article broadly touching on the topic:
     - https://docs.microsoft.com/en-gb/windows/win32/procthread/about-processes-and-threads?redirectedfrom=MSDN
    Simplified overview of async mechanism in rust:
     - https://youtu.be/ThjvMReOXYM
     - https://youtu.be/9_3krAQtD2k
    Chapter 10.5: "asyncio: Asynchronous I/O, Event Loop, and Concurrency Tools"
    of "the Python 3 Standard Library by Example".
"""

from time import time

import argparse
import difflib
import enum
import http_error_codes
import sched
import user_interface as ui
from collections import defaultdict
from datetime import datetime
from json.decoder import JSONDecoder
from typing import NamedTuple, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


__VERSION__ = "0.1.0"


scheduler = sched.scheduler()
DEFAULT_DATETIME_FORMAT = "%d-%m-%Y %H:%M:%S"
DEFAULT_CONFIG_FILE = "layout.json"
CHECKING_PERIOD = 10

# Adding such fake headers makes it more difficult for servers to detect that our it is in face python script
# that is trying to gain access to some resources. Some services block such connections on purpose so that
# programmers use their API instead.
HTTPS_HEADER: dict[str, str] = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}

URL = str


class WebsiteState(NamedTuple):
    """Data struct that groups information about webpages state."""
    check_timestamp: str
    content: list[str]
    title: str


class OperationMode(enum.Enum):
    """Enumeration of different operation types."""
    TEXT_MODE = enum.auto()
    LAYOUT_MODE = enum.auto()

    def __str__(self) -> str:
        return super().__str__().split(".")[-1]

    @classmethod
    def from_str(cls, rep: str):
        """Create appropriate version of the OperationMode based on string rep input.
        Accepted strings (case insensitive):
         - text | t    -> OperationMode.TEXT_MODE
         - layout | l  -> OperationMode.LAYOUT_MODE
        """
        if rep.lower() in ("text", "t"):
            return OperationMode.TEXT_MODE
        if rep.lower() in ("layout", "l"):
            return OperationMode.LAYOUT_MODE
        else:
            raise ValueError("Invalid string representation of OperationMode.")


class ConfigInfo(NamedTuple):
    """Data struct that groups configuration information."""
    operation_mode: OperationMode
    input: str


def schedule_website_check(
        url: URL,
        website_state_lookup: dict[URL, Optional[WebsiteState]], *,
        operation_mode: OperationMode,
        delay: int = CHECKING_PERIOD) -> None:
    """Schedules website check in delay seconds."""
    scheduler.enter(delay, 1, check_website, (url, website_state_lookup), {"operation_mode": operation_mode})


def process_content(content: list[str]) -> list[str]:
    return list(filter(lambda line: line != "\n", content))


def check_website(url: URL, website_state_lookup: dict[URL, Optional[WebsiteState]], *,
                  operation_mode: OperationMode) -> None:
    """Check for changes in a website that can be accessed via *url*.
    Check consists of:
     - fetching a webpage
     - comparing new website against its previous version -- previous state is stored in previous_state data structure.
       Depending on the value of operation_mode program either checks for changes in:
         - page's layout (compared html lines)
         - page's text contents (parsed using BeautifulSoup)
     - print comparison
     - if any change occurred print changes to the screen and update the state in other case do nothing
     - schedule next callback.
    """
    prev_state = website_state_lookup[url]
    req = Request(url, headers=HTTPS_HEADER)

    try:
        website_start = time()
        with urlopen(req) as response:
            print(f"Fetching website took: {time() - website_start}s")
            soup = BeautifulSoup(response.read().decode("utf-8"), features="html.parser")
            if operation_mode is OperationMode.LAYOUT_MODE:
                new_content = soup.prettify().splitlines(keepends=True)
            else:
                new_content = process_content(soup.get_text().splitlines(keepends=True))
            title = soup.title.string if prev_state is None else prev_state.title

            curr_state = WebsiteState(
                datetime.now().strftime(DEFAULT_DATETIME_FORMAT),
                new_content,
                title
            )

            # logging for first check.
            if prev_state is None:
                ui.log_initial(curr_state)
            # actual comparison and appropriate logging.
            else:
                start = time()
                changes = list(difflib.unified_diff(
                    prev_state.content, curr_state.content,
                    "Previous version", "Current version",
                    prev_state.check_timestamp, curr_state.check_timestamp,
                    n=3
                ))
                print(f"Comparing took: {time() - start}s")
                if changes:
                    ui.log_change(curr_state, changes)
                else:
                    ui.log_no_change(curr_state)

            # update state in global lookup.
            website_state_lookup[url] = curr_state

            # schedule next check
            schedule_website_check(url, website_state_lookup, operation_mode=operation_mode)
    # Handle HTTP error codes
    except HTTPError as err:
        print(http_error_codes.responses[err.code])
        del website_state_lookup[url]
    # Handle Connection errors
    except URLError as err:
        print('Cannot establish connection to the server!.')
        print('Reason: ', err.reason)
        del website_state_lookup[url]


def command_line_interface() -> tuple[OperationMode, Optional[str]]:
    parser = argparse.ArgumentParser(description="Track changes in websites.")
    parser.add_argument(
        "--config-file", "-c",
        default=DEFAULT_CONFIG_FILE,
        help="Allows to specify .json file from which program will attempt read urls.",
    )
    parser.add_argument(
        "--operation-mode", "-o",
        type=OperationMode.from_str,
        help="Choose operation mode for this script:\n"
             " - text | t   -- in this mode program tracks changes to the text contents of the website\n"
             " - layout | l -- track changes to the layout of tha page"
    )
    namespace = parser.parse_args()
    return namespace.operation_mode, namespace.config_file


def main():
    operation_mode, config_file = command_line_interface()
    if config_file is None:
        config_file = DEFAULT_CONFIG_FILE
    website_state_lookup: dict[URL, Optional[WebsiteState]] = defaultdict(lambda: None)
    ui.log_config(ConfigInfo(operation_mode, config_file))
    with open(config_file, "r", encoding="utf-8") as urls:
        for url in JSONDecoder().decode(urls.read())["urls"]:
            check_website(url, website_state_lookup, operation_mode=operation_mode)
        scheduler.run()


if __name__ == "__main__":
    main()
