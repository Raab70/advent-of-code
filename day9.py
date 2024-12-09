import itertools
import sys
from copy import deepcopy

from rich import print
from tqdm import tqdm

from aoc.files import readlines

sys.set_int_max_str_digits(20_000)
# Part 1
# sample = "12345"
sample = "2333133121414131402"
sample = [int(x) for x in sample]
data = sample
data = readlines(9)[0]


def build_fmap(data):
    # Numbers alternate between a file block and free blocks
    fmap = []
    blocks = [d for d in data[::2]]
    free = [d for d in data[1::2]]
    for idx, (b, f) in enumerate(itertools.zip_longest(blocks, free)):
        if b:
            curr_block = [idx] * int(b)
            fmap.extend(curr_block)
        if f:
            curr_free = ["."] * int(f)
            fmap.extend(curr_free)
    return fmap


def compute_checksum(fmap):
    checksum = 0
    for idx, f in enumerate(fmap):
        if f != ".":
            checksum += int(f) * idx
    return checksum


def find_last_block(fmap, ignored=set()):
    for idx, f in enumerate(fmap[::-1]):
        if f != "." and f not in ignored:
            # Now convert the index back to reverse order
            return len(fmap) - idx - 1, f
    return None, None


fmap = build_fmap(data)

# Compact the fmap by moving blocks to the front  of the list
compacted = ["."] * len(fmap)
end_block = len(fmap)
for idx, f in enumerate(tqdm(fmap)):
    if f != ".":
        compacted[idx] = f
        fmap[idx] = "."
    else:
        # If we have a free block, find the last block that is not free and move it here
        end_block, _ = find_last_block(fmap)
        if end_block is None:
            break
        compacted[idx] = fmap[end_block]
        fmap[end_block] = "."


print(compute_checksum(compacted))


# Part 2
# Move whole files instead of fragmenting them
def print_fmap(fmap):
    print("".join([str(f) for f in fmap]))


def sublist_idx(sub, lst):
    for i in range(len(lst) - len(sub) + 1):
        if lst[i : i + len(sub)] == sub:
            return i
    return None


fmap = build_fmap(data)
# print_fmap(fmap)
# Compact the fmap by moving blocks to a free space to the left if one exists
compacted = deepcopy(fmap)
ignored = set()
n = len(set(fmap))
while True:
    if len(ignored) % 1_000 == 0:
        print(f"{len(ignored):,} / {n:,}")
    # Since we look backwards this index is always the END of the block
    block_end_idx, block_val = find_last_block(compacted, ignored=ignored)
    if block_end_idx is None:
        break
    block_len = sum(1 for f in compacted if f == block_val)
    block = [block_val] * block_len
    needed = ["."] * block_len
    # print(f"Block: {block_val}, Len: {block_len}")
    insert_idx = sublist_idx(needed, compacted)
    if insert_idx is None or insert_idx > block_end_idx:
        ignored.add(block_val)
        continue
    # print(f"Inserting at: {insert_idx}")
    compacted[insert_idx : insert_idx + block_len] = block
    compacted[block_end_idx - block_len + 1 : block_end_idx + 1] = needed
    # print_fmap(compacted)
    ignored.add(block_val)

# print_fmap(compacted)
print(compute_checksum(compacted))
