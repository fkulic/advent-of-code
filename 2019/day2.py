import re
import sys
from copy import deepcopy
from itertools import permutations
from pathlib import Path


def ints_in_str(s: str) -> list[int]:
    return [int(x) for x in re.findall(r"(-?\d+)", s)]


def run_intcode(memory: list[int]) -> int:
    instruction_pointer = 0
    while memory[instruction_pointer] != 99:
        op, in1, in2, out = memory[instruction_pointer : instruction_pointer + 4]
        if op == 1:
            memory[out] = memory[in1] + memory[in2]
        if op == 2:
            memory[out] = memory[in1] * memory[in2]
        instruction_pointer += 4
    return memory[0]


def part_one(memory: list[int]) -> int:
    memory[1], memory[2] = 12, 2
    return run_intcode(deepcopy(memory))


def part_two(memory: list[int]) -> int:
    for noun, verb in permutations(range(100), 2):
        m = deepcopy(memory)
        m[1], m[2] = noun, verb
        run_intcode(m)
        if m[0] == 19690720:
            return 100 * noun + verb
    raise Exception("Not possible")


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"

    memory = ints_in_str(input_path.read_text())

    print("FIRST PART", part_one(memory))
    print("SECOND PART", part_two(memory))
