import math
import re
from collections import defaultdict
from copy import deepcopy

from rich import print

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
            # Print registers in binary
            # bin_reg = {k: bin(v) for k, v in registers.items()}
            # print(
            #     f"Instruction: {instruction}, Operand: {operand_lit}, Registers: {bin_reg}"
            # )
        if instruction == 0:
            # adv instruction performs division
            # Result is truncated an written to A
            registers["A"] = math.trunc(
                registers["A"] / (1 << get_operand(operand_lit, registers))
            )
        elif instruction == 1:
            # bxl calculates the bitwise XOR of register B and the literal operand and stores it in B
            registers["B"] ^= operand_lit
        elif instruction == 2:
            # bst combo operand mod 8 and writes to B
            registers["B"] = get_operand(operand_lit, registers) % 8
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
            registers["B"] ^= registers["C"]
        elif instruction == 5:
            # out combo op mod 8 and outputs the value
            output.append(get_operand(operand_lit, registers) % 8)
        elif instruction == 6:
            # bdv works like adv except the result is stored in the B register
            registers["B"] = math.trunc(
                registers["A"] / (1 << get_operand(operand_lit, registers))
            )
        elif instruction == 7:
            # cdv is like adv except the result is stored in the C register, still read from A
            registers["C"] = math.trunc(
                registers["A"] / (1 << get_operand(operand_lit, registers))
            )
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

    sample = """
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
    """.strip().splitlines()
    program, registers = parse_program(sample)
    output = run_program(program, registers, verbose=False)
    assert ",".join(str(o) for o in output) == "4,6,3,5,6,3,5,2,1,0"

    sample = """
Register A: 0
Register B: 0
Register C: 9

Program: 2,6
    """.strip().splitlines()
    program, registers = parse_program(sample)
    output = run_program(program, registers, verbose=False)
    assert registers["B"] == 1

    sample = """
Register A: 10
Register B: 0
Register C: 0

Program: 5,0,5,1,5,4
    """.strip().splitlines()
    program, registers = parse_program(sample)
    output = run_program(program, registers, verbose=False)
    assert output == [0, 1, 2]

    sample = """
Register A: 2024
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
    """.strip().splitlines()
    program, registers = parse_program(sample)
    output = run_program(program, registers, verbose=False)
    assert output == [4, 2, 5, 6, 7, 7, 7, 7, 3, 1, 0]
    assert registers["A"] == 0

    sample = """
Register A: 0
Register B: 29
Register C: 0

Program: 1,7
    """.strip().splitlines()
    program, registers = parse_program(sample)
    output = run_program(program, registers, verbose=False)
    assert registers["B"] == 26

    sample = """
Register A: 0
Register B: 2024
Register C: 43690

Program: 4,0
    """.strip().splitlines()
    program, registers = parse_program(sample)
    output = run_program(program, registers, verbose=False)
    assert registers["B"] == 44354

    data = readlines(day_no)
    program, registers = parse_program(data)
    output = run_program(program, registers, verbose=False)
    pr(",".join(str(o) for o in output))

    # Part 2
    # Program outputs another program!
    # The value in register A is corrupted, so we need to fix it

    # B, C start at 0
    # 2,4,1,5,7,5,1,6,0,3,4,6,5,5,3,0
    # 0: 2(4) = B = combo(4) [A] % 8
    # 1: 1(5) = A = B^op(5) [B]
    # 2: 7(5) = C = A/2**combo(5) [B]
    # 3: 1(6) = A = B^op(6) [C]
    # 4: 0(3) = A = A/2**combo(3) [A]
    # 5: 4(_) = B = B^C
    # 6: 5(5) = output = combo(5) [B] % 8
    # 7: 3(0) = jump to 0, aka restart
    # So it's just a for loop...

    # Do the search in binary space!
    expected = sum(d << (i * 3) for i, d in enumerate(program))
    print(bin(expected))
    possible = [0]

    # Search from right to left for each 3-bit chunk which means we need to search 8 possiblities
    # We do 3-bit chunks because the machine is a 3-bit machine which means the output is 3 bits
    # So each 3-bit chunk represents a single output number or instruction in our program
    for i in reversed(range(16)):
        new = []
        for j in range(8):
            for n in possible:
                inp = n + (j << i * 3)
                reg = {
                    "A": inp,
                    "B": 0,
                    "C": 0,
                }
                result = run_program(program, reg, verbose=False)
                shifted_result = sum(d << (i * 3) for i, d in enumerate(result))
                # Mask off to the bits we're looking for
                mask = (-1 << i * 3) & (8**16 - 1)
                if shifted_result & mask == expected & mask:
                    new += [inp]
        possible = new
        print(f"i: {i}, len: {len(possible)}")
    pr(min(possible))
