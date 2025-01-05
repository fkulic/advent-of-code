import re
import sys
from copy import deepcopy
from pathlib import Path

from intcode import IntCodeComputer


def ints_in_str(s: str) -> list[int]:
    return [int(x) for x in re.findall(r"(-?\d+)", s)]


def part_one(memory: list[int]) -> int:
    computer = IntCodeComputer(deepcopy(memory), lambda: 1)
    computer.run_intcode()
    return computer.output[0]


def part_two(memory: list[int]) -> int:
    computer = IntCodeComputer(deepcopy(memory), lambda: 2)
    computer.run_intcode()
    return computer.output[0]


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"

    memory = ints_in_str(input_path.read_text())

    print("FIRST PART", part_one(memory))
    print("SECOND PART", part_two(memory))
