from copy import deepcopy
from collections import defaultdict, Counter
from rich import print

import pyperclip
from aoc.files import readlines


def pr(s):
    print(s)
    pyperclip.copy(str(s))


if __name__ == "__main__":
    print(f"Starting {__file__}")
    data = readlines(9)
    sample = """
    """
    # Comment out this line to use actual data
    data = sample
