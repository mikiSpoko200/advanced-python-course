#!/usr/bin/python
# -*- coding: utf-8 -*-


class MyMeta(type):

    def __new__(mcs, name, bases, namespace, **kwargs):
        cls = super().__new__(mcs, name, bases, namespace, **kwargs)


def main():
    print("Hello World!")


if __name__ == "__main__":
    main()
