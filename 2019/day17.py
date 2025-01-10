import re
import sys
from collections import deque
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path

from intcode import IntCodeComputer


def ints_in_str(s: str) -> list[int]:
    return [int(x) for x in re.findall(r"(-?\d+)", s)]


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other) -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __lt__(self, other: "Point") -> bool:
        return (self.x, self.y) < (other.x, other.y)


DIRECTIONS = [Point(-1, 0), Point(0, 1), Point(1, 0), Point(0, -1)]
DIRECTIONS_MAPPING = {"^": Point(-1, 0), ">": Point(0, 1), "v": Point(0, -1), "<": Point(1, 0)}


def left_right(current_direction) -> list[tuple[Point, str]]:
    i = DIRECTIONS.index(current_direction)
    left_i = (i - 1) % len(DIRECTIONS)
    right_i = (i + 1) % len(DIRECTIONS)
    return [(DIRECTIONS[left_i], "L"), (DIRECTIONS[right_i], "R")]


def get_pattern(lst, A, B, C, pattern=None) -> list[tuple[str, int]] | None:
    if pattern is None:
        pattern = []
    if len(lst) > 0 and len(pattern) == 20:
        return None
    if lst[: len(A)] == A:
        pattern.append("A")
        return get_pattern(lst[len(A) :], A, B, C, pattern)
    if lst[: len(B)] == B:
        pattern.append("B")
        return get_pattern(lst[len(B) :], A, B, C, pattern)
    if lst[: len(C)] == C:
        pattern.append("C")
        return get_pattern(lst[len(C) :], A, B, C, pattern)
    if len(lst) > 0:
        return None
    else:
        return pattern


def split_into_substrings_with_occurrences(s: list[tuple[str, int]]) -> list[list[tuple[str, int]]]:
    visited = set()
    for i in range(2, 22, 2):
        A = s[:i]
        for j_start in range(i, len(s), 2):
            for j_end in range(j_start + 2, len(s), 2):
                if j_end - j_start > 20:
                    break
                B = s[j_start:j_end]
                for k_start in range(j_end, len(s), 2):
                    for k_end in range(k_start + 2, len(s), 2):
                        if k_end - k_start > 20:
                            continue
                        C = s[k_start:k_end]

                        hashable_key = (tuple(A), tuple(B), tuple(C))
                        if hashable_key in visited:
                            continue
                        visited.add(hashable_key)
                        pattern = get_pattern(s, A, B, C)
                        if pattern is not None:
                            return [pattern, A, B, C]

    raise Exception("Not possible")


def parse(computer_output: list[int]) -> tuple[set[Point], tuple[Point, Point]]:
    scaffolds = set()
    robot = None
    r = 0
    c = 0
    for x in computer_output:
        char = chr(x)
        match chr(x):
            case "#":
                p = Point(r, c)
                scaffolds.add(p)
                c += 1
            case "^" | "v" | "<" | ">":
                p = Point(r, c)
                scaffolds.add(p)
                robot = p, DIRECTIONS_MAPPING[char]
                c += 1
            case "\n":
                r += 1
                c = 0
            case _:
                c += 1
    assert robot
    return scaffolds, robot


def alignment_sum(scaffolds) -> int:
    alignment_sum = 0
    for p in scaffolds:
        if sum(int(p + d in scaffolds) for d in DIRECTIONS) == 4:
            alignment_sum += p.x * p.y
    return alignment_sum


def find_full_pattern_path(scaffolds, robot_pos, robot_dir) -> list[tuple[str, int]]:
    Q = deque([robot_pos])
    full_pattern = []
    move = 0
    while Q:
        pos = Q.popleft()
        move += 1
        straight_ahead_pos = pos + robot_dir
        if straight_ahead_pos in scaffolds:
            Q.append(straight_ahead_pos)
            continue

        for d, letter in left_right(robot_dir):
            new_pos = pos + d
            if new_pos in scaffolds:
                if len(full_pattern) > 0:
                    full_pattern.append(move)
                full_pattern.append(letter)
                move = 0
                robot_dir = d
                Q.append(new_pos)
                break

    full_pattern.append(move)
    return full_pattern


class InputFunction:

    def __init__(self, pattern: list[list[tuple[str, int]]]):
        self.input_queue = deque([])
        for part in pattern:
            self.input_queue.extend(self.to_ascii(part))
        self.input_queue.append(ord("n"))
        self.input_queue.append(10)

    @staticmethod
    def to_ascii(part: list[tuple[str, int]]) -> list[int]:
        ascii_list = []
        for i, x in enumerate(part):
            if isinstance(x, int):
                for c in str(x):
                    ascii_list.append(ord(c))
            else:
                ascii_list.append(ord(x))
            if i < len(part) - 1:
                ascii_list.append(ord(","))
        ascii_list.append(10)
        return ascii_list

    def input(self) -> int:
        return self.input_queue.popleft()


def both_parts(memory: list[int]) -> tuple[int, int]:
    computer = IntCodeComputer(deepcopy(memory), None)
    computer.run_intcode()
    scaffolds, (robot_pos, robot_dir) = parse(computer.output)
    first = alignment_sum(scaffolds)

    full_pattern = find_full_pattern_path(scaffolds, robot_pos, robot_dir)
    splitted = split_into_substrings_with_occurrences(full_pattern)

    input_f = InputFunction(splitted)
    memory[0] = 2
    computer = IntCodeComputer(deepcopy(memory), input_f.input)
    computer.run_intcode()
    second = computer.output[-1]

    return first, second


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"

    memory = ints_in_str(input_path.read_text())

    first, second = both_parts(memory)
    print("FIRST PART", first)
    print("SECOND PART", second)
