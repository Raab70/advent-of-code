import re
from copy import deepcopy

from aoc.files import readlines

data = readlines(3)

# Instructions are like mul(X,Y) where X and Y are 1-3 digit numbers
# There are also invlaid characters that should be ignored
m = r"mul\((\d{1,3}),(\d{1,3})\)"

# Use the regex to extract all matches and then add up the results
matches = re.findall(m, data[0])

s = 0
for match in matches:
    s += int(match[0]) * int(match[1])
print(s)


# Part 2
# do() enables, don't() disables
# Muls are enabled by default
data = data[0]
start = 0
cnt = 0
s = deepcopy(data)
on = True
done = False
while True:
    try:
        idx = s.index("do")
    except ValueError:
        print("No more do's or don'ts")
        done = True
    # Now check between here and idx for muls
    if on:
        matches = re.findall(m, s[:idx])
        for match in matches:
            cnt += int(match[0]) * int(match[1])
    if done:
        break
    if s[idx : idx + 7] == "don't()":
        print("Found a don't() at index", idx)
        start = idx + 7
        on = False
    elif s[idx : idx + 4] == "do()":
        print("Found a do() at index", idx)
        start = idx + 4
        on = True
    else:
        print("Couldn't find a do() or don't() at index", idx)
        start = idx + 1
    s = s[start:]
print(cnt)
