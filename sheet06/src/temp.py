#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Exercise 2. Implement a website monitoring system that checks if a page has changed its content.
We assume that our program can monitor more than one page; we also assume that checking takes
place periodically (e.g. every 1 minute).
In this task we assume that page layout changes rarely, only individual elements of this layout are
changed, so if the program detects a change, it must return only what has changed.
"""

"""
What i learned for this lab:
For quite some time a wanted to get into parallel/concurrent programming.
I had a vague notion of the meaning of terms such as process, thread, coroutine
asynchronous programming in particular term asyncIO which prevents programs from stalling
on long IO operations such as awaiting for user input or network request.


Do more reading on:
- file descriptors,
- epoll and select in async context 


My learning resources:
introduction to asyncio in python: https://www.youtube.com/watch?v=3mb9jFAHRfw&ab_channel=PyConAU            
MSDN article broadly touching on the topic: https://docs.microsoft.com/en-gb/windows/win32/procthread/about-processes-and-threads?redirectedfrom=MSDN
Simplified overview of async mechanism in rust: 
 - https://youtu.be/ThjvMReOXYM
 - https://youtu.be/9_3krAQtD2k
Chapter 10.5: "asyncio: Asynchronous I/O, Event Loop, and Concurrency Tools" of "the Python 3 Standard Library by Example" 
"""


import argparse
import difflib
import sched
import json
import time
from urllib.request import Request
from typing import Optional, ParamSpec, Callable


"""
Program description:
    1. Simple user interface that loads urls to track from a json file or commandline input
    2. Coloring scheme based on the outcome of check:
        - green -- change
        - blue  -- no change
        - red   -- error
    3. There are two mods of operation:
        - text change only mode -- checks only for changes in pages text
        - layout change         -- detects both changes in text and in it's layout on the page (HTML)
    4. Probably should use asyncIO for non-blocking operations.
    5. Program holds a dictionary that matches website's url to its contents. On every iteration of main
       even loop it fetches new content, compares results and acts accordingly.
    6. In pure layout mode using only urllib will suffice but for text changes it would be much more convenient
       to use BeautifulSoup.
    7. As of now my contents revolved around using some kind of scheduler that invokes a check for each website
       based on some clock. In case user specifies a lot of pages to track I imagine that program can choke due
       to IO stalling and let's say one iteration of event loop takes 100s. I don't want my program to wait another 60s.
       It should start working as soon as possible and notify end user about the delay.
    7.1. A cool feature would be to allow user to specify priority levels for certain websites and based on that system 
       would prioritize checking these websites on time and in case of failure to keep up for the highest priority crash or sth?
 
"""


__VERSION__ = "0.0.1"


url = str


def cli() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("", help="Template for casual python script")
    args = parser.parse_args()


def load_urls(path: str) -> list[url]:
    with open(path, "r", encoding="utf-8") as urls:
        dec = json.JSONDecoder()
        return dec.decode(urls.read())


def check_for_changes(url: url) -> Optional[tuple[str, str]]:
    pass
        

def monitor_urls(urls: list[url]) -> None:
    scheduler = sched.scheduler(time.time, time.sleep)
    for
    scheduler.enter()


def main():
    comparator = difflib.Differ()


if __name__ == "__main__":
    main()
