import re
import sys
from collections import defaultdict, deque

from rich import print
from tqdm import tqdm

from aoc.files import readlines
from aoc.pr import pr

sys.setrecursionlimit(10**6)


def evolve(secret):
    # mix = bitwise XOR, prune = modulo 16777216
    # The secret evolves by multiplying by 64, mix then prune
    # Divide by 32, mix and prune
    # multiply by 2048, mix and prune
    step1 = secret * 64
    secret ^= step1
    secret %= 16777216
    step2 = secret // 32
    secret ^= step2
    secret %= 16777216
    step3 = secret * 2048
    secret ^= step3
    secret %= 16777216
    return secret


if __name__ == "__main__":
    day_no = int(re.search(r"day(\d+).py", __file__).group(1))
    print(f"Starting Day {day_no}")
    data = readlines(day_no)
    sample = """
1
2
3
2024
""".strip().splitlines()
    # Comment out this line to use actual data
    # data = sample

    # Confirm evolution works
    # secret = 123
    # for _ in range(10):
    #     secret = evolve(secret)
    #     pr(secret)

    # Part 1
    tot = 0
    for secret in data:
        secret = int(secret)
        for _ in range(2000):
            secret = evolve(secret)
        tot += secret
    pr(tot)

    # Part 2
    print("Part 2")
    # Price is the ones digit (mod 10)
    # Monkeys look for changes in price
    # We need a single sequence of 4 prices for each secret that says when to sell
    history = defaultdict(list)
    sales_lookup = defaultdict(dict)
    sequences = set()
    for secret in tqdm(data):
        secret = int(secret)
        initial = secret
        last = secret % 10
        last4 = deque(maxlen=4)
        # print(f"Price {last}")
        for _ in range(2_000):
            secret = evolve(secret)
            price = secret % 10
            delta = price - last
            last = price
            last4.append(delta)
            last4_tuple = tuple(last4)
            sequences.add(last4_tuple)
            history[initial].append((price, last4_tuple))
            if len(last4) != 4:
                continue
            if last4_tuple in sales_lookup[initial]:
                continue
            sales_lookup[initial][last4_tuple] = price
            # print(f"Price {price} Delta: {delta}")

    # Now sum up all of the prices for all of the numbers, What is the most bananas we can get?

    m = 0
    sales = defaultdict(int)
    for k in tqdm(history.keys()):
        for seq in sequences:
            price = sales_lookup[k].get(seq)
            # if seq == (-1, 1, 0, 0):
            #     print(f"For {k} price is {price}")
            if price is not None:
                sales[seq] += price

    pr(max(sales, key=sales.get))
    pr(max(sales.values()))
