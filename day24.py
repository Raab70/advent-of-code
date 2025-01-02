import re
import sys

from aocd.models import Puzzle
from rich import print

from aoc.pr import pr

sys.setrecursionlimit(10**6)
OPERATORS = {
    "OR": lambda x, y: x | y,
    "AND": lambda x, y: x & y,
    "XOR": lambda x, y: x ^ y,
}

if __name__ == "__main__":
    day_no = int(re.search(r"day(\d+).py", __file__).group(1))
    puzzle = Puzzle(year=2024, day=day_no)
    print(f"Starting Day {day_no}")
    data = puzzle.input_data.splitlines()
    # Comment out this line to use actual data
    # data = puzzle.examples[0].input_data.splitlines()

    def parse(data):
        values = {}
        nodes = []

        for line in data:
            if not line:
                continue
            if ":" in line:
                node, value = line.split(": ")
                values[node] = int(value)
            else:
                gate, out = line.split(" -> ")
                for op in OPERATORS.keys():
                    if f" {op} " in gate:
                        a, b = gate.split(f" {op} ")
                        nodes.append((a, b, op, out))
                        break
        return nodes, values

    def process(nodes, values, follow=None):
        while nodes:
            processed = set()
            for i, (a, b, op, out) in enumerate(nodes):
                if a in values and b in values:
                    a = values[a]
                    b = values[b]
                else:
                    continue
                if follow and follow in (a, b):
                    pr(f"{a} {op} {b} -> {out}")
                    follow = out
                func = OPERATORS[op]
                values[out] = func(a, b)
                processed.add(out)
                nodes.pop(i)
            if not processed:
                raise RuntimeError("No progress")
        return values

    # Part 1
    # What is the decimal number output on the wires starting with z?
    def get_bin(values, prefix="z"):
        zlen = max(int(k[1:]) for k in values if k.startswith(prefix)) + 1
        zs = [None] * zlen
        for k, v in values.items():
            if k.startswith(prefix):
                zs[int(k[1:])] = str(v)

        a = int("".join(reversed(zs)), 2)
        return a

    nodes, values = parse(data)
    values = process(nodes, values)
    a = get_bin(values)
    pr(a)
    puzzle.answer_a = a

    # Part 2
    # The system is doing addition
    # Exactly 4 pairs of gates output wires have been swapped
    nodes, values = parse(data)
    inputx = get_bin(values, "x")
    inputy = get_bin(values, "y")
    maxx = len(bin(inputx)) - 2
    expected = inputx + inputy
    # CHeck if any of the bits are correct for x + y = a vs expected
    bine = bin(expected)
    bina = bin(a)
    # print(f"Expected: {bine}")
    # print(f"Actual  : {bina}")

    # We know we're going to be swapping outputs so let's organize by output
    cons = {}
    wrongs = set()
    for node in nodes:
        a, b, op, out = node  # x08 AND y08 -> hdk
        cons[out] = (a, op, b)

    def get_out(a, op, b):
        for c, v in cons.items():
            if v in ((a, op, b), (b, op, a)):
                return c
        raise RuntimeError("Not found")

    def search(a, op):
        # Search for the op being performed on an input a
        # Returns the output and the other input
        for out, v in cons.items():
            if op == v[1]:
                if a == v[0]:
                    return out, v[2]
                elif a == v[2]:
                    return out, v[0]

    def swap(a, b):
        cons[a], cons[b] = cons[b], cons[a]
        wrongs.update({a, b})

    wrongs = set()
    a = get_out("x00", "AND", "y00")
    for i in range(1, maxx):
        x = f"x{i:02}"
        y = f"y{i:02}"
        z = f"z{i:02}"
        # XOR is first and last
        c_maybe = get_out(x, "XOR", y)
        z_maybe, c = search(a, "XOR")
        if z != z_maybe:
            swap(z, z_maybe)
        if c != c_maybe:
            swap(c, c_maybe)
        # Now just get the next iteration
        d = get_out(x, "AND", y)
        e = get_out(c, "AND", a)
        # Carryover is the last to start the next iteration
        a = get_out(d, "OR", e)

    b = ",".join(sorted(wrongs))
    pr(b)
    puzzle.answer_b = b
