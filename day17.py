import concurrent.futures
import math
import multiprocessing as mp
import re
from collections import defaultdict
from copy import deepcopy

from rich import print
from tqdm import tqdm

from aoc.files import readlines
from aoc.pr import pr


def get_operand(op, registers):
    if op in (0, 1, 2, 3):
        return op
    if op == 4:
        return registers["A"]
    if op == 5:
        return registers["B"]
    if op == 6:
        return registers["C"]
    print(f"Unknown operand: {op}")
    return None


def run_program(program, registers, verbose=True):
    instr_ptr = 0
    output = []
    while True:
        try:
            instruction = program[instr_ptr]
        except IndexError as e:
            if verbose:
                print(f"Halting: {e}")
            break
        operand_lit = program[instr_ptr + 1]
        if verbose:
            print(
                f"Instruction: {instruction}, Operand: {operand_lit}, Registers: {registers}"
            )
        if instruction == 0:
            # adv instruction performs division
            combo_operand = get_operand(operand_lit, registers)
            res = registers["A"] / (2**combo_operand)
            # Result is truncated an written to A
            registers["A"] = math.trunc(res)
        elif instruction == 1:
            # bxl calculates the bitwise XOR of register B and the literal operand and stores it in B
            res = registers["B"] ^ operand_lit
            registers["B"] = res
        elif instruction == 2:
            # bst combo operand mod 8 and writes to B
            combo_operand = get_operand(operand_lit, registers)
            registers["B"] = combo_operand % 8
        elif instruction == 3:
            # jnz nothing if A register is zero
            if registers["A"] == 0:
                instr_ptr += 2
                continue
            # Otherwise it jumps by setting the instruction pointer to the value of its literal operand
            instr_ptr = operand_lit
            # if this instruction jumps, the instruction pointer is not increased by 2 after this instruction
            continue
        elif instruction == 4:
            # bxc bitwise XOR of register B and C and store in B, ignore operand
            res = registers["B"] ^ registers["C"]
            registers["B"] = res
        elif instruction == 5:
            # out combo op mod 8 and outputs the value
            combo_operand = get_operand(operand_lit, registers)
            output.append(combo_operand % 8)
        elif instruction == 6:
            # bdv works like adv except the result is stored in the B register
            combo_operand = get_operand(operand_lit, registers)
            res = registers["A"] / (2**combo_operand)
            registers["B"] = math.trunc(res)
        elif instruction == 7:
            # cdv is like adv except the result is stored in the C register, still read from A
            combo_operand = get_operand(operand_lit, registers)
            res = registers["A"] / (2**combo_operand)
            registers["C"] = math.trunc(res)
        instr_ptr += 2
    return output


def parse_program(data):
    registers = defaultdict(int)
    program = []
    for line in data:
        if "Register" in line:
            registers[line.split()[1][0]] = int(line.split()[2])
        elif "Program" in line:
            program = list(map(int, line.split(":")[1].split(",")))

    return program, registers


if __name__ == "__main__":
    day_no = int(re.search(r"day(\d+).py", __file__).group(1))
    print(f"Starting Day {day_no}")

    #     sample = """
    # Register A: 729
    # Register B: 0
    # Register C: 0

    # Program: 0,1,5,4,3,0
    #     """.strip().splitlines()
    #     program, registers = parse_program(sample)
    #     output = run_program(program, registers, verbose=False)
    #     assert ",".join(str(o) for o in output) == "4,6,3,5,6,3,5,2,1,0"

    #     sample = """
    # Register A: 0
    # Register B: 0
    # Register C: 9

    # Program: 2,6
    #     """.strip().splitlines()
    #     program, registers = parse_program(sample)
    #     output = run_program(program, registers, verbose=False)
    #     assert registers["B"] == 1

    #     sample = """
    # Register A: 10
    # Register B: 0
    # Register C: 0

    # Program: 5,0,5,1,5,4
    #     """.strip().splitlines()
    #     program, registers = parse_program(sample)
    #     output = run_program(program, registers, verbose=False)
    #     assert output == [0, 1, 2]

    #     sample = """
    # Register A: 2024
    # Register B: 0
    # Register C: 0

    # Program: 0,1,5,4,3,0
    #     """.strip().splitlines()
    #     program, registers = parse_program(sample)
    #     output = run_program(program, registers, verbose=False)
    #     assert output == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]
    #     assert registers["A"] == 0

    #     sample = """
    # Register A: 0
    # Register B: 29
    # Register C: 0

    # Program: 1,7
    #     """.strip().splitlines()
    #     program, registers = parse_program(sample)
    #     output = run_program(program, registers, verbose=False)
    #     assert registers["B"] == 26

    #     sample = """
    # Register A: 0
    # Register B: 2024
    # Register C: 43690

    # Program: 4,0
    #     """.strip().splitlines()
    #     program, registers = parse_program(sample)
    #     output = run_program(program, registers, verbose=False)
    #     assert registers["B"] == 44354

    data = readlines(day_no)
    program, registers = parse_program(data)
    output = run_program(program, registers, verbose=False)
    pr(",".join(str(o) for o in output))

    # Part 2
    # Program outputs another program!
    # The value in register A is corrupted, so we need to fix it
    data = """
Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
""".strip().splitlines()
    data = readlines(day_no)
    program, registers = parse_program(data)
    tgt_output = program.copy()
    orig_reg = deepcopy(registers)

    # Do a binary search to find the start where the length matches
    start = 34999999000000
    end = 39999999000000
    for i in tqdm(range(1_000)):
        print(f"Searching range {end-start:,}")
        if end - start < 10:
            break
        mid = (start + end) // 2
        registers = deepcopy(orig_reg)
        registers["A"] = mid
        output = run_program(program, registers, verbose=False)
        if len(output) < len(tgt_output):
            start = mid
        else:
            end = mid
    print(f"Start: {start} - End: {end}")

    # Brute force search
    for i in tqdm(range(int(start), int(start + 1e11))):
        registers = deepcopy(orig_reg)
        registers["A"] = i
        output = run_program(program, registers, verbose=False)
        if i % 100_000 == 0:
            print(
                f"Trying A: {i} - {len(output)} / {len(tgt_output)} {output[:10]} {tgt_output[:10]}"
            )
        if len(output) != len(tgt_output):
            print(f"Skipping A: {i}")
        if output == tgt_output:
            print(f"Found A: {i}")
            pr(i)
            break
