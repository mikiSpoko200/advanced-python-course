#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import book_download

"""
This script similarly to ex4 operates on downloaded file in order to test algorithms performance for big data.
The same downloading rules apply.
"""

HEART_OF_DARKNESS_URL = r"https://www.gutenberg.org/files/219/219-h/219-h.htm#link2H_4_0003"
NO_DOWNLOAD = False

__book_title = "Heart of Darkness"
__file_name = __book_title + ".txt"


CompressedText = list[tuple[str, int]]


def compression(text: str) -> CompressedText:
    """Compress text into list of pairs (<character>, <number of consecutive appearances>).

    To be fair it's a pretty terrible compression algorithm.
    Or more precisely not algorithm itself but it's implementation in python in form of list[tuple[str, int]].
    Empty list alone generates 56 bytes of overhead. From my testing it breaks even in terms of memory footprint if
    string contains nothing but 40 repetitions of the same character.
    """

    compressed = []
    text_iter = iter(text)
    current_char = next(text_iter)
    repeats = 1
    for letter in text_iter:
        if letter == current_char:
            repeats += 1
        else:
            compressed.append((current_char, repeats))
            current_char = letter
            repeats = 1
    compressed.append((current_char, repeats))
    return compressed


def decompression(compressed_text: CompressedText) -> str:
    """Recreate original string from a CompressedText."""
    return "".join([char * freq for char, freq in compressed_text])


def compression_efficiency(compressed_text: CompressedText) -> float:
    """Calculate the ratio of compressed text memory footprint to uncompressed string representation."""
    return sys.getsizeof(compressed_text) / sys.getsizeof(decompression(compressed_text)) * 100.0


def main():
    if not NO_DOWNLOAD and not os.path.exists(__file_name):
        print(f"Downloading {__file_name} ...")
        book_download.main()
        print("Download successful!")
    print(f"'Compressing' {__file_name}")
    with open(__file_name, "r", encoding="utf-8") as file:
        decompressed = file.read()
        compressed = compression(decompressed)
        print(f"decompressed text memory usage = {(size_d := sys.getsizeof(decompressed)) // 1024} kB")
        print(f"compressed text memory usage = {(size_c := sys.getsizeof(compressed)) // 1024} kB")
        print(f"compressed ~= {size_c / size_d:.2f} * decompressed")


if __name__ == "__main__":
    main()

"""
Results:
    As we can see out 'compression' algorithm bloats memory usage only slightly over four times.
    Again if it wasn't for python object memory overhead this could be a viable method for code
    json or anything with high number of repeating characters.
"""
