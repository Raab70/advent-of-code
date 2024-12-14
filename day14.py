import re
import sys
from collections import Counter

from rich import print
from tqdm import tqdm

from aoc.files import readlines
from aoc.pr import pr


def step(r, maxx, maxy):
    newr = []
    for x, y, vx, vy in r:
        x += vx
        y += vy
        # If the new position is out of bounds, wrap around
        newr.append((x % maxx, y % maxy, vx, vy))
    return newr


if __name__ == "__main__":
    day_no = int(re.search(r"day(\d+).py", __file__).group(1))
    print(f"Starting Day {day_no}")
    data = readlines(day_no)
    maxx = 101
    maxy = 103

    sample = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
""".strip().split("\n")
    # Comment out these lines to use actual data
    # data = sample
    # maxx = 11
    # maxy = 7

    r = []
    for line in data:
        x, y, vx, vy = map(int, re.findall(r"-?\d+", line))
        r.append((x, y, vx, vy))

    for i in range(100):
        r = step(r, maxx, maxy)

    # Count the robots in each quadrant, ignoring the ones in the middle
    c = Counter()
    for x, y, _, _ in r:
        c[(x, y)] += 1
    midx = maxx // 2
    midy = maxy // 2
    q1 = sum(v for k, v in c.items() if k[0] < midx and k[1] < midy)
    q2 = sum(v for k, v in c.items() if k[0] > midx and k[1] < midy)
    q3 = sum(v for k, v in c.items() if k[0] > midx and k[1] > midy)
    q4 = sum(v for k, v in c.items() if k[0] < midx and k[1] > midy)
    pr(q1 * q2 * q3 * q4)

    # Part 2
    def print_grid_pts(r):
        grid = [["." for _ in range(maxx)] for _ in range(maxy)]
        for x, y, _, _ in r:
            grid[y][x] = "#"
        for row in grid:
            print("".join(row))

    # Reload the data for part 2
    data = readlines(day_no)
    maxx = 101
    maxy = 103

    r = []
    for line in data:
        x, y, vx, vy = map(int, re.findall(r"-?\d+", line))
        r.append((x, y, vx, vy))

    for i in tqdm(range(100_000)):
        r = step(r, maxx, maxy)
        # If we have a cluster of 9 robots in a row, print
        for y in range(maxy):
            row = sorted([rx for rx, ry, _, _ in r if ry == y])
            s = 1
            for j in range(1, len(row)):
                if row[j] - row[j - 1] == 1:
                    s += 1
                    if s == 9:
                        print_grid_pts(r)
                        pr(i + 1)
                        sys.exit()
                else:
                    s = 1
