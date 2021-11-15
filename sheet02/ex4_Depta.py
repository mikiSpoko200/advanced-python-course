#!/usr/bin/python
# -*- coding: utf-8 -*-

import io
import random
import os
from typing import overload, TextIO
from textwrap import fill

import book_download

"""NOTE:
I chose to demonstrate how my program functions on a book "Heart of Darkness" by Joseph Conrad.
Link to the book published under project Gunteberg so it's legal for me to download it.
I prepared a separate script 'book_download.py' that handles the logic of downloading the .html file
and converting it into the .txt format. 
By default it will be automatically invoked upon running this script unless
a "Heart of Darkness.txt" file exists in current working directory or global variable 'NO_DOWNLOAD'
defined below is set to True.
"""
HEART_OF_DARKNESS_URL = r"https://www.gutenberg.org/files/219/219-h/219-h.htm#link2H_4_0003"
NO_DOWNLOAD = False
PRINT_N_SENTENCES = float("inf")  # defines how many sentence transformations should be printed to stdout.

# defines if converted sentences should be printed
# if False only sentence minimal length is asserted.
PRINT_CONVERSION = True

# algorithm parameters
WORD_LENGTH = 10
WORN_NUMBER = 5

__book_title = "Heart of Darkness"
__file_name = __book_title + ".txt"


@overload
def simplify_sentence(text: str, word_length: int, word_number: int) -> str: ...


@overload
def simplify_sentence(text: TextIO, word_length: int, word_number: int) -> str: ...


def simplify_sentence(text: str | TextIO, word_length: int, word_number: int) -> str:
    """Simplify sentence by removing certain words.
    Firstly remove all words longer than word_length.
    If after the first step sentence is still longer than word_number then remove words at random.
    Function accepts either string or TextIO (string stream) for bigger data sets.

    Formatting assumptions:
        For following algorithm to work, text needs to end with a dot i.e. all sentences must be 'closed'.
        Also this (very simple) algorithm can produce very bizarre outcome when processing text with abbreviations.
        For example:
            "Hello World! i.e. have a nice day."
        the abbreviation 'i.' would be treated as ending of following sentence, and 'e.' as one letter long sentence.
        This is where this exercise gets from manageable to very difficult as there is no simple way of fixing this
        issue. One could implement function that tries to determine if a particular dot in fact represents and ending
        of a sentence but, frankly, that's beyond my capabilities and amount of time available :/.
    """
    # turn string into in-memory stream for polymorphic behaviour.
    text = io.StringIO(text) if isinstance(text, str) else text

    prev_sentence_ending = ""
    while (chunk := text.read(4096)) != "":
        sentence_closed = chunk[-1] == "."
        sentences = [" ".join(sentence.split("\n")) for sentence in chunk.split(".") if sentence]
        # add all that remained from last chunk.
        sentences[0] += prev_sentence_ending.strip()
        # if chunk cut sentence in two store it.
        if not sentence_closed:
            prev_sentence_ending = sentences.pop()

        # format sentences and yield results from them
        def remove_random(words: list[str]) -> list[str]:
            if (diff := len(words) - word_number) > 0:
                to_delete = set(random.sample(range(len(words)), diff))
                return [word for i, word in enumerate(words) if i not in to_delete]
            else:
                return words

        for sentence in sentences:
            words = [word.strip() for word in sentence.split(" ") if word]
            short_words = [word for word in words if word and len(word) <= word_length]
            trimmed = remove_random(short_words)
            formatted_sentence = " ".join(trimmed) + "."
            yield formatted_sentence


def main():
    if not NO_DOWNLOAD and not os.path.exists(__file_name):
        print(f"Downloading {__file_name} ...")
        book_download.main()
        print("Download successful!")
    with open(__file_name, "r", encoding="utf-8") as file:
        data = file.read()
        sentences = ["".join(sentence.split("\n")) for sentence in data.split(".") if sentence]
        for index, (sentence, stripped) in enumerate(zip(
                    sentences,
                    simplify_sentence(data, WORD_LENGTH, WORN_NUMBER))):
            if index > PRINT_N_SENTENCES - 1:
                break
            if PRINT_CONVERSION:
                print(f"{index + 1}.", "-" * 80)
                print(f"{fill(sentence)}.\n==>\n{fill(stripped)}")
            # slice - removes dot, split - gets words.
            words = stripped[:-1].split(" ")
            assert len(words) <= 5
            assert all(len(word) <= WORD_LENGTH for word in words)


if __name__ == "__main__":
    main()
