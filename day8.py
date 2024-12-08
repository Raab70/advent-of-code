from collections import defaultdict

from rich import print

from aoc.files import get_data_path, readlines

sample = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
""".strip().splitlines()

data = readlines(8)
# data = sample


def is_oob(x, y):
    return x < 0 or x >= len(data[0]) or y < 0 or y >= len(data)


loc = defaultdict(list)
antinodes = set()
for y, line in enumerate(data):
    for x, c in enumerate(line):
        if c != ".":
            loc[c].append((x, y))

# For every pair of points with the same frequency
for k, v in loc.items():
    for i, p1 in enumerate(v):
        for p2 in v[i + 1 :]:
            x1, y1 = p1
            x2, y2 = p2
            dx = x2 - x1
            dy = y2 - y1
            # The antinode is the same distance away from both points
            xan1 = x1 - dx
            yan1 = y1 - dy
            xan2 = x2 + dx
            yan2 = y2 + dy
            if not is_oob(xan1, yan1):
                antinodes.add((xan1, yan1))
            if not is_oob(xan2, yan2):
                antinodes.add((xan2, yan2))
print(len(antinodes))


# Part 2
# Now the antinodes continue on forever
for k, v in loc.items():
    for i, p1 in enumerate(v):
        for p2 in v[i + 1 :]:
            x1, y1 = p1
            x2, y2 = p2
            dx = x2 - x1
            dy = y2 - y1
            # The antinode is the same distance away from both points
            for i in range(100):
                xan1 = x1 - i * dx
                yan1 = y1 - i * dy
                xan2 = x2 + i * dx
                yan2 = y2 + i * dy
                if not is_oob(xan1, yan1):
                    antinodes.add((xan1, yan1))
                if not is_oob(xan2, yan2):
                    antinodes.add((xan2, yan2))
print(len(antinodes))
