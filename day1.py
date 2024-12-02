with open("data/input1.txt") as f:
    data = f.read().splitlines()
    split = [d.split("   ") for d in data]
    l1 = sorted([int(s[0]) for s in split])
    l2 = sorted([int(s[1]) for s in split])

dist = 0
for l1a, l2b in zip(l1, l2):
    dist += abs(l1a - l2b)
print(dist)

sim = 0
for l1a in l1:
    cnt = sum(l1a == l2a for l2a in l2)
    sim += cnt * l1a
print(sim)