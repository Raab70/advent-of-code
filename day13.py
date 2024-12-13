import math
import re
from collections import Counter, defaultdict
from copy import deepcopy

import numpy as np
from rich import print
from tqdm import tqdm

from aoc.files import readlines
from aoc.pr import pr

DEFAULT_COST = 100_000_000_000_000


def solve_linear_system(x1, x2, x, y1, y2, y):
    """
    Solves a system of two linear equations:
    a * x1 + b * x2 = x
    a * y1 + b * y2 = y
    """

    A = np.array([[x1, x2], [y1, y2]], dtype=np.int64)
    b = np.array([x, y], dtype=np.int64)

    try:
        solution = np.linalg.solve(A, b)
    except np.linalg.LinAlgError:
        return None  # No unique solution

    # Check if a and b are integers within precision
    if not np.allclose(solution, solution.round()):
        return None
    # Check that the solution solves the equation
    solution = solution.round().astype(int)
    if not (np.dot(A, solution) == b).all():
        return None
    return solution


if __name__ == "__main__":
    day_no = int(re.search(r"day(\d+).py", __file__).group(1))
    print(f"Starting Day {day_no}")
    data = readlines(day_no)
    sample = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
""".strip().split("\n")
    # Comment out this line to use actual data
    # data = sample

    A_COST = 3
    A = "A"
    B = "B"
    B_COST = 1
    machines = []
    data_iter = iter(data)
    for line in data_iter:
        if not line:  # Skip empty lines
            continue

        if line.startswith("Button A"):
            machine = {}
            name, x, y = re.findall(r"Button (\w): X\+(\d+), Y\+(\d+)", line)[0]
            machine[name] = int(x), int(y)
            nextline = next(data_iter)
            name, x, y = re.findall(r"Button (\w): X\+(\d+), Y\+(\d+)", nextline)[0]
            machine[name] = int(x), int(y)
            nextline = next(data_iter)
            x, y = re.findall(r"X=(\d+), Y=(\d+)", nextline)[0]
            machine["prize"] = int(x), int(y)
        machines.append(machine)

    # Find the cheapest way to get to the price from each machine
    # First, find out if the machine can ever win a prize, if not, skip it
    for machine in machines:
        # Prefer to use the B button unless A gets us thrice as far
        # Start by getting to the prize's largest coordinate
        prize = machine["prize"]
        xp, yp = prize
        # Find the cost to get to the prize
        cost = DEFAULT_COST
        soln = None
        max_presses = 100
        xd = math.gcd(machine[A][0], machine[B][0])
        yd = math.gcd(machine[A][1], machine[B][1])
        if xp % xd != 0 or yp % yd != 0:
            # print("No solution")
            machine["cost"] = cost
            continue
        for a_presses in range(1, max_presses):
            for b_presses in range(1, max_presses):
                x = a_presses * machine[A][0] + b_presses * machine[B][0]
                y = a_presses * machine[A][1] + b_presses * machine[B][1]
                if x == xp and y == yp:
                    tc = a_presses * A_COST + b_presses * B_COST
                    if tc < cost:
                        cost = tc
                        soln = a_presses, b_presses
                else:
                    continue
        machine["cost"] = cost
        machine["solution"] = soln
    pr(sum(1 for m in machines if m["cost"] != DEFAULT_COST))
    pr(sum(m["cost"] for m in machines if m["cost"] != DEFAULT_COST))

    # machines = [machines[0]]
    for idx, machine in enumerate(machines):
        # Prefer to use the B button unless A gets us thrice as far
        # Start by getting to the prize's largest coordinate
        prize = machine["prize"]
        xp, yp = prize
        xp += 10_000_000_000_000
        yp += 10_000_000_000_000

        # Find the cost to get to the prize

        # Calculate all combinations of presses that could be possible
        xd = math.gcd(machine[A][0], machine[B][0])
        yd = math.gcd(machine[A][1], machine[B][1])
        if xp % xd != 0 or yp % yd != 0:
            machine["cost2"] = DEFAULT_COST
            machine["solution2"] = None
            continue
        soln = solve_linear_system(
            machine[A][0], machine[B][0], xp, machine[A][1], machine[B][1], yp
        )
        if soln is not None:
            a, b = soln
            machine["cost2"] = a * A_COST + b * B_COST
        else:
            machine["cost2"] = DEFAULT_COST
        machine["solution2"] = soln
    pr(sum(1 for m in machines if m["cost2"] != DEFAULT_COST))
    pr(sum(m["cost2"] for m in machines if m["cost2"] != DEFAULT_COST))
