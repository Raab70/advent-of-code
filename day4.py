from aoc.files import readlines

data = readlines(4)
data = [line.strip() for line in data]
# Part 1
search_str = "XMAS"
backwards = search_str[::-1]
# We need to find words that are normal, backwards, up and down and diagonal
# Now build the diagonal rows
max_col = len(data[0])
max_row = len(data)
cols = [[] for _ in range(max_col)]
rows = [[] for _ in range(max_row)]
fdiag = [[] for _ in range(max_row + max_col - 1)]
bdiag = [[] for _ in range(len(fdiag))]
min_bdiag = -max_row + 1

for x in range(max_col):
    for y in range(max_row):
        cols[x].append(data[y][x])
        rows[y].append(data[y][x])
        fdiag[x + y].append(data[y][x])
        bdiag[x - y - min_bdiag].append(data[y][x])
cnt = 0
for row in rows:
    cnt += "".join(row).count(search_str)
    cnt += "".join(row).count(backwards)
print(f"{cnt} {search_str} found in rows")
for col in cols:
    cnt += "".join(col).count(search_str)
    cnt += "".join(col).count(backwards)
print(f"{cnt} {search_str} found in rows/cols")
for diag in fdiag:
    cnt += "".join(diag).count(search_str)
    cnt += "".join(diag).count(backwards)
print(f"{cnt} {search_str} found in rows/cols/diag")
for diag in bdiag:
    cnt += "".join(diag).count(search_str)
    cnt += "".join(diag).count(backwards)
print(f"{cnt} {search_str} found in rows/cols/diag/bdiag")
print(f"{cnt} {search_str} found")


# Part 2
# Now we are just looking for diagonals that cross!
search_str = "MAS"
backwards = search_str[::-1]
cnt = 0
# Easiest way to do this is to just create all of these X's and then search for the string
for x in range(1, max_col - 1):
    for y in range(1, max_row - 1):
        # x and y are centroids so we need to pad by 1
        x1 = data[y - 1][x - 1] + data[y][x] + data[y + 1][x + 1]
        x2 = data[y - 1][x + 1] + data[y][x] + data[y + 1][x - 1]
        if search_str in x1 or backwards in x1:
            if search_str in x2 or backwards in x2:
                cnt += 1
print(f"{cnt} {search_str} found in diagonals")
