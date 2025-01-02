import re
import sys

from aocd.models import Puzzle
from rich import print

from aoc.pr import pr

sys.setrecursionlimit(10**6)

if __name__ == "__main__":
    day_no = int(re.search(r"day(\d+).py", __file__).group(1))
    puzzle = Puzzle(year=2024, day=day_no)
    print(f"Starting Day {day_no}")
    data = puzzle.input_data.splitlines()
    # Comment out this line to use actual data
    # data = puzzle.examples[0].input_data.splitlines()

    # If the top row is #, it's a lock, else key
    # Each lock/key is a list of heights
    locks = []
    keys = []
    # Each key is 8 lines long with the last one being blank
    for i in range(0, len(data), 8):
        ds = data[i : i + 7]
        curr = []
        val = ds[0][0]
        for j in range(len(ds[0])):
            curr.append(sum(d[j] == "#" for d in ds) - 1)
        if val == "#":
            locks.append(curr)
        else:
            keys.append(curr)

    # Part 1
    # How many unique lock/key pairs fit together without overlapping in any column?
    def match(lock, key):
        if len(lock) != len(key):
            return False
        if all((lo + k) <= 5 for lo, k in zip(lock, key)):
            return True
        return False

    a = 0
    for lock in locks:
        for key in keys:
            if match(lock, key):
                # print(f"Lock {lock} and key {key} fit!")
                a += 1
            else:
                pass
                # print(f"Lock {lock} and key {key} [red]overlap[/red]!")
    pr(a)
    puzzle.answer_a = a
