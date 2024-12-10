from dataclasses import dataclass
from pathlib import Path
import sys


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def is_inside(self, dimensions: "Point") -> bool:
        return 0 <= self.x < dimensions.x and 0 <= self.y < dimensions.y


directions = [Point(1, 0), Point(-1, 0), Point(0, -1), Point(0, 1)]


def load_inputs(filepath: Path) -> tuple[list[list[int]], set[Point]]:
    t_map: list[list[int]] = []
    starts: set[Point] = set()
    for i, line in enumerate(Path(filepath).read_text().strip().splitlines()):
        t_map.append([])
        for j, x in enumerate(line.strip()):
            x = int(x)
            t_map[i].append(x)
            if x == 0:
                starts.add(Point(i, j))
    return t_map, starts


def both_parts(t_map: list[list[int]], paths: set[Point]) -> tuple[int, int]:
    dimensions = Point(len(t_map), len(t_map[0]))
    score = 0
    rating = 0
    for start in paths:
        c_pos = [start]
        ends = set()
        while c_pos:
            new_poses = []
            for pos in c_pos:
                for d in directions:
                    new_pos = d + pos
                    if not new_pos.is_inside(dimensions):
                        continue

                    v_new_pos = t_map[new_pos.x][new_pos.y]
                    if v_new_pos == t_map[pos.x][pos.y] + 1:
                        if v_new_pos == 9:
                            ends.add(new_pos)
                            rating += 1
                        else:
                            new_poses.append(new_pos)

            c_pos = new_poses
        score += len(ends)

    return score, rating


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    t_map, starts = load_inputs(input_path)
    first, second = both_parts(t_map, starts)

    print("FIRST PART", first)
    print("SECOND PART", second)
