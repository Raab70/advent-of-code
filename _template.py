import re
import sys
from collections import Counter, defaultdict
from copy import deepcopy

from rich import print
from tqdm import tqdm
from aocd.models import Puzzle

from aoc.pr import pr

sys.setrecursionlimit(10 ** 6)

if __name__ == "__main__":
    day_no = int(re.search(r"day(\d+).py", __file__).group(1))
    puzzle = Puzzle(year=2024, day=day_no)
    print(f"Starting Day {day_no}")
    data = puzzle.input_data.splitlines()
    # Comment out this line to use actual data
    # data = puzzle.examples[0].input_data.splitlines()

    # Part 1
    a = None
    pr(a)
    # puzzle.answer_a = a

    # Part 2
    b = None
    pr(b)
    # puzzle.answer_b = b
