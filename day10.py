from collections import defaultdict

from rich import print

from aoc.files import readlines

HEAD = 0


def get_trailheads(data):
    trailheads = []
    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            try:
                val = int(cell)
                if val == HEAD:
                    trailheads.append((x, y))
            except ValueError:
                pass
    return trailheads


def get_next_steps(data, curr_pos):
    x, y = curr_pos
    curr_steps = [
        (x, y - 1),
        (x, y + 1),
        (x - 1, y),
        (x + 1, y),
    ]
    next_steps = []
    val = int(data[y][x])
    for step in curr_steps:
        if is_oob(data, step[0], step[1]):
            continue
        try:
            next_val = int(data[step[1]][step[0]])
            if next_val == val + 1:
                next_steps.append(step)
        except (ValueError, IndexError):
            pass
    return next_steps


def is_oob(data, x, y):
    maxx = len(data[0])
    maxy = len(data)
    if x < 0 or y < 0 or x >= maxx or y >= maxy:
        return True
    return False


if __name__ == "__main__":
    print(f"Starting {__file__}")
    data = readlines(10)
    sample = """
012345
123456
234567
345678
4.6789
56789.
""".strip().split("\n")

    # Comment out this line to use actual data
    # data = sample

    # Trailheads always have height 0
    trailheads = get_trailheads(data)

    # Score is the number of 9-height positions reachable from a given trailhead
    # So first we need to find all the trailheads

    # Now we need to find all the 9-height positions reachable from each trailhead
    scores = defaultdict(int)
    ratings = defaultdict(int)
    visited = defaultdict(set)
    for trailhead in trailheads:
        print(f"Trailhead: {trailhead}")
        curr_pos = trailhead
        queue = [curr_pos]
        # Now we also need to keep track of the path we take along the way
        paths = defaultdict(list)
        while True:
            # print()
            # print(f"Queue: {queue}")
            if not queue:
                break
            curr_pos = queue.pop(0)
            next_steps = get_next_steps(data, curr_pos)
            # print(f"Next steps: {next_steps}")
            for step in next_steps:
                curr_val = int(data[curr_pos[1]][curr_pos[0]])
                val = int(data[step[1]][step[0]])
                # print(f"From {curr_pos=} {curr_val=} Next step: {step} {val=}")
                if val == 9:
                    print(f"[{trailhead=}] Found 9 at {step}")
                    if step not in visited[trailhead]:
                        scores[trailhead] += 1
                    visited[trailhead].add(step)
                    ratings[step] += 1

                if val != 9:
                    # Don't add 9s to the queue
                    queue.append(step)
                    paths[step] = paths[curr_pos] + [step]
print(scores)
print(ratings)
print(sum(scores.values()))
print(sum(ratings.values()))
