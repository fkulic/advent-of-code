import sys
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path

MIN_R, MIN_C = sys.maxsize, sys.maxsize
MAX_R, MAX_C = 0, 0


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)


UP = Point(-1, 0)
RIGHT = Point(0, 1)
DOWN = Point(1, 0)
LEFT = Point(0, -1)
DIRECTIONS = [UP, RIGHT, DOWN, LEFT]


def make_portals_start_end(letters: dict[Point, str], walkable: set[Point]):
    portals = defaultdict(list)
    portal_poses = {}
    start, end = None, None
    for p, l in letters.items():
        e = None
        level = 0
        if l2 := letters.get(p + RIGHT):
            e = p + RIGHT + RIGHT
            if e not in walkable:
                e = p + LEFT

        elif l2 := letters.get(p + DOWN):
            e = p + DOWN + DOWN
            if e not in walkable:
                e = p + UP

        if l2:
            assert e
            name = l + l2
            if name == "AA":
                start = e
            elif name == "ZZ":
                end = e
            else:
                if e.x in (MIN_R, MAX_R) or e.y in (MIN_C, MAX_C):
                    level = -1
                else:
                    level = 1
                portal_poses[e] = name
                portals[name].append((e, level))

    assert start is not None and end is not None
    return portals, portal_poses, start, end


def part_one(start: Point, end: Point, portals, portal_poses, walkable) -> int:
    visited = set()
    Q = deque([(start, 0)])
    while Q:
        p, cost = Q.popleft()
        if p in visited:
            continue
        visited.add(p)

        for d in DIRECTIONS:
            new_p = p + d
            if new_p == end:
                return cost + 1

            if name := portal_poses.get(new_p):
                idx = 1 if portals[name][0][0] == new_p else 0
                Q.append((portals[name][idx][0], cost + 2))
            elif new_p in walkable:
                Q.append((new_p, cost + 1))
    raise Exception("Not possible")


def part_two(start: Point, end: Point, portals, portal_poses, walkable) -> int:
    visited = set()
    Q = deque([(start, 0, 0)])
    while Q:
        p, cost, level = Q.popleft()
        if (p, level) in visited:
            continue
        visited.add((p, level))

        for d in DIRECTIONS:
            new_p = p + d
            if new_p == end and level == 0:
                return cost + 1

            if name := portal_poses.get(new_p):
                current_idx = 0 if portals[name][0][0] == new_p else 1
                new_idx = current_idx ^ 1
                new_level = level + portals[name][current_idx][1]
                if new_level < 0:
                    continue
                portal_out_pos = portals[name][new_idx][0]
                Q.append((portal_out_pos, cost + 2, new_level))
            elif new_p in walkable:
                Q.append((new_p, cost + 1, level))
    raise Exception("Not possible")


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"
    data = input_path.read_text().splitlines()

    walkable = set()
    letters = {}

    for i, line in enumerate(data):
        for j, c in enumerate(line):
            p = Point(i, j)
            if c == ".":
                MIN_R = min(i, MIN_R)
                MIN_C = min(j, MIN_C)
                MAX_R = max(i, MAX_R)
                MAX_C = max(j, MAX_C)
                walkable.add(p)
            elif c.isalpha():
                letters[p] = c

    portals, portal_poses, start, end = make_portals_start_end(letters, walkable)
    print("FIRST PART", part_one(start, end, portals, portal_poses, walkable))
    print("SECOND PART", part_two(start, end, portals, portal_poses, walkable))
