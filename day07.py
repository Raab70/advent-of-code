import operator

from rich import print

from aoc.files import readlines

sample = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""
# data = sample.strip().split("\n")
data = readlines(7)


def print_sum(data, operators):
    cnt = 0
    for equation in data:
        sp = equation.split(":")
        tv = int(sp[0].strip())
        eq = [int(val) for val in sp[1].strip().split(" ")]
        # print(f"Starting equation {eq}")
        subtotals = set([eq[0]])
        for idx in range(1, len(eq)):
            new_subtotals = set()
            val = eq[idx]
            # print(f"Subtotals: {subtotals} {val}")
            for curr_subtotal in subtotals:
                for op, func in operators.items():
                    new_subtotals.add(func(curr_subtotal, val))
                    # print(f"Adding {curr_subtotal} {op} {new_subtotals}")
            subtotals = new_subtotals
            # print(f"{idx} {op} {new_subtotals}")
        if tv in subtotals:
            cnt += tv
    print(cnt)


operators = {
    "ADD": operator.add,
    "MUL": operator.mul,
}
print_sum(data, operators)

# Part 2
operators = {
    "ADD": operator.add,
    "MUL": operator.mul,
    "CONCAT": lambda x, y: int(f"{x}{y}"),
}
print_sum(data, operators)
