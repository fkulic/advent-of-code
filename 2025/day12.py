from dataclasses import dataclass
from itertools import product
import sys
from pathlib import Path


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)


def flip(shape: set[Point]):
    rotated = set()
    for i in range(3):
        for j in range(3):
            if Point(i, j) in shape:
                rotated.add(Point(2 - i, j))
    return rotated


def rotate(shape: set[Point]):
    rotated = set()
    for i in range(3):
        for j in range(3):
            if Point(i, j) in shape:
                rotated.add(Point(2 - j, i))
    return rotated


def print_shape(shape: set[Point]):
    for i in range(3):
        for j in range(3):
            if Point(i, j) in shape:
                print("#", end="")
            else:
                print(".", end="")
        print()
    print()


def can_fit(shape: set[Point], starting_point: Point, occupied: set[Point]):
    for p in shape:
        if p + starting_point in occupied:
            return False
    return True


def part_one(shapes: list[set[Point]], regions) -> int:
    # all_shapes = []
    # for shape in shapes:
    #     all_ways = set([frozenset(shape)])
    #     transformed = shape
    #     for _ in range(3):
    #         transformed = rotate(transformed)
    #         all_ways.add(frozenset(transformed))
    #     transformed = flip(shape)
    #     all_ways.add(frozenset(transformed))
    #     for _ in range(3):
    #         transformed = rotate(transformed)
    #         all_ways.add(frozenset(transformed))
    #     all_shapes.append(all_ways)

    # This works for received input
    # Write generic solution later that works for any input
    can_pack = 0
    for dimensions, needed in regions:
        total_needed = sum(needed[i] * len(shapes[i]) for i in range(len(needed)))
        if total_needed <= dimensions.x * dimensions.y:
            can_pack += 1

    return can_pack


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    if not input_path.is_file():
        print(f"{input_path} is not a file")
        sys.exit(1)

    data = input_path.read_text().strip().split("\n\n")
    shapes = []
    for shapes_lines in data[:-1]:
        shape = set()
        for row, line in enumerate(shapes_lines.splitlines()[1:]):
            for col, c in enumerate(line):
                if c == "#":
                    shape.add(Point(row, col))
        shapes.append(shape)

    regions = []
    for line in data[-1].splitlines():
        dim, needed = line.split(": ")
        dim = dim.split("x")
        dim = Point(int(dim[0]), int(dim[1]))
        needed = [int(x) for x in needed.split()]
        regions.append((dim, needed))

    print("FIRST PART", part_one(shapes, regions))
