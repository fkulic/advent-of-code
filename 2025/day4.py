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


AROUND = [Point(x, y) for x, y in product([0, -1, 1], repeat=2) if x != 0 or y != 0]


def part_one(paper_rolls: set[Point]) -> int:
    total_sum = 0
    for p in paper_rolls:
        if sum(1 for d in AROUND if p + d in paper_rolls) < 4:
            total_sum += 1

    return total_sum


def part_two(paper_rolls: set[Point]) -> int:
    total_sum = 0
    while True:
        removed_rolls = set()
        for p in paper_rolls:
            if sum(1 for d in AROUND if p + d in paper_rolls) < 4:
                removed_rolls.add(p)

        if len(removed_rolls) == 0:
            break

        paper_rolls -= removed_rolls
        total_sum += len(removed_rolls)

    return total_sum


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    if not input_path.is_file():
        print(f"{input_path} is not a file")
        sys.exit(1)

    paper_rolls = set()
    for row, line in enumerate(input_path.read_text().strip().splitlines()):
        for col, c in enumerate(line.strip()):
            if c == "@":
                paper_rolls.add(Point(row, col))

    print("FIRST PART", part_one(paper_rolls))
    print("SECOND PART", part_two(paper_rolls))
