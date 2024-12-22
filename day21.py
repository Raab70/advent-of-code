import re
import sys
from functools import cache

from rich import print

from aoc.grid import Point
from aoc.pr import pr

sys.setrecursionlimit(10**9)
CACHE = {}
DIRS = {
    "^": Point(0, -1),
    "v": Point(0, 1),
    "<": Point(-1, 0),
    ">": Point(1, 0),
}
DIRS_INVERSE = {
    Point(0, -1): "^",
    Point(0, 1): "v",
    Point(-1, 0): "<",
    Point(1, 0): ">",
}


def build_gd(grid):
    grid_dict = {}
    for j, row in enumerate(grid):
        for i, val in enumerate(row):
            if val is None:
                continue
            grid_dict[val] = Point(i, j)

    return grid_dict


def play_buttons(button_str, grid_dict):
    gdr = {v: k for k, v in grid_dict.items()}
    start = grid_dict["A"]
    # print(f"Starting at {start}")
    out = ""
    curr_loc = start
    for char in button_str:
        if char == "A":
            out += gdr[curr_loc]
        else:
            curr_loc += DIRS[char]
    return out


@cache
def get_pos_opts(pos, newpos, depth, partial_row):
    if pos.x < newpos.x:
        h = ">" * (newpos.x - pos.x)
    elif pos.x > newpos.x:
        h = "<" * (pos.x - newpos.x)
    else:
        h = ""
    if pos.y < newpos.y:
        v = "v" * (newpos.y - pos.y)
    elif pos.y > newpos.y:
        v = "^" * (pos.y - newpos.y)
    else:
        v = ""

    if h == "":
        opts = [v]
    elif v == "":
        opts = [h]
    elif pos.x == 0 and newpos.y == partial_row:
        opts = [h + v]
    elif newpos.x == 0 and pos.y == partial_row:
        opts = [v + h]
    else:
        opts = [h + v, v + h]

    def bestopts():
        for i in opts:
            yield find_best(i + "A", depth - 1, True)

    return min(bestopts())


if __name__ == "__main__":
    day_no = int(re.search(r"day(\d+).py", __file__).group(1))
    print(f"Starting Day {day_no}")
    data = """
129A
540A
789A
596A
582A
""".strip().splitlines()
    sample = """
029A
980A
179A
456A
379A
""".strip().splitlines()
    # Comment out this line to use actual data
    # data = sample

    grid = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], [None, "0", "A"]]
    gdn = build_gd(grid)
    grid2 = [
        [None, "^", "A"],
        ["<", "v", ">"],
    ]
    gdd = build_gd(grid2)

    def find_best(code, depth, is_directional):
        # print(f"Finding best for {code} with depth {depth} and is_directional {is_directional}")
        if depth <= 0:
            return len(code)
        res = 0
        grid = gdd if is_directional else gdn
        partial_row = 0 if is_directional else 3
        start = grid["A"]
        for c in code:
            end = grid[c]
            res += get_pos_opts(start, end, depth, partial_row)
            start = end
        return res

    def get_complexity(data, depth):
        c = 0
        for line in data:
            ans = find_best(line, depth, False)
            c += ans * int(re.search(r"(\d+)", line).group(1))
        return c

    # Find the length of the shortest sequence and the numeric part of the code and multiply
    print("Part 1")
    pr(get_complexity(data, 3))

    print("Part 2")
    pr(get_complexity(data, 26))
