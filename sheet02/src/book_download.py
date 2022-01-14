#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import urllib.request
import itertools
import textwrap
import shutil
from bs4 import BeautifulSoup


# Following link redirects to book "Heart of Darkness" by Joseph Conrad published under guntenberg project.
HEART_OF_DARKNESS_URL = r"https://www.gutenberg.org/files/219/219-h/219-h.htm#link2H_4_0003"


def download(url: str, file_name: str) -> None:
    """Download contents of website specified and store in <file_name>.html."""
    with urllib.request.urlopen(url) as data:
        with open(file_name + ".html", "w", encoding="utf-8") as temp:
            temp.writelines(data.read().decode("utf-8"))


def process(file_name: str) -> None:
    """Attempt to format book from guntenberg.org and store it in <file_name>.txt."""
    with open(file_name + ".html", "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
        chapters = soup.find_all("div", class_="chapter")
        text = []
        for chapter in chapters:
            for paragraph in itertools.chain(chapter.find_all("h2"), chapter.find_all("p")):
                text.append(textwrap.fill(paragraph.text + '\n', width=72))
    with open(file_name + ".txt", "w", encoding="utf-8") as out:
        out.writelines(text)


def download_heart_of_darkness() -> None:
    """Download Heart of Darkness."""
    download(HEART_OF_DARKNESS_URL, "Heart of Darkness")


def process_heart_of_darkness() -> None:
    """Process Heart of Darkness."""
    process("Heart of Darkness")


def main():
    download_heart_of_darkness()
    process_heart_of_darkness()


if __name__ == "__main__":
    main()
