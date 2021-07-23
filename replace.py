#!/usr/bin/env python3
import sys
import fileinput


def replace_text(path, what, text):
    with fileinput.FileInput(path, inplace=True) as file:
        for line in file:
            print(line.replace(what, text), end='')


if __name__ == "__main__":
    replace_text(sys.argv[1], sys.argv[2], sys.argv[3])
