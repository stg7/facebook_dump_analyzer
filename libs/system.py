#!/usr/bin/env python3
"""
    System

    system helper functions

    author: Steve Göring
    contact: stg7@gmx.de
    2014
"""
import os


def read_file(file_name, enc="latin-1"):
    """
    read a text file into a string
    :file_name file to open
    :return content as string
    """
    f = open(file_name, "r", encoding=enc)
    content = "".join(f.readlines())
    f.close()
    return content


def create_dir_if_not_exists(dir):
    try:
        os.stat(dir)
    except:
        os.mkdir(dir)

if __name__ == "__main__":
    print("\033[91m[ERROR]\033[0m lib is not a standalone module")
    exit(-1)
