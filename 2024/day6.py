import copy
import sys
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __hash__(self):
        return hash((self.x, self.y))


class Directions:
    _DIRECTIONS = [Point(-1, 0), Point(0, 1), Point(1, 0), Point(0, -1)]

    def __init__(self):
        self._i = 0

    def reset(self):
        self._i = 0

    def next(self) -> Point:
        direction = self._DIRECTIONS[self._i]
        self._i = (self._i + 1) % len(self._DIRECTIONS)
        return direction


def load_inputs(filepath: Path) -> tuple[Point, set[Point], Point]:
    lines = [list(line.strip()) for line in filepath.read_text().splitlines()]
    assert lines and lines[0]

    dimensions = Point(len(lines), len(lines[0]))
    obstacles = set()
    guard = None

    for i, line in enumerate(lines):
        for j, character in enumerate(line):
            if character == "#":
                obstacles.add(Point(i, j))
            if not guard and character == "^":
                guard = Point(i, j)

    assert obstacles or guard, "No guard or obstacles"
    return dimensions, obstacles, guard


def is_point_outside(point: Point, dimensions: Point) -> bool:
    return (
        0 > point.x or point.x >= dimensions.x or 0 > point.y or point.y >= dimensions.y
    )

def first_part(dimensions: Point, obstacles: set[Point], guard: Point) -> int:
    directions = Directions()
    direction = directions.next()
    in_front = guard
    count = 1
    visited = set()

    while True:
        in_front = guard + direction
        visited.add(guard)

        if is_point_outside(in_front, dimensions):
            break

        if in_front in obstacles:
            direction = directions.next()
        else:
            guard = in_front
            if guard not in visited:
                count += 1

    return count


def second_part(dimensions: Point, obstacles: set[Point], guard: Point) -> int:
    directions = Directions()
    loop = 0

    for i in range(dimensions.x):
        for j in range(dimensions.y):
            if Point(i, j) in obstacles:
                continue
            
            directions.reset()
            direction = directions.next()
            local_guard = guard
            in_front = guard

            expanded_obstacles = copy.deepcopy(obstacles)
            expanded_obstacles.add(Point(i, j))
            visited_with_direction = set()

            while True:
                in_front = local_guard + direction
                if (in_front, direction) in visited_with_direction:
                    loop += 1
                    break

                visited_with_direction.add((local_guard, direction))
                if is_point_outside(in_front, dimensions):
                    break

                if in_front in expanded_obstacles:
                    direction = directions.next()
                else:
                    local_guard = in_front

    return loop


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"
    data = load_inputs(input_path)

    print("FIRST PART", first_part(*data))
    print("SECOND PART", second_part(*data))
