import re
import sys
from collections import defaultdict, deque

import networkx as nx
from rich import print
from tqdm import tqdm

from aoc.files import readlines
from aoc.grid import Point
from aoc.pr import pr

sys.setrecursionlimit(10**6)


def build_graph(grid):
    graph = nx.DiGraph()
    for point, cell in grid.items():
        graph.add_node(point)
        if cell == "#":
            continue
        for new_point in point.neighbors():
            if grid.get(new_point) == ".":
                graph.add_edge(point, new_point)
    return graph


def shortest_paths(graph, start, end):
    paths = list(nx.all_shortest_paths(graph, start, end))
    dists = {}
    for path in paths:
        for i, p in enumerate(path):
            if p not in dists:
                dists[p] = i
    return dists


def find_cheats(graph, max_cheat_length):
    forward_dist = shortest_paths(graph, start, end)
    reverse_dist = shortest_paths(graph, end, start)
    maxx = max(p.x for p in grid)
    maxy = max(p.y for p in grid)
    race_len = forward_dist[end]
    cnt = 0
    for y in tqdm(range(maxy)):
        for x in range(maxx):
            cheat_start = Point(x, y)
            # If we're not on the path, skip
            if cheat_start not in forward_dist:
                continue

            q = deque([(cheat_start, 0)])
            visited = {cheat_start}

            while q:
                pt, steps = q.popleft()
                if steps == max_cheat_length:
                    continue

                for n in pt.neighbors():
                    # print(n)
                    if n in visited:
                        continue
                    if not (0 <= n.x < maxx and 0 <= n.y < maxy):
                        continue

                    visited.add(n)
                    q.append((n, steps + 1))

                    if n in forward_dist:
                        time_with_cheat = (
                            forward_dist[cheat_start] + steps + 1 + reverse_dist[n]
                        )
                        if race_len - time_with_cheat > 99:
                            cnt += 1
    return cnt


if __name__ == "__main__":
    day_no = int(re.search(r"day(\d+).py", __file__).group(1))
    print(f"Starting Day {day_no}")
    data = readlines(day_no)
    sample = """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
""".strip().splitlines()
    # Comment out this line to use actual data
    # data = sample

    maxy = len(data)
    maxx = len(data[0])
    grid = defaultdict(str)
    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            grid[Point(x, y)] = cell
            if cell == "S":
                start = Point(x, y)
                grid[start] = "."
            if cell == "E":
                end = Point(x, y)
                grid[end] = "."

    graph = build_graph(grid)
    print("Begin Part 1")
    pr(find_cheats(graph, 2))
    print("Begin Part 2")
    pr(find_cheats(graph, 20))
