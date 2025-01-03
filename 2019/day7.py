import re
import sys
from collections import deque
from copy import deepcopy
from itertools import permutations
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


def run_feedback_loop(memory: list[int], phase_settings: tuple[int, ...]) -> int:
    computers = []
    Qs = [deque([x]) for x in phase_settings]
    Qs[0].append(0)

    for i in range(5):
        next_i = (i + 1) % 5

        def gen(i=i):
            return Qs[i].popleft() if Qs[i] else None

        def put(value, next_i=next_i):
            Qs[next_i].append(value)

        computer = IntCodeComputer(deepcopy(memory), gen, put)
        computers.append(computer)
    while True:
        for i, c in enumerate(computers):
            halted = c.run_intcode()
            if i == len(computers) - 1 and halted:
                return Qs[0].pop()


def part_two(memory: list[int]) -> int:
    max_thrust = 0
    for perm in permutations(range(5, 10)):
        max_thrust = max(max_thrust, run_feedback_loop(memory, perm))
    return max_thrust


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"

    memory = ints_in_str(input_path.read_text())

    print("FIRST PART", part_one(memory))
    print("SECOND PART", part_two(memory))
