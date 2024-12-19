import re

from rich import print
from tqdm import tqdm

from aoc.files import readlines
from aoc.pr import pr

if __name__ == "__main__":
    day_no = int(re.search(r"day(\d+).py", __file__).group(1))
    print(f"Starting Day {day_no}")
    data = readlines(day_no)
    sample = """
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
""".strip().splitlines()
    # Comment out this line to use actual data
    # data = sample

    patterns = data[0].split(", ")

    def substring_search(target_string, substrings, break_early=False):
        n = len(target_string)
        res = [False] * (n + 1)  # res[i] is True if target_string[:i] can be formed
        cnt = [0] * (n + 1)  # cnt[i] is the number of ways to form target_string[:i]
        # Empty string is always possible
        res[0] = True
        cnt[0] = 1

        for i in range(1, n + 1):
            for substring in substrings:
                sn = len(substring)
                if i >= sn and target_string[i - sn : i] == substring:
                    cnt[i] += cnt[i - sn]
                    if res[i - sn]:
                        res[i] = True
                        if break_early:
                            break
        return res[n], cnt[n]

    cnt = 0
    cnt2 = 0
    for line in tqdm(data[2:]):
        # Each line is a design that can be accomplished with some combination of patterns
        # How many designs are possible?
        relevant = [p for p in patterns if p in line]
        can_work, num_comb = substring_search(line, relevant)
        if can_work:
            cnt += 1
            cnt2 += num_comb

    pr(cnt)
    pr(cnt2)
