import math
import re
import sys
from collections import deque
from dataclasses import dataclass
from pathlib import Path


def ints_in_str(s: str) -> list[int]:
    return [int(x) for x in re.findall(r"(-?\d+)", s)]


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    def distance(self, other: "Point") -> float:
        return (
            (other.x - self.x) ** 2 + (other.y - self.y) ** 2 + (other.z - self.z) ** 2
        )


def both_parts(boxes: list[Point], n: int) -> int:
    distances = []
    for i, p1 in enumerate(boxes):
        for p2 in boxes[i + 1 :]:
            distances.append((p1, p2))
    distances.sort(key=lambda x: x[0].distance(x[1]))

    at_n = 0
    where_is_it = {}
    circuits = {}
    distances = deque(distances)
    i = 1
    connections = 0
    while True:
        if connections == n:
            lens = sorted([len(circuits[k]) for k in circuits], reverse=True)
            at_n = math.prod(lens[:3])

        if len(where_is_it) == len(boxes) and len(circuits) == 1:
            return at_n, p1.x * p2.x

        connections += 1
        p1, p2 = distances.popleft()
        i1 = where_is_it.get(p1)
        i2 = where_is_it.get(p2)
        if i1 and i2:
            if i1 != i2:
                for p in circuits[i2]:
                    circuits[i1].add(p)
                    where_is_it[p] = i1
                del circuits[i2]
            continue

        if i1:
            where_is_it[p2] = i1
            circuits[i1].add(p2)
        elif i2:
            where_is_it[p1] = i2
            circuits[i2].add(p1)
        else:
            where_is_it[p1] = i
            where_is_it[p2] = i
            circuits[i] = set([p1, p2])
            i += 1


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    if not input_path.is_file():
        print(f"{input_path} is not a file")
        sys.exit(1)

    boxes = []
    for line in input_path.read_text().strip().splitlines():
        boxes.append(Point(*ints_in_str(line)))

    connections = 10 if len(boxes) <= 20 else 1000

    first, second = both_parts(boxes, connections)
    print("FIRST PART", first)
    print("SECOND PART", second)
