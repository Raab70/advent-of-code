import re
from collections import defaultdict

from rich import print

from aoc.files import readlines
from aoc.grid import grow_region, perimeter
from aoc.pr import pr


def sides(pts):
    # To find sides we actually count corners, look for a 2x2 square that is a corner
    sides = 0
    for x, y in pts:
        for nx, ny, x1, y1, x2, y2 in [
            (x + 1, y, x, y - 1, x + 1, y - 1),  # Right, Up, Up-Right
            (x - 1, y, x, y - 1, x - 1, y - 1),  # Left, Up, Up-Left
            (x, y + 1, x - 1, y, x - 1, y + 1),  # Down, Left, Down-Left
            (x, y - 1, x - 1, y, x - 1, y - 1),  # Up, Left, Up-Left
        ]:
            on_edge = (nx, ny) not in pts
            if not on_edge:
                continue
            if not ((x1, y1) in pts and (x2, y2) not in pts):
                print(x, y, nx, ny, x1, y1, x2, y2)
                sides += 1
    return sides


if __name__ == "__main__":
    day_no = int(re.search(r"day(\d+).py", __file__).group(1))
    print(f"Starting Day {day_no}")
    data = readlines(day_no)
    sample = """
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
    """.strip().split("\n")
    # Comment out this line to use actual data
    data = sample

    # Part 1
    regions = defaultdict(list)
    seen = set()
    for y in range(len(data)):
        for x in range(len(data[y])):
            if (x, y) not in seen:
                region, seen = grow_region(data, x, y, seen)
                regions[data[y][x]].append(region)

    # Price = area * perimeter
    s = 0
    s2 = 0
    for k, vl in regions.items():
        for r in vl:
            area = len(r)
            p = perimeter(r)
            n_sides = sides(r)
            s += area * p
            s2 += area * n_sides

    pr(s)
    pr(s2)
