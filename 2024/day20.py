from collections import deque
from dataclasses import dataclass
from itertools import combinations
import sys
from pathlib import Path


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def man_distance(self, other: "Point"):
        return abs(self.x - other.x) + abs(self.y - other.y)


DIRECTIONS = [Point(-1, 0), Point(0, 1), Point(1, 0), Point(0, -1)]


def find_path(path: set[Point], S: Point, E: Point):
    Q = deque([(S, 0)])
    visited = {}
    while Q:
        p, cost = Q.popleft()
        if p in visited:
            continue
        visited[p] = cost

        for d in DIRECTIONS:
            new_p = p + d
            if new_p == E:
                visited[new_p] = cost + 1
                return visited
            elif new_p in path and new_p not in visited:
                Q.append((new_p, cost + 1))

    raise Exception("Didn't find E")


def both_parts(walls: set[Point], S: Point, E: Point) -> tuple[int, int]:
    no_cheat_path = find_path(walls, S, E)
    first, second = 0, 0
    for (p1, c1), (p2, c2) in combinations(no_cheat_path.items(), 2):
        distance = p1.man_distance(p2)
        saved_time = abs(c2 - c1) - distance
        if saved_time >= 100:
            if distance == 2:
                first += 1
            if distance <= 20:
                second += 1
    return first, second


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"
    data = input_path.read_text().strip()

    S = None
    E = None
    path: set[Point] = set()
    for i, line in enumerate(data.splitlines()):
        for j, c in enumerate(line.strip()):
            if c == ".":
                path.add(Point(i, j))
            elif c == "S":
                S = Point(i, j)
            elif c == "E":
                E = Point(i, j)
    assert isinstance(S, Point) and isinstance(E, Point)

    first, second = both_parts(path, S, E)
    print("FIRST PART", first)
    print("SECOND PART", second)
