import re
import time
from collections import defaultdict

from rich import print
import networkx as nx

from aoc.files import readlines
from aoc.grid import DIRS, Point
from aoc.pr import pr


def print_grid(grid):
    for y in range(max(pt.y for pt in grid) + 1):
        for x in range(max(pt.x for pt in grid) + 1):
            out = "#" if grid[Point(x, y)] == 1 else "."
            print(out, end="")
        print()


def build_grid_pt_graph(maxx, maxy):
    G = nx.grid_2d_graph(maxx + 1, maxy + 1)
    mapping = {node: Point(node[0], node[1]) for node in G.nodes()}
    G = nx.relabel_nodes(G, mapping)
    return G


if __name__ == "__main__":
    day_no = int(re.search(r"day(\d+).py", __file__).group(1))
    print(f"Starting Day {day_no}")

    start_time = time.time()
    data = readlines(day_no)

    data = [tuple(map(int, x.split(","))) for x in data]
    pts = [Point(x, y) for x, y in data]

    # Input are coordinates from 0-70 in both directions but these are byte positions
    # x is left edge and y is top edge
    start = Point(0, 0)
    end = Point(70, 70)

    # Part 1
    # As bytes fall they corrupt that memory space
    grid = defaultdict(int)
    for i in range(1024):
        if i > len(pts) - 1:
            break
        pt = pts[i]
        grid[pt] = 1

    # print_grid(grid)

    def bfs(start, end, grid):
        q = [start]
        distance = {start: 0}
        while q:
            pt = q.pop(0)
            if pt == end:
                return distance

            for d in DIRS:
                new_pt = pt + d
                if 0 <= new_pt.x <= end.x and 0 <= new_pt.y <= end.y:
                    if new_pt in distance:
                        continue
                    if grid[new_pt] == 1:
                        continue
                    distance[new_pt] = distance[pt] + 1
                    q.append(new_pt)
        return distance

    distance = bfs(start, end, grid)
    pr(distance[end])

    # Part 2
    def bfs2(start, end, grid):
        q = [start]
        visited = set()
        while q:
            pt = q.pop(0)
            if pt == end:
                return True

            for d in DIRS:
                new_pt = pt + d
                if 0 <= new_pt.x <= end.x and 0 <= new_pt.y <= end.y:
                    if new_pt in visited:
                        continue
                    if grid[new_pt] == 1:
                        continue
                    visited.add(new_pt)
                    q.append(new_pt)
        return False

    grid = defaultdict(int)
    for i in range(10_000):
        pt = pts[i]
        grid[pt] = 1

        if not bfs2(start, end, grid):
            print(f"Found at {i}")
            pr(pt)
            break
    print(f"Time taken: {time.time() - start_time:.2f}")

    # What if we try to do it with NetworkX?
    print()
    print("Starting NetworkX solution")
    start_time = time.time()
    data = readlines(day_no)

    data = [tuple(map(int, x.split(","))) for x in data]
    pts = [Point(x, y) for x, y in data]

    # Input are coordinates from 0-70 in both directions but these are byte positions
    # x is left edge and y is top edge
    start = Point(0, 0)
    end = Point(70, 70)

    # Part 1
    # As bytes fall they corrupt that memory space
    graph = build_grid_pt_graph(end.x, end.y)
    for i in range(1024):
        if i > len(pts) - 1:
            break
        pt = pts[i]
        graph.remove_node(pt)
    pr(nx.shortest_path_length(graph, start, end))

    # Part 2
    graph = build_grid_pt_graph(end.x, end.y)
    for i in range(10_000):
        if i > len(pts) - 1:
            break
        pt = pts[i]
        graph.remove_node(pt)
        try:
            dist = nx.shortest_path_length(graph, start, end)
        except nx.NetworkXNoPath:
            print(f"Found at {i}")
            pr(pt)
            break
    print(f"Time taken: {time.time() - start_time:.2f}")
