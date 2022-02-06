#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("some_arg", help="Template for casual python script")
    args = parser.parse_args()
    print("Hello World!")


if __name__ == "__main__":
    main()
