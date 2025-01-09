import re
import sys
from collections import deque
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


DIRECTIONS = {
    Point(-1, 0): 1,
    Point(1, 0): 2,
    Point(0, -1): 3,
    Point(0, 1): 4,
}


def find_oxygen_system(memory: list[int]):
    robot = IntCodeComputer(memory, lambda: 0)
    current_pos = Point(0, 0)

    floor = set()
    walls = set()
    oxygen_pos = None
    oxygen_cost = 0

    visited = set()
    Q = deque([(current_pos, robot, 0)])
    while Q:
        pos, robot, cost = Q.popleft()
        if pos in visited:
            continue
        visited.add(pos)

        for d, command in DIRECTIONS.items():
            new_pos = pos + d
            if new_pos not in visited and new_pos not in walls:
                input_q = deque([command, None])

                def input_f():
                    return input_q.popleft()

                new_robot = robot.clone(input_f)
                new_robot.run_intcode()
                if new_robot.output:
                    match new_robot.output[-1]:
                        case 0:  # wall
                            walls.add(new_pos)
                        case 1:  # moved
                            floor.add(new_pos)
                            Q.append((new_pos, new_robot, cost + 1))
                        case 2:  # reached oxygen system
                            oxygen_pos = new_pos
                            oxygen_cost = cost + 1

    return floor, oxygen_pos, oxygen_cost


def time_to_fill_with_oxygen(floor, oxygen_pos):
    Q = deque([(oxygen_pos, 0)])
    max_time = 0
    visited = set()
    while Q:
        p, t = Q.popleft()
        if p in visited:
            continue
        visited.add(p)

        next_positions = [(new_p, t + 1) for d in DIRECTIONS if (new_p := p + d) in floor and new_p not in visited]
        if len(next_positions) == 0:
            max_time = max(max_time, t)
        else:
            Q.extend(next_positions)
    return max_time


def both_parts(memory: list[int]) -> tuple[int, int]:
    floor, oxygen_pos, oxygen_cost = find_oxygen_system(memory)
    time_to_fill = time_to_fill_with_oxygen(floor, oxygen_pos)

    return oxygen_cost, time_to_fill


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"

    memory = ints_in_str(input_path.read_text())

    first, second = both_parts(memory)
    print("FIRST PART", first)
    print("SECOND PART", second)
