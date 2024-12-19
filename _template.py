import re
import sys
from collections import Counter, defaultdict
from copy import deepcopy

from rich import print
from tqdm import tqdm

from aoc.files import readlines
from aoc.pr import pr

sys.setrecursionlimit(10 ** 6)

if __name__ == "__main__":
    day_no = int(re.search(r"day(\d+).py", __file__).group(1))
    print(f"Starting Day {day_no}")
    data = readlines(day_no)
    sample = """
    """
    # Comment out this line to use actual data
    data = sample
