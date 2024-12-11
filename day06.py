from collections import Counter
from copy import deepcopy

from rich import print
from tqdm import tqdm

from aoc.files import readlines

data = readlines(6)

GU = "^"
GR = ">"
GD = "V"
GL = "<"
OBS = "#"
MARK = "X"
# The guard moves up until they hit an obstacle, turn right 90 degrees, continue
# Count the number of distinct positions on the map they visit

sample = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
""".split("\n")
# data = sample


def replace_char(s, i, c):
    return s[:i] + c + s[i + 1 :]


def move_guard(data):
    gy = [(GU in lst or GR in lst or GD in lst or GL in lst) for lst in data].index(
        True
    )
    # Find out which guard is in the row
    if GU in data[gy]:
        gx = data[gy].index(GU)
        new_gy = gy - 1
        new_gx = gx
    elif GR in data[gy]:
        gx = data[gy].index(GR)
        new_gy = gy
        new_gx = gx + 1
    elif GD in data[gy]:
        gx = data[gy].index(GD)
        new_gy = gy + 1
        new_gx = gx
    elif GL in data[gy]:
        gx = data[gy].index(GL)
        new_gy = gy
        new_gx = gx - 1

    if data[new_gy][new_gx] == OBS:
        # Turn right and don't move
        if data[gy][gx] == GU:
            data[gy] = replace_char(data[gy], gx, GR)
        elif data[gy][gx] == GR:
            data[gy] = replace_char(data[gy], gx, GD)
        elif data[gy][gx] == GD:
            data[gy] = replace_char(data[gy], gx, GL)
        elif data[gy][gx] == GL:
            data[gy] = replace_char(data[gy], gx, GU)
    else:
        curr_g = data[gy][gx]
        data[new_gy] = replace_char(data[new_gy], new_gx, curr_g)
        data[gy] = replace_char(data[gy], gx, MARK)
    return data


# print("\n".join(data))
while True:
    try:
        data = move_guard(data)
    except IndexError:
        # Replace the guard with a mark
        gy = [(GU in lst or GR in lst or GD in lst or GL in lst) for lst in data].index(
            True
        )
        if GU in data[gy]:
            gx = data[gy].index(GU)
        elif GR in data[gy]:
            gx = data[gy].index(GR)
        elif GD in data[gy]:
            gx = data[gy].index(GD)
        elif GL in data[gy]:
            gx = data[gy].index(GL)
        data[gy] = replace_char(data[gy], gx, MARK)
        break

# print("\n".join(data))
print(sum([lst.count(MARK) for lst in data]))


# Part 2
# Now we want to get the guard caught in a loop by placing a SINGLE obstruction
# Find all of the possible places to put the obstruction such that the guard gets caught in a loop


def get_guard_post(data):
    gy = [(GU in lst or GR in lst or GD in lst or GL in lst) for lst in data].index(
        True
    )
    if GU in data[gy]:
        gx = data[gy].index(GU)
    elif GR in data[gy]:
        gx = data[gy].index(GR)
    elif GD in data[gy]:
        gx = data[gy].index(GD)
    elif GL in data[gy]:
        gx = data[gy].index(GL)
    return gx, gy


def is_obs_adjacent(data, gxy):
    gx, gy = gxy
    # Handle boundaries
    maxy = len(data) - 1
    maxx = len(data[0]) - 1
    if gy == 0 or gy == maxy or gx == 0 or gx == maxx:
        return False
    if gy > 0 and data[gy - 1][gx] == OBS:
        return True
    if gy < maxy and data[gy + 1][gx] == OBS:
        return True
    if gx > 0 and data[gy][gx - 1] == OBS:
        return True
    if gx < maxx and data[gy][gx + 1] == OBS:
        return True
    return False


def move_guard(data, gxy):
    gx, gy = gxy
    if GU in data[gy]:
        new_gy = gy - 1
        new_gx = gx
    elif GR in data[gy]:
        new_gy = gy
        new_gx = gx + 1
    elif GD in data[gy]:
        new_gy = gy + 1
        new_gx = gx
    elif GL in data[gy]:
        new_gy = gy
        new_gx = gx - 1
    else:
        raise ValueError("Guard not found")

    if is_oob((new_gx, new_gy)):
        # If we've reached an edge of the map just return
        return data, (new_gx, new_gy), False

    if data[new_gy][new_gx] == OBS:
        # Turn right and don't move
        new_gx, new_gy = gx, gy
        turned = True
        if data[gy][gx] == GU:
            data[gy] = replace_char(data[gy], gx, GR)
        elif data[gy][gx] == GR:
            data[gy] = replace_char(data[gy], gx, GD)
        elif data[gy][gx] == GD:
            data[gy] = replace_char(data[gy], gx, GL)
        elif data[gy][gx] == GL:
            data[gy] = replace_char(data[gy], gx, GU)
    else:
        turned = False
        curr_g = data[gy][gx]
        data[new_gy] = replace_char(data[new_gy], new_gx, curr_g)
        data[gy] = replace_char(data[gy], gx, MARK)
    return data, (new_gx, new_gy), turned


def is_oob(gxy):
    gx, gy = gxy
    if gy < 0 or gy >= len(data) or gx < 0 or gx >= len(data[0]):
        return True
    return False


def is_looped(start_data):
    # Check if the guard gets caught in a loop
    # We know this happens if the guard repeats a turn
    i = 0
    gxys = Counter()
    gxy = get_guard_post(start_data)
    while True:
        start_data, gxy, turned = move_guard(start_data, gxy)
        if is_oob(gxy):
            return False
        if turned:
            gxys[gxy] += 1
            if gxys[gxy] > 5:
                return True
        i += 1
        if i > 100_000:
            print("WARNING: Too many iterations reached")
            return True


data = readlines(6)
cnt = 0
for y in tqdm(range(len(data))):
    # print(f"Checking row {y}, current count: {cnt}")
    for x in range(len(data[0])):
        if data[y][x] == OBS or data[y][x] in [GU, GR, GD, GL]:
            continue
        new_data = deepcopy(data)
        new_data[y] = replace_char(new_data[y], x, OBS)
        if is_looped(new_data):
            cnt += 1
print(cnt)
