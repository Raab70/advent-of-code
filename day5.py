from collections import defaultdict

from rich import print

from aoc.files import readlines

data = readlines(5)
data = [line.strip() for line in data]

sample = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
""".split(
    "\n"
)
# Uncomment this line to use the sample data
# data = sample

# Part 1
ordering = []
updates = []
for line in data:
    if "|" in line:
        ordering.append(line)
    elif "" == line:
        continue
    else:
        updates.append(line)
ordering = [[int(i) for i in line.split("|")] for line in ordering]
ordering_dict = defaultdict(list)
for order in ordering:
    ordering_dict[order[0]].append(order[1])
updates = [[int(i) for i in line.split(",")] for line in updates]

# Start by identifying which updates are in the right order
update_is_ordered = [True] * len(updates)
for idx, update in enumerate(updates):
    # print(f"\nStarting on update: {update}")
    for i in range(1, len(update)):
        current_page = update[i]
        ordering_rules = [True] * len(ordering_dict[current_page])
        # print(f"{current_page=} {ordering_dict[current_page]=}")
        for ordering_idx, after_page in enumerate(ordering_dict[current_page]):
            try:
                after_idx = update.index(after_page)
            except ValueError:
                continue
            # print(f"{current_page=} {after_page=} {after_idx=} {i=} {after_idx < i=}")
            if after_idx < i:
                update_is_ordered[idx] = False
                continue
# for update, is_ord in zip(updates, update_is_ordered):
#     print(f"{update=} {is_ord=}")
print(f"Part 1: {sum(update_is_ordered)=} / {len(update_is_ordered)=}")
# Now find the middle page number for each update that is correctly ordered
mp = 0
for idx, update in enumerate(updates):
    if update_is_ordered[idx]:
        # ordered_update = sorted(update)
        length = len(update)
        if length % 2 == 0:
            # print(f"{update=} {length=} {length // 2 - 1=}")
            mp += update[length // 2 - 1]
        else:
            # print(f"{update=} {length=} {length // 2=}")
            mp += update[length // 2]
print(f"Part 1: {mp}")


# Part 2
# For each of the incorrectly-ordered updates, use the page ordering rules to put the numbers in the right order
# Then find the middle page number and add them
def is_ordered(update):
    for i in range(1, len(update)):
        current_page = update[i]
        # print(f"{current_page=} {ordering_dict[current_page]=}")
        for after_page in ordering_dict[current_page]:
            try:
                after_idx = update.index(after_page)
            except ValueError:
                continue
            # print(f"{current_page=} {after_page=} {after_idx=} {i=} {after_idx < i=}")
            if after_idx < i:
                return False
    return True


def move_before(update, current_page, before_page):
    before_idx = update.index(before_page)
    current_idx = update.index(current_page)
    # Insert the current page before the before page
    update.pop(current_idx)
    update.insert(before_idx, current_page)


def move_after(update, current_page, after_page):
    # Move the after page to one after the current_page
    after_idx = update.index(after_page)
    current_idx = update.index(current_page)
    # Insert the after page after the current page
    update.pop(after_idx)
    update.insert(current_idx + 1, after_page)


mp = 0
for idx, update in enumerate(updates):
    if not update_is_ordered[idx]:
        # print(f"\nStarting on update: {update}")
        while not is_ordered(update):
            for i in range(len(update)):
                current_page = update[i]
                rules = ordering_dict[current_page]
                # print(f"{i=} {current_page=} {rules=}")
                # If none of the rules apply, skip
                if not any([after_page in update for after_page in rules]):
                    # print(f"Skipping {current_page=} {rules=}")
                    continue
                for after_page in rules:
                    try:
                        after_idx = update.index(after_page)
                    except ValueError:
                        continue
                    # print(f"{current_page=} {after_page=} {after_idx=} {i=} {after_idx < i=}")
                    if after_idx < i:
                        # Rule is violated
                        move_after(update, current_page, after_page)
        if not is_ordered(update):
            print(f"Update is still not ordered: {update}")
        # print(f"Ordered update: {update} {is_ordered(update)=}")
        length = len(update)
        if length % 2 == 0:
            mp += update[length // 2 - 1]
            # print(f"{update=} {length=} {length // 2 - 1=}")
        else:
            mp += update[length // 2]
            # print(f"{update=} {mp=} {length=} {length // 2=}")
print(f"Part 2: {mp}")
