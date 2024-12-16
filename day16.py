import heapq
import re
from collections import defaultdict
from copy import deepcopy

from rich import print

from aoc.files import readlines
from aoc.pr import pr
from aoc.grid import Point, DIRS


def min_path_grid_with_turns(grid, start, dirs):
    maxy = len(grid)
    maxx = len(grid[0])

    distances = defaultdict(list)  # Key: (x, y, direction)
    previous = defaultdict(list)  # Key: (x, y, direction)
    priority_queue = [(0, start, "R")]  # (distance, (x, y), previous_direction)
    ptsible_moves = [(v[0], v[1], k) for k, v in dirs.items()]

    while priority_queue:
        current_distance, current_node, prev_dir = heapq.heappop(priority_queue)

        x, y = current_node

        for dx, dy, direction in ptsible_moves:
            nx, ny = x + dx, y + dy
            if grid[ny][nx] == WALL:
                continue
            if 0 <= ny < maxy and 0 <= nx < maxx:
                new_distance = current_distance + 1
                if prev_dir and prev_dir != direction:  # Check for turn
                    new_distance += 1000  # Turn cost
                if grid[ny][nx] == END:
                    print(
                        f"Found end at {nx, ny} {prev_dir}/{direction} {new_distance}"
                    )
                    print(
                        f"Coming from node: {current_node} {direction} which has cost {current_distance}"
                    )
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
    sample = """
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################""".strip().splitlines()
    # Comment out this line to use actual data
    # data = sample

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
    distances, previous = min_path_grid_with_turns(grid, start, dirs)

    min_cost = float("inf")
    for direction in ["U", "D", "L", "R"]:
        if ((end, direction)) in distances:
            cost = min(distances[(end, direction)])
            if cost < min_cost:
                min_cost = cost
                last_dir = direction
    pr(min_cost)
    # Find all paths that have the minimum cost
    print("Part 2")

    BOARD = {}
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            p = Point(x, y)
            BOARD[p] = WALL if c == WALL else EMPTY
            if c == START:
                START = p
            elif c == END:
                END = p

    start = Point(start[0], start[1])
    end = Point(end[0], end[1])
    todo = [(0, start, end, [])]
    seen = {}

    best_score = 1e9
    best_paths = defaultdict(list)
    while todo:
        score, pt, d, path = heapq.heappop(todo)
        # print(f"Visiting {pt} with score {score} and direction {d}")
        if seen.get((pt, d), 1e9) < score:
            continue
        seen[pt, d] = score

        if pt == END:
            best_score = min(best_score, score)
            best_paths[score].append(path + [pt])

        for dir in DIRS:
            np = pt + dir
            if dir == -d:
                continue

            if dir == d and BOARD.get(np) == EMPTY:
                heapq.heappush(todo, (score + 1, np, dir, [pt] + path))
            elif BOARD.get(np) == EMPTY:
                heapq.heappush(todo, (score + 1001, np, dir, [pt] + path))

    min_path_pts = set()
    for path in best_paths[best_score]:
        min_path_pts.update(set(path))

    # Part 1 solution for validation
    pr(best_score)
    pr(len(min_path_pts))
