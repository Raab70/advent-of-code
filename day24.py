import itertools
import re
import sys
from collections import Counter, defaultdict, deque
from copy import deepcopy

from aocd.models import Puzzle
from rich import print
from tqdm import tqdm

from aoc.pr import pr

sys.setrecursionlimit(10**6)

if __name__ == "__main__":
    day_no = int(re.search(r"day(\d+).py", __file__).group(1))
    puzzle = Puzzle(year=2024, day=day_no)
    print(f"Starting Day {day_no}")
    data = puzzle.input_data.splitlines()
    # Comment out this line to use actual data
    # data = puzzle.examples[0].input_data.splitlines()

    def parse(data):
        values = {}
        nodes = []
        OPERATORS = {
            "OR": lambda x, y: x | y,
            "AND": lambda x, y: x & y,
            "XOR": lambda x, y: x ^ y,
        }
        for line in data:
            if not line:
                continue
            if ":" in line:
                node, value = line.split(": ")
                values[node] = int(value)
            else:
                gate, out = line.split(" -> ")
                for op, func in OPERATORS.items():
                    if f" {op} " in gate:
                        a, b = gate.split(f" {op} ")
                        nodes.append((a, b, func, out))
                        break
        return nodes, values

    def process(nodes, values, follow=None):
        while nodes:
            processed = set()
            for i, (a, b, func, out) in enumerate(nodes):
                if a in values and b in values:
                    a = values[a]
                    b = values[b]
                else:
                    continue
                if follow and follow in (a, b):
                    pr(f"{a} {func.__name__} {b} -> {out}")
                    follow = out
                values[out] = func(a, b)
                processed.add(out)
                nodes.pop(i)
            if not processed:
                raise RuntimeError("No progress")
        return values

    # Part 1
    # What is the decimal number output on the wires starting with z?
    def get_bin(values, prefix="z"):
        zlen = max(int(k[1:]) for k in values if k.startswith(prefix)) + 1
        zs = [None] * zlen
        for k, v in values.items():
            if k.startswith(prefix):
                zs[int(k[1:])] = str(v)

        a = int("".join(reversed(zs)), 2)
        return a

    nodes, values = parse(data)
    values = process(nodes, values)
    a = get_bin(values)
    pr(a)
    puzzle.answer_a = a

    # Part 2
    # The system is doing addition
    # Exactly 4 pairs of gates output wires have been swapped
    nodes, values = parse(data)
    inputx = get_bin(values, "x")
    inputy = get_bin(values, "y")
    expected = inputx + inputy
    # CHeck if any of the bits are correct for x + y = a vs expected
    bine = bin(expected)
    bina = bin(a)
    print(f"Expected: {bine}")
    print(f"Actual  : {bina}")

    def flip(nodes, pairs):
        for pair in pairs:
            for i, (a, b, func, out) in enumerate(nodes):
                if out == pair[0]:
                    nodes[i] = (a, b, func, pair[1])
                elif out == pair[1]:
                    nodes[i] = (a, b, func, pair[0])
        return nodes

    def test_flip(nodes, pairs, bit):
        "Returns True if the flip works for the given bit"
        nodes = flip(nodes, pairs)
        for x in [0, 1]:
            for y in [0, 1]:
                inx = bin(x << bit)[2:].zfill(maxx)
                iny = bin(y << bit)[2:].zfill(maxy)
                values = {}
                for i in range(maxx):
                    values[f"x{i:02d}"] = inx[-i]
                    values[f"y{i:02d}"] = iny[-i]
                assert get_bin(values, "x") == x << bit
                assert get_bin(values, "y") == y << bit
                expected = (x << bit) + (y << bit)

                try:
                    values = process(nodes, values)
                except RuntimeError:
                    return False
                a = get_bin(values)
                # Only check the bits we're interested in:
                bina = bin(a)
                bine = bin(expected)
                if bina != bine:
                    return False
        return True

    # Find nodes that don't terminate correctly!
    import networkx as nx

    G = nx.DiGraph()
    for node in nodes:
        a, b, _, out = node
        G.add_edge(a, out)
        G.add_edge(b, out)

    def find_terminal_nodes_from_start(graph, start_node):
        """
        Finds terminal nodes reachable from a given start node in a DiGraph.

        Args:
            graph: A NetworkX DiGraph.
            start_node: The starting node for the search.

        Returns:
            A set of terminal nodes reachable from the start node.
            Returns an empty set if the start node is not in the graph.
        """

        if start_node not in graph:
            print(f"Warning! {start_node} not in graph")
            return set()

        reachable_nodes = set()
        terminal_nodes = set()

        # Use Depth-First Search (DFS) to find reachable nodes
        for node in nx.dfs_preorder_nodes(graph, source=start_node):
            reachable_nodes.add(node)

        # Check for terminal nodes among the reachable nodes
        for node in reachable_nodes:
            if graph.out_degree(node) == 0:
                terminal_nodes.add(node)

        return terminal_nodes

    maxx = max(int(k[1:]) for k in values.keys() if k.startswith("x")) + 1
    maxy = max(int(k[1:]) for k in values.keys() if k.startswith("y")) + 1
    maxz = max(int(k[1:]) for _, _, _, k in nodes if k.startswith("z")) + 1
    terminal_nodes = {}
    for x in range(maxx):
        start = f"x{x:02d}"
        tn = find_terminal_nodes_from_start(G, start)
        terminal_nodes[start] = tn
    for y in range(maxy):
        start = f"y{y:02d}"
        tn = find_terminal_nodes_from_start(G, start)
        terminal_nodes[start] = tn

    bad_conns = set()
    for i in range(maxx):
        x = f"x{i:02d}"
        y = f"y{i:02d}"
        expected = set(f"z{j:02d}" for j in range(i, maxz))
        if terminal_nodes[x] != expected:
            bad_conns.add(x)
        if terminal_nodes[y] != expected:
            bad_conns.add(y)

    sys.exit()
    # MORE OLD CODE -------------------------------------------------------------------------------------

    # for each bit from least to most significant, check if the bit is correct
    # if not, find the gate that is causing the error and flip it
    def get_all_flippable(nodes, bina, bine):
        flippable = defaultdict(set)
        bits = set()
        for bit in reversed(range(1, len(bine))):
            if bine[-bit] != bina[-bit]:
                print(f"Bit {bit} is incorrect")
                print(f"Expected: {bine[-bit]}")
                print(f"Actual  : {bina[-bit]}")
                for a, b, func, out in nodes:
                    if out == f"z{bit:02d}":
                        print(f"{a} {b} -> {out}")
                        bits.add(bit)
                        flippable[bit].add(a)
                        flippable[bit].add(b)

        while True:
            for i, (a, b, _, out) in enumerate(nodes):
                found = False
                for bit, f in flippable.items():
                    if out in f:
                        found = True
                        # print(f"{a} {b} -> {out}")
                        if a[0] not in ("x", "y"):
                            f.add(a)
                        if b[0] not in ("x", "y"):
                            f.add(b)
                if found:
                    nodes.pop(i)
            else:
                break
        return bits, flippable

    bits, flippable = get_all_flippable(nodes, bina, bine)
    # Group the bits by neighbors, and try flipping them within their set
    flippable_groups = defaultdict(set)
    bit_groups = defaultdict(set)
    prev_b = None
    group_idx = 0
    for b in sorted(bits):
        if prev_b is None:
            flippable_groups[group_idx].update(flippable[b])
            bit_groups[group_idx].add(b)
            prev_b = b
            continue
        if b - prev_b == 1:
            flippable_groups[group_idx].update(flippable[b])
            bit_groups[group_idx].add(b)
        else:
            group_idx += 1
            flippable_groups[group_idx].update(flippable[b])
            bit_groups[group_idx].add(b)
        prev_b = b

    # quads = []
    # for group, bits in zip(flippable_groups.values(), bit_groups.values()):
    #     pairs = list(itertools.combinations(group, 2))
    #     print(f"Group {group} Bits {bits} Pairs {len(pairs)}")
    #     for quad in tqdm(list(itertools.combinations(pairs, 4))):
    #         # if any of the pairs share a wire, skip
    #         if any(set(quad[0]) & set(q) for q in quad[1:]):
    #             continue
    #         quads.append(quad)

    flips = []
    all_bits = set(range(1, len(bine) + 1))
    ungrouped_bits = all_bits - set(itertools.chain(*bit_groups.values()))
    print()
    broken_bits = [bit for bit in range(1, len(bine) + 1) if bine[-bit] != bina[-bit]]
    print("starting search")
    print(f"Broken bits: {broken_bits}")
    all_pairs = []
    for group, bits in zip(flippable_groups.values(), bit_groups.values()):
        bits_to_check = ungrouped_bits | bits

        pairs = list(itertools.combinations(group, 2))
        print(f"Group {group} Bits {bits} Pairs {len(pairs)}")
        for pair in tqdm(pairs):
            nodes, values = parse(data)
            nodes = flip(nodes, [pair])
            try:
                values = process(nodes, values)
            except RuntimeError:
                continue
            a = get_bin(values)
            # Only check the bits we're interested in:
            bina = bin(a)
            bine = bin(expected)
            if all(bine[-bit] == bina[-bit] for bit in bits_to_check):
                print(f"Found flip {flips} + {pair} for bits {bits}")
                broken_bits = [
                    bit for bit in range(1, len(bine) + 1) if bine[-bit] != bina[-bit]
                ]
                print(f"Broken bits: {broken_bits}")
                flips.append(pair)
    # Now we'll have more than the 4 flips we need
    quads = list(itertools.combinations(flips, 4))
    print(f"Found {len(quads)} quads")
    good_quads = []
    for quad in tqdm(quads):
        # Skip any quads that contain the same wire twice
        if len(set(itertools.chain(*quad))) < 8:
            continue
        nodes, values = parse(data)
        nodes = flip(nodes, quad)
        xbit = 1
        ybit = 15
        values[f"x{xbit:02d}"] = values[f"x{xbit:02d}"] & 1
        values[f"y{ybit:02d}"] = values[f"y{xbit:02d}"] & 1
        inputx = get_bin(values, "x")
        inputy = get_bin(values, "y")
        try:
            values = process(nodes, values)
        except RuntimeError:
            continue
        a = get_bin(values)
        if a == (inputx + inputy):
            print(f"Found quad {quad} which fixes all bits")
            good_quads.append(quad)
    print(f"Found {len(good_quads)} good quads")

    # Now we need to use other inputs to find the correct quad
    xbits = len(bin(inputx)) - 5
    ybits = len(bin(inputy)) - 5
    good_quads = set(good_quads)
    bad_quads = set()
    for xbit in tqdm(range(1, xbits)):
        for ybit in range(1, ybits):
            for flips in good_quads:
                if flips in bad_quads:
                    continue
                nodes, values = parse(data)
                values[f"x{xbit:02d}"] = values[f"x{xbit:02d}"] & 1
                values[f"y{ybit:02d}"] = values[f"y{xbit:02d}"] & 1
                inputx = get_bin(values, "x")
                inputy = get_bin(values, "y")
                nodes = flip(nodes, flips)
                values = process(nodes, values)
                a = get_bin(values)
                if a != inputx + inputy:
                    print(f"Able to rule out {flips} for x{xbit:02d} y{ybit:02d}")
                    bad_quads.add(flips)
            good_quads = good_quads - bad_quads
            if len(good_quads) == 1:
                break

    wires = sorted(set(itertools.chain(*flips)))
    assert len(wires) == 8
    pr(",".join(wires))
    # puzzle.answer_b = ",".join(wires)
    sys.exit()

    # OLD CODE -----------------------------------------------------------

    def get_next_bit(nodes, bina, bine, bits_tried):
        flippable = set()
        for bit in reversed(range(1, len(bine))):
            if bit in bits_tried:
                continue
            if bine[-bit] != bina[-bit]:
                print(f"Bit {bit} is incorrect")
                print(f"Expected: {bine[-bit]}")
                print(f"Actual  : {bina[-bit]}")
                for a, b, func, out in nodes:
                    if out == f"z{bit:02d}":
                        print(f"{a} {b} -> {out}")
                        flippable.add(a)
                        flippable.add(b)
                        break
                if flippable:
                    break
                print()
        while True:
            for i, (a, b, _, out) in enumerate(nodes):
                if out in flippable:
                    # print(f"{a} {b} -> {out}")
                    if a[0] not in ("x", "y"):
                        flippable.add(a)
                    if b[0] not in ("x", "y"):
                        flippable.add(b)
                    nodes.pop(i)
                    break
            else:
                break
        return bit, flippable

    def find_flip(flippable, bit):
        for pair in list(itertools.combinations(flippable, 2)):
            # print(f"Trying flip {pair}")
            nodes, values = parse(data)
            nodes = flip(nodes, [pair])
            # print(f"Flipped {pair}")
            try:
                values = process(nodes, values)
                # print("Done processing")
                a = get_bin(values)
                bina = bin(a)
                if bina[-bit] == bine[-bit]:
                    # print(f"Found flip {pair}")
                    return pair

            except RuntimeError:
                pass
        return None

    flipped = set()
    bits_tried = set()
    while True:
        # Apply any flips
        nodes, values = parse(data)
        if flipped:
            nodes = flip(nodes, flipped)
        values = process(nodes, values)
        bina = bin(get_bin(values))

        # Check if the output is correct
        nodes, values = parse(data)
        bit, flippable = get_next_bit(nodes, bina, bine, bits_tried)
        if not flippable:
            break

        # Find a pair of gates to flip
        pair = find_flip(flippable, bit)
        if pair:
            if pair in flipped:
                print(f"Already flipped {pair}")
                break
            print(f"Flipping {pair} to fix bit {bit}")
            flipped.add(pair)
        else:
            print(f"No flip found for {bit}")
            bits_tried.add(bit)

    b = None
    pr(b)
    # puzzle.answer_b = b
