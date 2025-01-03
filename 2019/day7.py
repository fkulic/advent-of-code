from itertools import permutations
import re
import sys
from copy import deepcopy
from pathlib import Path

from intcode import IntCodeComputer


def ints_in_str(s: str) -> list[int]:
    return [int(x) for x in re.findall(r"(-?\d+)", s)]


def part_one(memory: list[int]) -> int:
    max_o = 0
    for perm in permutations(range(5)):
        last = 0
        for p in perm:
            it = iter([p, last])

            def gen():
                return next(it)

            computer = IntCodeComputer(deepcopy(memory), gen)
            computer.run_intcode()
            last = computer.output[0]
        max_o = max(max_o, last)
    return max_o


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"

    memory = ints_in_str(input_path.read_text())

    print("FIRST PART", part_one(memory))
    # print("SECOND PART", part_two(memory))
