import re
from collections import Counter

from rich import print
from tqdm import tqdm

from aoc.files import readlines
from aoc.pr import pr


def single_blink(stone: int):
    if stone == 0:
        return [1]
    stone_str = str(stone)
    if len(stone_str) % 2 == 0:
        half = len(stone_str) // 2
        # Remove any leading zeros but leave a single zero if it is the only digit]
        return [int(stone_str[:half]), int(stone_str[half:])]
    return [stone * 2024]


def blink(stones):
    new_stones = Counter()
    for stone, cnt in stones.items():
        for ns in single_blink(stone):
            new_stones[ns] += cnt
    return new_stones


def blinks(stones, n):
    for idx in range(n):
        print(f"Step {idx} have {len(stones):,} unique stones")
        stones = blink(stones)
    return stones


if __name__ == "__main__":
    day_no = int(re.search(r"day(\d+).py", __file__).group(1))
    print(f"Starting Day {day_no}")
    data = readlines(day_no)
    sample = ["0 1 10 99 999"]
    sample = ["125 17"]
    # Comment out this line to use actual data
    # data = sample
    data = data[0].split(" ")

    # Part 1
    # If the stone is 0 it becomes 1
    # If the stone has en even number of digits it becomes two stones for each half of digits
    # If no other rules apply the stone's number is multiplied by 2024
    stones_dict = Counter(map(int, data))
    stones_dict = blinks(stones_dict, 25)
    pr(stones_dict.total())

    # Part 2
    stones_dict = Counter(map(int, data))
    stones_dict = blinks(stones_dict, 75)
    pr(stones_dict.total())
