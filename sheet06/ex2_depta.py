#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Exercise 2. Implement a website monitoring system that checks if a page has changed its content.
We assume that our program can monitor more than one page; we also assume that checking takes
place periodically (e.g. every 1 minute).
In this task we assume that page layout changes rarely, only individual elements of this layout are
changed, so if the program detects a change, it must return only what has changed.

What I learned for this lab:
For quite some time a wanted to get into parallel/concurrent programming.
I had a vague notion of the meaning of terms such as process, thread, coroutine
asynchronous programming in particular term asyncIO which prevents programs from stalling
on long IO operations such as awaiting for user input or network request.


TODO: Do more reading on:
    - file descriptors,
    - epoll and select in async context


My learning resources:
introduction to asyncio in python: https://www.youtube.com/watch?v=3mb9jFAHRfw&ab_channel=PyConAU
MSDN article broadly touching on the topic: https://docs.microsoft.com/en-gb/windows/win32/procthread/about-processes-and-threads?redirectedfrom=MSDN
Simplified overview of async mechanism in rust:
 - https://youtu.be/ThjvMReOXYM
 - https://youtu.be/9_3krAQtD2k
Chapter 10.5: "asyncio: Asynchronous I/O, Event Loop, and Concurrency Tools"
of "the Python 3 Standard Library by Example".
"""
import itertools
import os

"""
Program description:
    
    This program tracks 'changes' in websites on 60s basis.
    
    There are two mods of operation:
        - text change only mode -- checks only for changes in pages text
        - layout change         -- detects both changes in text and in it's layout on the page (HTML)
    
    Webpage is represented by it's title parsed from HTMl on initial parsing and it's not updated even if title changes.
    If webpage code does not contain title tag url is used instead.


    1. Simple user interface that reads string representation of 
    2. Coloring scheme based on the outcome of check:
        - green -- change
        - blue  -- no change
        - red   -- error
    5. Program holds a dictionary that matches website's url to its contents. On every iteration of main
       even loop it fetches new content, compares results and acts accordingly.
    6. In pure layout mode using only urllib will suffice but for text changes it would be much more convenient
       to use BeautifulSoup.
    7. As of now my contents revolved around using some kind of scheduler that invokes a check for each website
       based on some clock. In case user specifies a lot of pages to track I imagine that program can choke due
       to IO stalling and let's say one iteration of event loop takes 100s. I don't want my program to wait another 60s.
       It should start working as soon as possible and notify end user about the delay.
    7.1. A cool feature would be to allow user to specify priority levels for certain websites and based on that system textwrap.shorten
       would prioritize checking these websites on time and in case of failure to keep up for the highest priority crash or sth?

"""


import argparse
import difflib
import sched
import enum
import http_error_codes
import textwrap as tw
from collections import defaultdict
from bs4 import BeautifulSoup
from json.decoder import JSONDecoder
from typing import NamedTuple, Optional
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from datetime import datetime
from termcolor import colored


__VERSION__ = "0.0.1"

"""
Alternative solution to that would be using signal module which provides us with functionality
there we could use 
signal.setitimer(signal.ITIMER_REAL, 60) -- this would every 60s schedule SIGALRM signal.
We could than add a signal handler with 
signal.signal(signal.SIGALRM, <our function for checking webpages>)

But this unfortunately does not work under windows.

We can however use the sched module included in standard library.

However this solution will be blocking.
"""

scheduler = sched.scheduler()
DEFAULT_DATETIME_FORMAT = "%d-%m-%Y %H:%M:%S"
CHECKING_PERIOD = 10

# Adding such fake headers makes it more difficult for servers to detect that our it is in face python script
# that is trying to gain access to some resources. Some services block such connections on purpose so that
# programmers use their API instead.
HTTPS_HEADER: dict[str, str] = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}

URL = str


class WebsiteState(NamedTuple):
    check_timestamp: str
    content: list[str]
    title: str


class OperationMode(enum.Enum):
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


def schedule_website_check(
        url: URL,
        website_state_lookup: dict[URL, Optional[WebsiteState]], *,
        operation_mode: OperationMode,
        delay: int = CHECKING_PERIOD) -> None:
    """Schedules website check in delay seconds."""
    scheduler.enter(delay, 1, check_website, (url, website_state_lookup), {"operation_mode": operation_mode})


def log_communicate(state: WebsiteState, communicat: str) -> None:
    """Default stdio communicate logging template."""
    print(f"{state.check_timestamp} :: {communicat} :: {state.title}")


def log_initial(state: WebsiteState) -> None:
    """Log information about initial website processing."""
    log_communicate(state, colored("New website added  ", color="blue"))


def log_error(state: WebsiteState, errmsg: str) -> None:
    """Log information about request error."""
    log_communicate(state, colored(f"ERROR :: {errmsg}", on_color="red"))


def log_change(state: WebsiteState, changes: list[str]) -> None:
    """Log information about website state change."""
    log_communicate(state, colored("Changes detected   ", color="green"))
    for change in changes:
        if change[0] == "-" and change[:3] != "---":
            change = colored(change, color="red")
        if change[0] == "+" and change[:3] != "+++":
            change = colored(change, color="green")
        if change[:2] == "@@":
            change = colored(change, color="blue")
        print(tw.fill(
            change,
            width=os.get_terminal_size().columns - 10,
            initial_indent="\t",
            subsequent_indent="\t")
        )


def log_no_change(state: WebsiteState) -> None:
    """Log information about website state change."""
    log_communicate(state, colored("No changes detected", color="yellow"))


def process_content(content: list[str]) -> list[str]:
    return list(filter(lambda line: line != "\n", content))


def check_website(url: URL, website_state_lookup: dict[URL, Optional[WebsiteState]], *,
                  operation_mode: OperationMode) -> None:
    """Check for changes in a website that can be accessed via *url*.

    TODO:
        * Add description of actions taken when checking a website for the first time.
            - Parsing for title -- add this field to the WebsiteState datastruct.
        * Add status printing to the stdout.
        *'. Maybe add coloring based on the outcome of check?:
            - green  -- no change
            - yellow -- a change
            - red    -- some connection or access error.
        * If connection for some reason failed don't retry -- already done -- no scheduling after failure.

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
        with urlopen(req) as response:
            soup = BeautifulSoup(response.read(), features="html.parser")
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
                log_initial(curr_state)
            # actual comparison and appropriate logging.
            else:
                changes = list(difflib.unified_diff(
                    prev_state.content, curr_state.content,
                    "Previous version", "Current version",
                    prev_state.check_timestamp, curr_state.check_timestamp,
                    n=3
                ))
                if changes:
                    log_change(curr_state, changes)
                else:
                    log_no_change(curr_state)

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


def command_line_interface() -> OperationMode:
    parser = argparse.ArgumentParser(description="Track changes in websites.")
    parser.add_argument(
        "--operation-mode", "-o",
        type=OperationMode.from_str,
        help="Choose operation mode for this script:\n"
             " - text | t   -- in this mode program tracks changes to the text contents of the website\n"
             " - layout | l -- track changes to the layout of tha page"
    )
    namespace = parser.parse_args()
    return namespace.operation_mode


def main():
    operation_mode = command_line_interface()
    website_state_lookup: dict[URL, Optional[WebsiteState]] = defaultdict(lambda: None)
    print(f"Running web surveillance in {colored(operation_mode, color='cyan')}.")
    with open("config.json", "r", encoding="utf-8") as urls:
        for url in JSONDecoder().decode(urls.read())["urls"]:
            check_website(url, website_state_lookup, operation_mode=operation_mode)
        scheduler.run()


if __name__ == "__main__":
    main()
