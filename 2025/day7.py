import sys
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def is_inside(self, dimensions: "Point") -> bool:
        return 0 <= self.x < dimensions.x and 0 <= self.y < dimensions.y


DOWN = Point(1, 0)
LEFT = Point(0, -1)
RIGHT = Point(0, 1)


def part_one(start: Point, splitters: set[Point], dimensions: Point) -> int:
    beam = deque([start])
    splitted = set()
    visited = set()

    while beam:
        p = beam.popleft()
        if p in visited:
            continue

        visited.add(p)
        d = p + DOWN

        if not d.is_inside(dimensions):
            continue

        if d in splitters:
            beam.append(d + LEFT)
            beam.append(d + RIGHT)
            splitted.add(d)
        else:
            beam.append(d)

    return len(splitted)


def part_two(start: Point, splitters: set[Point], dimensions: Point) -> int:
    timelines = {start: 1}
    row = 0
    while row < dimensions.x:
        row += 1
        next_row = defaultdict(int)
        for p, count in timelines.items():
            d = p + DOWN
            if d in splitters:
                next_row[d + LEFT] += count
                next_row[d + RIGHT] += count
            else:
                next_row[d] += count

        timelines = next_row
    return sum(timelines.values())


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    if not input_path.is_file():
        print(f"{input_path} is not a file")
        sys.exit(1)

    data = input_path.read_text().strip().splitlines()
    dimensions = Point(len(data[0]), len(data))

    splitters = set()
    start = Point(0, 0)
    for row, line in enumerate(data):
        for col, c in enumerate(line):
            if c == "^":
                splitters.add(Point(row, col))
            elif c == "S":
                start = Point(row, col)

    print("FIRST PART", part_one(start, splitters, dimensions))
    print("SECOND PART", part_two(start, splitters, dimensions))
