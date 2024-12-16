import heapq
import re
from collections import Counter, defaultdict
from copy import deepcopy

from rich import print

from aoc.files import readlines
from aoc.pr import pr


def min_path_grid_with_turns(grid, start):
    """
    Finds the minimum path between two points in a grid, considering turn costs.

    Args:
        grid: A 2D list representing the grid (costs).
        start: A tuple (row, col) representing the start point.
        end: A tuple (row, col) representing the end point.
        turn_cost: The cost incurred for each turn.

    Returns:
        A tuple: (min_cost, path) or (inf, None) if no path exists.
    """

    maxy = len(grid)
    maxx = len(grid[0])

    distances = defaultdict(list)  # Key: (x, y, direction)
    previous = defaultdict(list)  # Key: (x, y, direction)
    priority_queue = [(0, start, "R")]  # (distance, (x, y), previous_direction)

    while priority_queue:
        current_distance, current_node, prev_dir = heapq.heappop(priority_queue)

        # if (current_node, prev_dir) in distances and current_distance > distances[
        #     (current_node, prev_dir)
        # ]:
        #     continue
        # if current_node == end:
        #     path = []
        #     node_dir = (current_node, prev_dir)
        #     while node_dir:
        #         node, direction = node_dir
        #         path.insert(0, node)
        #         node_dir = previous.get(node_dir)
        #     return current_distance, path

        x, y = current_node
        possible_moves = [
            (-1, 0, "L"),
            (1, 0, "R"),
            (0, -1, "U"),
            (0, 1, "D"),
        ]  # (dx, dy, direction)

        for dx, dy, direction in possible_moves:
            nx, ny = x + dx, y + dy
            if grid[ny][nx] == WALL:
                continue
            if 0 <= ny < maxy and 0 <= nx < maxx:
                new_distance = current_distance + 1
                if prev_dir and prev_dir != direction:  # Check for turn
                    new_distance += 1000  # Turn cost
                # if (x, y) == (3, 7) or (x, y) == (13, 1):
                #     print(
                #         f"Checking {nx, ny} {grid[ny][nx]} Coming from {(x, y)} {prev_dir} ({current_distance})->({new_distance})"
                #     )
                #     print(distances.get(((nx, ny), direction), float("inf")))
                if grid[ny][nx] == END:
                    distances[((nx, ny), direction)].append(new_distance)
                    previous[((nx, ny), direction)].append((current_node, prev_dir))
                    continue
                if ((nx, ny), direction) in distances and new_distance > min(
                    distances[((nx, ny), direction)]
                ):  # If we've already found a path with the same cost
                    continue
                if (
                    previous.get(((nx, ny), direction))
                    and (current_node, prev_dir) in previous[((nx, ny), direction)]
                ):
                    continue
                distances[((nx, ny), direction)].append(new_distance)
                previous[((nx, ny), direction)].append((current_node, prev_dir))
                heapq.heappush(priority_queue, (new_distance, (nx, ny), direction))

    return distances, previous


if __name__ == "__main__":
    day_no = int(re.search(r"day(\d+).py", __file__).group(1))
    print(f"Starting Day {day_no}")
    data = readlines(day_no)
    sample = """
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
""".strip().splitlines()
    # Comment out this line to use actual data
    data = sample

    dirs = {
        "L": (-1, 0),
        "R": (1, 0),
        "U": (0, -1),
        "D": (0, 1),
    }  # (dx, dy, direction)
    EMPTY = "."
    START = "S"
    END = "E"
    WALL = "#"

    def find_start_end(grid):
        for j, row in enumerate(grid):
            for i, cell in enumerate(row):
                if cell == START:
                    start = (i, j)
                if cell == END:
                    end = (i, j)
        return start, end

    grid = [list(row) for row in data]
    start, end = find_start_end(grid)
    distances, previous = min_path_grid_with_turns(grid, start)

    min_cost = float("inf")
    for direction in ["U", "D", "L", "R"]:
        if ((end, direction)) in distances:
            cost = min(distances[(end, direction)])
            if cost < min_cost:
                min_cost = cost
    pr(min_cost)
    # Find all paths that have the minimum cost
    print("Part 2")
    seen = set()

    def get_paths_from_node(node, start, seen=seen, prev_dir=None):
        path = [node]
        dists = {}  # Key: node value: distance
        for dir in ["U", "D", "L", "R"]:
            dx, dy = dirs[dir]
            prev_node = (node[0] - dx, node[1] - dy)
            if not (0 <= prev_node[0] < len(grid[0]) and 0 <= prev_node[1] < len(grid)):
                continue
            if prev_node in seen:
                continue
            if (node, dir) not in distances:
                continue
            min_dist = min(distances.get((node, dir), [float("inf")]))
            # If we had to turn we've already added the cost in
            if prev_dir and prev_dir != dir:
                min_dist += 1000
            dists[prev_node] = min_dist
        # If we hit a dead end, just break out
        if not dists:
            print(f"Dead end at {node}")
            return []
        print(f"Candidates for {node} {dists}")
        # This is the minimum distance for any of the neighbors of the current node
        min_dist = min(dists.values())
        # Now look back through the neighbors to find the ones that have the minimum distance
        found_paths = []
        for prev_node, dist in dists.items():
            seen.add(prev_node)
            if prev_node == start:
                print("Found start")
                return path
            this_path = path.copy()
            this_path.append(prev_node)
            new_paths = get_paths_from_node(prev_node, start, seen=seen, prev_dir=dir)
            if not new_paths:
                # This was a dead end! It has been marked as seen so start over from here
                continue
            this_path.extend(new_paths)
            found_paths.append((dist, this_path))
        if not found_paths:
            return []
        fp_dists = [fp[0] for fp in found_paths]
        min_fp_dist = min(fp_dists)
        min_paths = [fp[1] for fp in found_paths if fp[0] == min_fp_dist]
        # Flatten list of lists
        min_paths = [item for sublist in min_paths for item in sublist]
        return min_paths

    paths = get_paths_from_node(end, start, seen=seen)
    pr(len(set(paths)))

    def get_cost_from_path(path):
        cost = 0
        prev_d = "R"
        for i in range(1, len(path)):
            r1, c1 = path[i - 1]
            r2, c2 = path[i]
            d = (r2 - r1, c2 - c1)
            cost += 1
            if prev_d is not None and d != prev_d:
                cost += 1000
            #     print(f"Turned at node {r1, c1} - {r2, c2} {cost:,}")
            # else:
            #     print(f"No turn at node {r1, c1} - {r2, c2} {cost:,}")
            prev_d = d
        return cost

    # pr(get_cost_from_path(min_path))

    def print_path(grid, path, marker="[red]O[/red]"):
        grid = deepcopy(grid)
        for r, c in path:
            grid[c][r] = marker
        for row in grid:
            print("".join(row))

    print_path(grid, paths)

    # Part 2
    # How many tiles are a part of at least one of the best paths
    # Luckily we've already got all the distances from the start to all the nodes
