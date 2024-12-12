import re
from collections import Counter, defaultdict
from copy import deepcopy

from rich import print

from aoc.files import readlines
from aoc.pr import pr


def is_adj(x, y, x2, y2):
    return abs(x - x2) + abs(y - y2) == 1


def is_oob(data, x, y):
    maxx = len(data[0])
    maxy = len(data)
    if x < 0 or y < 0 or x >= maxx or y >= maxy:
        return True
    return False


def merge_regions(regions):
    merged = []
    midx = set()
    for i, r in enumerate(regions):
        for j, r2 in enumerate(regions):
            if i == j:
                continue
            done = False
            for v in r:
                x, y = v
                for v2 in r2:
                    x2, y2 = v2
                    if is_adj(x, y, x2, y2):
                        # print(f"Merging {i},{j} bc of {x}, {y} and {x2}, {y2}")
                        if i not in midx and j not in midx:
                            merged.append(list(set(regions[i] + regions[j])))
                            midx.add(i)
                            midx.add(j)
                        done = True
                        break
                if done:
                    break
    # Anything not merged must be included
    for i, r in enumerate(regions):
        if i not in midx:
            merged.append(r)
    n_merged = len(midx)
    print(f"Merged {n_merged} regions")
    return merged, n_merged


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
    # data = sample

    # Part 1
    # TODO: Please stop merging...
    regions = defaultdict(list)
    curr = None
    for y, line in enumerate(data):
        # Split each line into distinct characters
        for x, c in enumerate(line):
            if c == curr:
                regions[c].append((x, y))
            else:
                curr = c
                regions[c].append((x, y))
    # Now count the contiguous regions for each character
    rr = defaultdict(list)
    rrr = defaultdict(list)
    # regions = {k: v for k, v in regions.items() if k == "I"}
    for k, vl in regions.items():
        # Break the list vl into a list of lists of contiguous regions
        for v in vl:
            x, y = v
            found = False
            for r in rr[k]:
                for v2 in r:
                    x2, y2 = v2
                    if is_adj(x, y, x2, y2):
                        r.append(v)
                        found = True
                        break
            if not found:
                rr[k].append([v])
        # Once all items are processed, merge any regions that are adjacent
        while True:
            rr[k], num_merged = merge_regions(rr[k])
            if num_merged == 0:
                break

    # Price = area * perimeter
    s = 0
    for k, vl in rr.items():
        for r in vl:
            perimeter = 0
            area = len(r)
            for v in r:
                x, y = v
                for x2, y2 in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                    if (x2, y2) not in r:
                        perimeter += 1

            n_sides = 0
            for x, y in r:
                for nx, ny, x1, y1, x2, y2 in [
                    (x + 1, y, x, y - 1, x + 1, y - 1),
                    (x - 1, y, x, y - 1, x - 1, y - 1),
                    (x, y + 1, x - 1, y, x - 1, y + 1),
                    (x, y - 1, x - 1, y, x - 1, y - 1),
                ]:
                    if (nx, ny) not in r and not ((x1, y1) in r and (x2, y2) not in r):
                        n_sides += 1
            s += area * n_sides

    pr(s)
