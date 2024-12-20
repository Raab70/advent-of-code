import itertools
import re
import sys
from collections import Counter, defaultdict
from copy import deepcopy

import networkx as nx
from rich import print
from tqdm import tqdm

from aoc.files import readlines
from aoc.grid import Point
from aoc.pr import pr

sys.setrecursionlimit(10**6)


def find_possible_cheats(grid, race_path, maxx, maxy):
    all_walls = [k for k, v in grid.items() if v == "#"]
    race_path_set = set(race_path)  # Convert to set for faster lookups
    all_possible_cheats = []

    for p in tqdm(all_walls):
        # Edge check first
        if p.x == 0 or p.y == 0 or p.x == maxx - 1 or p.y == maxy - 1:
            continue

        neighbors = p.neighbors()  # Calculate neighbors once

        # Check that neighbors are within bounds before checking race_path
        valid_neighbors = [n for n in neighbors if 0 <= n.x < maxx and 0 <= n.y < maxy]
        for i in range(len(valid_neighbors)):
            for j in range(i + 1, len(valid_neighbors)):
                n1 = valid_neighbors[i]
                n2 = valid_neighbors[j]
                if n1 in race_path_set and n2 in race_path_set:
                    all_possible_cheats.append((p, n1, n2))
                    all_possible_cheats.append((p, n2, n1))

    return all_possible_cheats


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
            if cell == "E":
                end = Point(x, y)

    def build_graph(grid, bidirectional=False):
        graph = nx.DiGraph()
        for point, cell in grid.items():
            graph.add_node(point)
            if cell == "#":
                continue
            for new_point in point.neighbors():
                if grid.get(new_point) != "#":
                    graph.add_edge(point, new_point)
                    if bidirectional:
                        graph.add_edge(new_point, point)
        return graph

    graph = build_graph(grid, bidirectional=True)
    race_path = nx.shortest_path(graph, start, end)
    race_path_set = set(race_path)
    race_len = len(race_path)

    all_walls = [k for k, v in grid.items() if v == "#"]
    # First, filter out anything that's definitely not a shortcut
    all_possible_cheats = find_possible_cheats(grid, race_path_set, maxx, maxy)

    def test_cheat(cheat):
        pw, p1, p2 = cheat
        # if p1 is after p2 in the race path, break
        try:
            i1 = race_path.index(p1)
            i2 = race_path.index(p2)
        except ValueError:
            return 0
        shortcut_len = i2 - i1 - 2
        if shortcut_len < 0:
            return 0
        # if pw == Point(8, 1):
        #     print(
        #         f"p1: {p1}, p2: {p2}, i1: {i1}, i2: {i2} shortcut_len: {shortcut_len}"
        #     )
        return shortcut_len

    def test_cheatg(cheat):
        _, p1, p2 = cheat
        graph.add_edge(p1, p2)
        try:
            shortcut_path = nx.shortest_path(graph, start, end)
            graph.remove_edge(p1, p2)

            shortcut_len = len(shortcut_path)
            return race_len - shortcut_len - 1
        except nx.NetworkXNoPath:
            graph.remove_edge(p1, p2)
            return 0

    # Results stores the savings compared to race len
    results = {}
    for cheat in tqdm(all_possible_cheats):
        if shortcut_len := test_cheatg(cheat):
            if shortcut_len != 0:
                results[cheat] = shortcut_len

    # for c, v in Counter(results.values()).items():
    #     print(f"There are {v} shortcuts that save {c} steps")
    # 1404 is too low
    pr(sum(v > 100 for v in results.values()))
