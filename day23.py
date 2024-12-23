import itertools
import re
import sys

import networkx as nx
from rich import print

from aoc.files import readlines
from aoc.pr import pr

sys.setrecursionlimit(10**6)

if __name__ == "__main__":
    day_no = int(re.search(r"day(\d+).py", __file__).group(1))
    print(f"Starting Day {day_no}")
    data = readlines(day_no)
    sample = """
    kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
""".strip().splitlines()
    # Comment out this line to use actual data
    # data = sample

    G = nx.Graph()
    for line in data:
        a, b = line.split("-")
        G.add_edge(a, b)

    # Consider only computer names that start with t
    # Find all the sets of three connected computers
    trios = set()
    for clique in nx.clique.enumerate_all_cliques(G):
        if len(clique) == 3:
            if any(v.startswith("t") for v in clique):
                trios.add(tuple(sorted(clique)))
    pr(len(trios))

    # Part 2
    max_clique = max(nx.find_cliques(G), key=len)
    # The password is the computer names in the maximum clique, in alphabetical order, separated by commas
    pr(",".join(sorted(max_clique)))
