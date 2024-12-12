from rich import print


def is_oob(grid, x, y):
    """Returns true if the x, y coordinates are out of bounds for the given grid"""
    maxx = len(grid[0])
    maxy = len(grid)
    if x < 0 or y < 0 or x >= maxx or y >= maxy:
        return True
    return False


def is_inb(grid, x, y):
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
