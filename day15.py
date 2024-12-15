import re
import sys
from copy import deepcopy

from rich import print

from aoc.files import readlines
from aoc.pr import pr

sys.setrecursionlimit(10_000)


def print_map(map):
    print("\n".join("".join(row) for row in map))


def gps_sum(map):
    s = 0
    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            if cell == BOX:
                print(f"Box at ({x}, {y}) = {100 * y + x}")
                s += (100 * (y)) + x
    return s


def big_gps_sum(map):
    s = 0
    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            if cell == "[":
                print(f"Box at ({x}, {y}) = {100 * y + x}")
                s += (100 * (y)) + x
    return s


if __name__ == "__main__":
    day_no = int(re.search(r"day(\d+).py", __file__).group(1))
    print(f"Starting Day {day_no}")
    data = readlines(day_no)
    sample = """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^

    """.strip().splitlines()
    #     sample = """
    # ########
    # #..O.O.#
    # ##@.O..#
    # #...O..#
    # #.#.O..#
    # #...O..#
    # #......#
    # ########

    # <^^>>>vv<v>>v<<
    #     """.strip().splitlines()
    #     sample = """
    # #######
    # #...#.#
    # #.....#
    # #..OO@#
    # #..O..#
    # #.....#
    # #######

    # <vv<<^^<<^^
    # """.strip().splitlines()
    # Comment out this line to use actual data
    # data = sample

    ROBOT = "@"
    BOX = "O"
    WALL = "#"
    EMPTY = "."
    DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    MOVES = {
        "v": (0, 1),
        "^": (0, -1),
        ">": (1, 0),
        "<": (-1, 0),
    }

    map = []
    for idx, line in enumerate(data):
        if not line:
            break
        map.append(list(line))
        if ROBOT in line:
            robot = (idx, line.index(ROBOT))

    moves = []
    for line in data[len(map) + 1 :]:
        moves.extend(line.strip())

    def move_box(bpos, map, direction):
        x, y = bpos
        dx, dy = MOVES[direction]
        new_x, new_y = x + dx, y + dy
        # print(f"Moving box from {x}, {y} to {new_x}, {new_y}")
        # If we hit a wall, stop
        if map[new_y][new_x] == WALL:
            # print(f"Can't move wall, staying at {x}, {y}")
            return bpos
        # If we hit a box, recurse
        if map[new_y][new_x] == BOX:
            bpos = move_box((new_x, new_y), map, direction)
            if bpos == (new_x, new_y):
                # print("Can't move box")
                return (x, y)
        map[new_y][new_x] = BOX
        map[y][x] = EMPTY
        return new_x, new_y

    def move(rpos, map, direction):
        x, y = rpos
        dx, dy = MOVES[direction]
        new_x, new_y = x + dx, y + dy
        # print(f"Moving from {x}, {y} to {new_x}, {new_y}")
        # If we hit a wall, stop
        if map[new_y][new_x] == WALL:
            return rpos
        # If we hit a box, move the box
        if map[new_y][new_x] == BOX:
            bpos = (new_x, new_y)
            act_bpos = move_box(bpos, map, direction)
            if act_bpos == bpos:
                return rpos

        map[new_y][new_x] = ROBOT
        map[y][x] = EMPTY
        return new_x, new_y

    # for m in moves:
    #     # print()
    #     robot = move(robot, map, m)
    #     # print(f"Move: {m}")
    #     # print_map(map)
    # print_map(map)
    # pr(gps_sum(map))

    # Part 2
    BIGBOX = ["[", "]"]
    newmap = []
    for row in map:
        newrow = []
        for char in row:
            if char == ROBOT:
                newrow.extend([ROBOT, EMPTY])
            elif char == BOX:
                newrow.extend(BIGBOX)
            elif char == WALL:
                newrow.extend([WALL, WALL])
            else:
                newrow.extend([EMPTY, EMPTY])
        newmap.append(newrow)
    print_map(newmap)

    def move_big_box(bpos, map, direction):
        in_bpos = bpos
        in_map = deepcopy(map)
        if map[bpos[1]][bpos[0]] == "]":
            x, y = bpos[0] - 1, bpos[1]
            x2, y2 = bpos[0], bpos[1]
        else:
            x, y = bpos[0], bpos[1]
            x2, y2 = bpos[0] + 1, bpos[1]
        dx, dy = MOVES[direction]
        new_x, new_y = x + dx, y + dy
        new_x2, new_y2 = x2 + dx, y2 + dy
        # print(f"Moving box from {x}, {y} to {new_x}, {new_y}")
        # If we hit a wall, stop
        if map[new_y][new_x] == WALL or map[new_y2][new_x2] == WALL:
            # print(f"Can't move wall, staying at {x}, {y}")
            return in_bpos
        # If we hit a box, recurse
        if direction in ("v", "^"):
            # Boxes are aligned!
            if map[new_y][new_x] == "[" or map[new_y2][new_x2] == "]":
                # print("Hit aligned boxes up/down")
                bpos = move_big_box((new_x, new_y), map, direction)
                if bpos == (new_x, new_y):
                    # print("Can't move box")
                    return in_bpos
            # These are the tricky cases where a box partially overlaps another box
            else:
                to_move = []
                if map[new_y][new_x] in BIGBOX:
                    # print("Hit misaligned left box")
                    to_move.append((new_x, new_y))
                if map[new_y2][new_x2] in BIGBOX:
                    # print("Hit misaligned right box")
                    to_move.append((new_x2, new_y2))
                if to_move:
                    for pos in to_move:
                        bpos = move_big_box(pos, map, direction)
                        if bpos == pos:
                            # print("Can't move box")
                            map = in_map
                            return in_bpos

        elif direction == ">":
            if map[new_y2][new_x2] in BIGBOX:
                bpos = move_big_box((new_x2, new_y2), map, direction)
                if bpos == (new_x2, new_y2):
                    # print("Can't move box")
                    return in_bpos
        elif direction == "<":
            if map[new_y][new_x] in BIGBOX:
                bpos = move_big_box((new_x, new_y), map, direction)
                if bpos == (new_x, new_y):
                    # print("Can't move box")
                    return in_bpos
        map[y][x] = EMPTY
        map[y2][x2] = EMPTY
        map[new_y][new_x] = "["
        map[new_y2][new_x2] = "]"
        # print(f"Moved box to {new_x}, {new_y}")
        # print_map(map)
        return new_x, new_y

    def move_big(rpos, map, direction):
        x, y = rpos
        dx, dy = MOVES[direction]
        new_x, new_y = x + dx, y + dy
        # print(f"Moving from {x}, {y} to {new_x}, {new_y}")
        # If we hit a wall, stop
        if map[new_y][new_x] == WALL:
            return rpos, map
        # If we hit a box, move the box
        if map[new_y][new_x] in BIGBOX:
            mc = deepcopy(map)
            bpos = (new_x, new_y)
            act_bpos = move_big_box(bpos, map, direction)
            if act_bpos == bpos:
                return rpos, mc

        map[new_y][new_x] = ROBOT
        map[y][x] = EMPTY
        return (new_x, new_y), map

    # Find the robot first
    for y, row in enumerate(newmap):
        for x, cell in enumerate(row):
            if cell == ROBOT:
                robot = (x, y)
                break
    for m in moves:
        # print()
        robot, newmap = move_big(robot, newmap, m)
        # print(f"Move: {m}")
        # print_map(newmap)

    print_map(newmap)
    pr(big_gps_sum(newmap))
