import re
import sys
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from intcode import IntCodeComputer


class Color(Enum):
    BLACK = 0
    WHITE = 1


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other) -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __lt__(self, other: "Point") -> bool:
        return (self.x, self.y) < (other.x, other.y)


class Directions:
    _DIRECTIONS = [Point(-1, 0), Point(0, 1), Point(1, 0), Point(0, -1)]

    def __init__(self):
        self._i = 0

    def reset(self):
        self._i = 0

    def next(self, turn) -> Point:
        if turn == 0:
            self._i = (self._i - 1) % len(self._DIRECTIONS)
        else:
            self._i = (self._i + 1) % len(self._DIRECTIONS)
        return self._DIRECTIONS[self._i]


def ints_in_str(s: str) -> list[int]:
    return [int(x) for x in re.findall(r"(-?\d+)", s)]


class PaintRobot:
    def __init__(self, initial_color) -> None:
        self.paint = defaultdict(int)
        self._directions = Directions()
        self._current_position = Point(0, 0)
        self.paint[self._current_position] = initial_color.value
        self._new_paint = True

    def color_on_current_panel(self):
        return self.paint[self._current_position]

    def paint_and_move_robot(self, value):
        if self._new_paint:
            self.paint[self._current_position] = value
        else:
            self._current_position += self._directions.next(value)
        self._new_paint = not self._new_paint


def part_one(memory: list[int]) -> int:
    paint_robot = PaintRobot(Color.BLACK)
    computer = IntCodeComputer(deepcopy(memory), paint_robot.color_on_current_panel, paint_robot.paint_and_move_robot)
    computer.run_intcode()
    return len(paint_robot.paint)


def part_two(memory: list[int]) -> str:
    paint_robot = PaintRobot(Color.WHITE)
    computer = IntCodeComputer(deepcopy(memory), paint_robot.color_on_current_panel, paint_robot.paint_and_move_robot)
    computer.run_intcode()
    sorted_paint = sorted(paint_robot.paint.keys())
    min_p, max_p = sorted_paint[0], sorted_paint[-1]

    hull = ["\n"]
    for i in range(min_p.x, max_p.x + 1):
        line = []
        for j in range(min_p.y, max_p.y + 1):
            if paint_robot.paint[Point(i, j)] == 1:
                line.append("\u25a0")
            else:
                line.append(" ")
        hull.append("".join(line))
    return "\n".join(hull)


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"

    memory = ints_in_str(input_path.read_text())

    print("FIRST PART", part_one(memory))
    print("SECOND PART", part_two(memory))
