import re
from copy import deepcopy
from collections import defaultdict, Counter
from rich import print

from aoc.files import readlines
from aoc.pr import pr


if __name__ == "__main__":
    day_no = int(re.search(r"day(\d+).py", __file__).group(1))
    print(f"Starting Day {day_no}")
    data = readlines(day_no)
    sample = """
    """
    # Comment out this line to use actual data
    data = sample
