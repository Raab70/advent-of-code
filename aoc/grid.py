from typing import Union, Any, List, Tuple
import math
from functools import total_ordering
from rich import print


def is_oob(grid: List[List[Any]], x: Union[int, Tuple, "Point"], y: int = None) -> bool:
    """Returns true if the x, y coordinates are out of bounds for the given grid"""
    if y is None and (isinstance(x, tuple) or isinstance(x, Point)):
        x, y = x

    maxx = len(grid[0])
    maxy = len(grid)
    if x < 0 or y < 0 or x >= maxx or y >= maxy:
        return True
    return False


def is_inb(grid: List[List[Any]], x: Union[int, Tuple, "Point"], y: int = None) -> bool:
    """Returns true if the x, y coordinates are in bounds for the given grid"""
    return not is_oob(grid, x, y)


def is_adj(x, y, x2, y2):
    """Check if two points are adjacent, does not count diagonals"""
    return abs(x - x2) + abs(y - y2) == 1


def grow_region(grid, x, y, seen):
    """Grow a region from a given point as long as the value matches"""
    c = grid[y][x]
    todo = [(x, y)]
    region = set()
    while todo:
        x, y = todo.pop(0)
        if (x, y) in seen:
            continue
        seen.add((x, y))
        region.add((x, y))
        for nx, ny in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            if is_inb(grid, nx, ny) and grid[ny][nx] == c:
                todo.append((nx, ny))
    return region, seen


def perimeter(pts):
    """Calculate the perimeter of a set of points representing a region"""
    perimeter = 0
    for pt in pts:
        x, y = pt
        for x2, y2 in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            if (x2, y2) not in pts:
                perimeter += 1
    return perimeter


def print_grid_pt(grid, pt):
    """Print a grid with a point highlighted"""
    x, y = pt
    for y2, row in enumerate(grid):
        for x2, cell in enumerate(row):
            if x2 == x and y2 == y:
                print("[red]" + cell + "[/red]", end="")
            else:
                print(cell, end="")
        print()


@total_ordering
class Point:
    """Simple 2-dimensional point."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, n):
        return Point(self.x * n, self.y * n)

    def __div__(self, n):
        return Point(self.x / n, self.y / n)

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return self.length < other.length

    def __invert__(self):
        return Point(-self.y, -self.x)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __repr__(self):
        return "Point({}, {})".format(self.x, self.y)

    def __hash__(self):
        return hash(tuple((self.x, self.y)))

    def __getitem__(self, idx):
        if idx == 0:
            return self.x
        if idx == 1:
            return self.y
        raise IndexError

    def is_adjacent(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y) == 1

    @property
    def length(self):
        return math.sqrt(self.x**2 + self.y**2)


DIRS = [
    Point(0, 1),  # north
    Point(1, 0),  # east
    Point(0, -1),  # south
    Point(-1, 0),  # west
]
