import re
import sys
from collections import deque
from copy import deepcopy
from pathlib import Path

from intcode import IntCodeComputer


def ints_in_str(s: str) -> list[int]:
    return [int(x) for x in re.findall(r"(-?\d+)", s)]


class InputFunction:

    def __init__(self, commands: list[str]):
        self.input_queue = deque(self.to_ascii(commands))

    @staticmethod
    def to_ascii(commands: list[str]) -> list[int]:
        ascii_list = []
        for command in commands:
            for c in command:
                ascii_list.append(ord(c))
            ascii_list.append(10)
        return ascii_list

    def input(self) -> int:
        return self.input_queue.popleft()


def print_out(output):
    for c in output:
        print(chr(c), end="")


def solution(memory: list[int], commands: list[str]):
    input_f = InputFunction(commands)
    computer = IntCodeComputer(deepcopy(memory), input_f.input)
    computer.run_intcode()
    if computer.output[-1] > 255:
        return computer.output[-1]

    print_out(computer.output)
    return "Not correct"


def part_one(memory: list[int]) -> int:
    commands = [
        "NOT B T",
        "NOT T T",
        "AND C T",
        "NOT T J",
        "AND D J ",
        "NOT A T ",
        "OR T J",
        "WALK",
    ]
    return solution(memory, commands)


def part_two(memory: list[int]) -> int:
    commands = [
        "NOT B T",
        "NOT T T",
        "AND C T",
        "NOT T J",
        "AND D J ",
        "AND H J ",
        "NOT A T ",
        "OR T J ",
        "RUN",
    ]
    return solution(memory, commands)


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"
    memory = ints_in_str(input_path.read_text())

    print("FIRST PART", part_one(memory))
    print("SECOND PART", part_two(memory))
