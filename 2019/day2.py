import re
import sys
from copy import deepcopy
from itertools import permutations
from pathlib import Path

from intcode import IntCodeComputer


def ints_in_str(s: str) -> list[int]:
    return [int(x) for x in re.findall(r"(-?\d+)", s)]


def part_one(memory: list[int]) -> int:
    m = deepcopy(memory)
    m[1], m[2] = 12, 2
    computer = IntCodeComputer(m, None)
    computer.run_intcode()
    return m[0]


def part_two(memory: list[int]) -> int:
    for noun, verb in permutations(range(100), 2):
        m = deepcopy(memory)
        m[1], m[2] = noun, verb
        computer = IntCodeComputer(m, None)
        computer.run_intcode()
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
