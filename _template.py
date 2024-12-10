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
    day_no = __file__.split("/")[-1].split(".")[0]
    data = readlines(day_no)
    sample = """
    """
    # Comment out this line to use actual data
    data = sample
