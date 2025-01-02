import sys
from collections import defaultdict, deque
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other) -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def man_dist_to_start(self) -> int:
        return abs(self.x) + abs(self.y)


DIRECTIONS = {
    "U": Point(-1, 0),
    "D": Point(1, 0),
    "L": Point(0, -1),
    "R": Point(0, 1),
}


def part_one(wire1: deque[tuple[Point, int]], wire2: deque[tuple[Point, int]]) -> int:
    intersections = set()
    first_wire_points = defaultdict(set)
    p = Point(0, 0)
    while wire1:
        direction, how_long = wire1.popleft()
        vertical = True if direction.x != 0 else False
        for _ in range(how_long):
            p += direction
            first_wire_points[vertical].add(p)

    p = Point(0, 0)
    while wire2:
        direction, how_long = wire2.popleft()
        vertical = True if direction.x != 0 else False
        for _ in range(how_long):
            p += direction
            if p in first_wire_points[not vertical]:
                intersections.add(p.man_dist_to_start())

    return min(intersections)


def part_two(wire1: deque[tuple[Point, int]], wire2: deque[tuple[Point, int]]) -> int:
    intersections = set()
    first_wire_points = defaultdict(lambda: defaultdict(int))
    step = 0
    p = Point(0, 0)
    while wire1:
        direction, how_long = wire1.popleft()
        vertical = True if direction.x != 0 else False
        for _ in range(how_long):
            step += 1
            p += direction
            first_wire_points[vertical][p] = step

    step = 0
    p = Point(0, 0)
    while wire2:
        direction, how_long = wire2.popleft()
        vertical = True if direction.x != 0 else False
        for _ in range(how_long):
            step += 1
            p += direction
            if first_dist := first_wire_points[not vertical].get(p):
                intersections.add(first_dist + step)

    return min(intersections)


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"

    wires = []
    for line in input_path.read_text().splitlines():
        wires.append(deque([(DIRECTIONS[path[0]], int(path[1:])) for path in line.split(",")]))

    print("FIRST PART", part_one(*deepcopy(wires)))
    print("SECOND PART", part_two(*deepcopy(wires)))
