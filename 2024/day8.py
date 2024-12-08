import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, a: int) -> "Point":
        return Point(self.x * a, self.y * a)

    def is_inside(self, dimensions: "Point") -> bool:
        return 0 <= self.x < dimensions.x and 0 <= self.y < dimensions.y


class Antinodes:
    def __init__(self, map_dimensions: Point) -> None:
        self._nodes: set[Point] = set()
        self._dimensions: Point = map_dimensions

    def add(self, point: Point) -> bool:
        if point.is_inside(self._dimensions):
            self._nodes.add(point)
            return True
        return False

    def size(self) -> int:
        return len(self._nodes)


def load_inputs(filepath: Path) -> tuple[list[list[Point]], Point]:
    lines = [list(line.strip()) for line in filepath.read_text().splitlines()]
    assert lines and lines[0]

    dimensions = Point(len(lines), len(lines[0]))
    antenas: defaultdict[str, list[Point]] = defaultdict(list)
    for i, line in enumerate(lines):
        for j, character in enumerate(line):
            if character not in (".", "#"):
                antenas[character].append(Point(i, j))

    assert antenas, "No antenas"
    return list(antenas.values()), dimensions


def both_parts(antenas: list[list[Point]], dimensions: Point) -> tuple[int, int]:
    part_one = Antinodes(dimensions)
    part_two = Antinodes(dimensions)
    for locations in antenas:
        for i, a in enumerate(locations):
            for b in locations[i + 1 :]:
                distance = b - a
                part_one.add(a + distance * 2)
                part_one.add(b - distance * 2)

                x = 1
                while part_two.add(a + distance * x) | part_two.add(b - distance * x):
                    x += 1

    return part_one.size(), part_two.size()


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"

    antenas, dimensions = load_inputs(input_path)
    first, second = both_parts(antenas, dimensions)
    print("FIRST PART", first)
    print("SECOND PART", second)
