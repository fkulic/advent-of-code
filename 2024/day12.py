from collections import deque
from dataclasses import dataclass
import sys
from pathlib import Path


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __lt__(self, other: "Point") -> bool:
        return (self.x, self.y) < (other.x, other.y)

    def is_inside(self, dimensions: "Point") -> int:
        return 0 <= self.x < dimensions.x and 0 <= self.y < dimensions.y


directions: list[Point] = [Point(1, 0), Point(0, -1), Point(-1, 0), Point(0, 1)]
diagonals: list[Point] = [Point(1, -1), Point(-1, -1), Point(-1, 1), Point(1, 1)]


def both_parts(farm_map: list[str]) -> tuple[int, int]:
    dimensions = Point(len(farm_map), len(farm_map[0]))
    first_part = 0
    second_part = 0
    visited = set()
    for i, line in enumerate(farm_map):
        for j, c in enumerate(line):
            current = Point(i, j)
            if current in visited:
                continue
            area = []
            same_plants = deque([current])
            perimeter = 0
            while same_plants:
                current = same_plants.popleft()
                if current in visited:
                    continue
                visited.add(current)
                area.append(current)

                for d in directions:
                    a = current + d
                    if a.is_inside(dimensions) and farm_map[a.x][a.y] == c:
                        same_plants.append(a)
                    else:
                        perimeter += 1

            first_part += len(area) * perimeter

            # Second part, count corners (corners == sides)
            sides = 0
            for p in area:
                for k, d in enumerate(directions):
                    next_k = (k + 1) % 4
                    a = (p + d) in area
                    b = p + directions[next_k] in area
                    if not a and not b:
                        sides += 1
                    elif a and b and (p + diagonals[k]) not in area:
                        sides += 1
            second_part += len(area) * sides

    return first_part, second_part


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    farm_map: list[str] = input_path.read_text().strip().splitlines()
    first, second = both_parts(farm_map)

    print("FIRST PART", first)
    print("SECOND PART", second)
