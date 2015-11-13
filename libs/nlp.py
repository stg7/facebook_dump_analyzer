#!/usr/bin/env python3
"""
    Nlp

    nlp helper functions

    author: Steve Göring
    contact: stg7@gmx.de
    2014
"""
import os

from system import read_file


_german_stop_words = set([x.lower() for x in read_file(os.path.dirname(os.path.realpath(__file__)) + "/german_stop_words", enc="utf-8").split("\n")])

def german_stop_words():
    return _german_stop_words

if __name__ == "__main__":
    print("\033[91m[ERROR]\033[0m lib is not a standalone module")
    exit(-1)
