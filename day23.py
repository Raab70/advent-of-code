import re
import sys

import networkx as nx
from aocd.models import Puzzle
from rich import print

from aoc.pr import pr

sys.setrecursionlimit(10**6)

if __name__ == "__main__":
    day_no = int(re.search(r"day(\d+).py", __file__).group(1))
    puzzle = Puzzle(year=2024, day=day_no)
    print(f"Starting Day {day_no}")
    data = puzzle.input_data.splitlines()
    # Comment out this line to use actual data
    # data = puzzle.examples[0].input_data.splitlines()

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
    puzzle.answer_a = len(trios)

    # Part 2
    max_clique = max(nx.find_cliques(G), key=len)
    # The password is the computer names in the maximum clique, in alphabetical order, separated by commas
    pr(",".join(sorted(max_clique)))
    puzzle.answer_b = ",".join(sorted(max_clique))
