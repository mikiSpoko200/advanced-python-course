#!/usr/bin/python
# -*- coding: utf-8 -*-


import unicodedata
from typing import Callable


def normalize_unicode(func: Callable[[str], bool]) -> Callable[[str], bool]:
    """Performs unicode NFKD normalization on function arugment."""

    def wrapper(text: str) -> bool:
        return func(unicodedata.normalize("NFKD", text))

    return wrapper


@normalize_unicode
def is_palindrome(text: str) -> bool:
    """Determine if passed text is a palindrome. Ignore all but unicode alphabetic characters.

    ***authors reflection regarding the topic***
    Gosh I thought I was being clever when i used str.isalpha as filter predicate.
    Now having spent a day trying to understand Unicode casefolding and caseless comparison pitfalls...
    I just feel silly now. Beginning to think that timezones aren't that bad after all.
    As it turns out human languages are messengers of chaos and Im just so so grateful
    that I don't have to study linguistics.

    But to the point...
    Correction after lab2:
    Unfortunately in some languages capitalization and lowering aren't each others inverse functions.
    As the following lowercase(capitalize(x)) ≡ lowercase(x) is not true for any arbitrary x.
    There are many counter examples such as german ß, which is lowercase letter so lower() would leave it as is,
    but capital ß is written as 'Ss' so it would get lowered to 'ss' which in turn would return false negative result.

    documentation for str.lower():
    > Return a copy of the string with all the cased characters converted to lowercase.
    > The lowercasing algorithm used is described in section 3.13 of the Unicode Standard

    documentation for str.casefold():
    > Return a casefolded copy of the string. Casefolded strings may be used for caseless matching.
    > Casefolding is similar to lowercasing but more aggressive because it is intended to remove all case
    > distinctions in a string. For example, the German lowercase letter 'ß' is equivalent to "ss".
    > Since it is already lowercase, lower() would do nothing to 'ß'; casefold() converts it to "ss".
    > The **casefolding** algorithm is described in section 3.13 of the Unicode Standard.

    str.casefold() solves these problems as it's main purpose, according to documentation,
    is to provide means for caseless comparison.

    But it would be just a little too perfect if that would solve all our problems.
    From what I gathered there still is the issue of accents e.g
    #>>> "ê".foldcase() == "ê".foldcase()
    false

    These we can handle with help of Unicode normalized forms.
    link: http://www.unicode.org/reports/tr15/#Normalization_Forms_Table

    It's quite a long document and unfortunately the didn't provide TL;DR
    There's a few posts discussing it over on stack overflow.
    link: https://stackoverflow.com/questions/319426/how-do-i-do-a-case-insensitive-string-comparison

    I made a simple wrapper
    """
    processed_text = list(filter(str.isalpha, text.casefold()))
    return processed_text == processed_text[::-1]


def main():
    print(f"{is_palindrome('Eine güldne, gute Tugend: Lüge nie!') = }")
    print(f"{is_palindrome('Kobyła ma mały bok.') = }")
    print(f"{is_palindrome('rotor') = }")
    print(f"{is_palindrome('tgtß') = }")
    print(f"{is_palindrome('êê') = }")


if __name__ == "__main__":
    main()
