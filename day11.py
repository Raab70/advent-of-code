import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from queue import Queue

import pyperclip
from rich import print
from tqdm import tqdm

from aoc.files import readlines


def pr(s):
    print(s)
    pyperclip.copy(str(s))


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
    new_stones = {}
    for stone, cnt in stones.items():
        for ns in single_blink(stone):
            new_stones[ns] = new_stones.get(ns, 0) + cnt
    return new_stones


def blinks(stones, n):
    for idx in range(n):
        print(f"Step {idx} have {len(stones):,} stones")
        stones = blink(stones)
    return stones


def build_stones_dict(data):
    stones_dict = {}
    for stone in map(int, data):
        stones_dict[stone] = stones_dict.get(stone, 0) + 1
    return stones_dict


if __name__ == "__main__":
    print(f"Starting {__file__}")
    # day_no = __file__.split("/")[-1].split(".")[0]
    data = readlines(11)
    sample = ["0 1 10 99 999"]
    sample = ["125 17"]
    # Comment out this line to use actual data
    # data = sample
    data = data[0].split(" ")

    # Part 1
    # If the stone is 0 it becomes 1
    # If the stone has en even number of digits it becomes two stones for each half of digits
    # If no other rules apply the stone's number is multiplied by 2024
    stones_dict = build_stones_dict(data)
    stones_dict = blinks(stones_dict, 25)
    pr(sum(stones_dict.values()))

    # Part 2
    stones_dict = build_stones_dict(data)
    stones_dict = blinks(stones_dict, 75)
    pr(sum(stones_dict.values()))
