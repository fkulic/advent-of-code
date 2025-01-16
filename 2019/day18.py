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


DIRECTIONS = [Point(-1, 0), Point(0, 1), Point(1, 0), Point(0, -1)]

ALL_KEYS = 0
KEYS: dict[int, Point] = {}
KEY_POSES: dict[Point, int] = {}
DOORS: dict[int, Point] = {}
DOOR_POSES: dict[Point, int] = {}

PATH_CACHE = {}


def get_paths(start, walls):
    if start in PATH_CACHE:
        return PATH_CACHE[start]

    Q = deque([(start, 0, 0)])
    paths = defaultdict(dict)
    visited = defaultdict(set)

    while Q:
        p, cost, doors_passed = Q.popleft()

        already_visited = False
        for prev_doors_passed in visited[p]:
            if (prev_doors_passed & doors_passed) == prev_doors_passed:
                already_visited = True
                break
            
        if already_visited:
            continue
        
        visited[p].add(doors_passed)

        for d in DIRECTIONS:
            new_p = p + d
            if new_p in walls:
                continue

            new_doors_passed = doors_passed
            if new_p in DOOR_POSES:
                new_doors_passed |= DOOR_POSES[new_p]

            if new_p in KEY_POSES:
                key_id = KEY_POSES[new_p]
                if new_doors_passed not in paths[key_id]:
                    paths[key_id][new_doors_passed] = cost + 1

            Q.append((new_p, cost + 1, new_doors_passed))
    PATH_CACHE[start] = paths
    return paths


def part_one(start, walls) -> int:
    visited = {}
    Q = deque([(start, 0, 0)])
    min_cost = 1000000000

    while Q:
        current_pos, current_cost, collected_keys = Q.popleft()

        if collected_keys == ALL_KEYS:
            if min_cost > current_cost:
                min_cost = current_cost
            continue

        if (current_pos, collected_keys) in visited and visited[(current_pos, collected_keys)] <= current_cost:
            continue
        visited[(current_pos, collected_keys)] = current_cost

        paths = get_paths(current_pos, walls)
        for key, paths_doors in paths.items():
            if key & collected_keys != 0:
                continue

            for doors, cost in paths_doors.items():
                if (collected_keys & doors) == doors:
                    new_collected = collected_keys | key
                    Q.append((KEYS[key], current_cost + cost, new_collected))

    return min_cost


def part_two(start, walls) -> int:
    return 2


class Mappings:
    def __init__(self):
        self._mappings = {}

    def as_bit(self, value: str):
        lower_case = value.lower()
        if lower_case not in self._mappings:
            bit_key = 1 << len(self._mappings)
            self._mappings[lower_case] = bit_key
        return self._mappings[lower_case]


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"
    data = input_path.read_text().strip()

    mappings = Mappings()
    walls = set()
    start = None

    bit_keys = {}
    ALL_KEYS = 0
    for i, line in enumerate(data.splitlines()):
        for j, c in enumerate(line):
            p = Point(i, j)

            if c.islower():
                bit_key = mappings.as_bit(c)
                KEYS[bit_key] = p
                KEY_POSES[p] = bit_key
                ALL_KEYS |= bit_key

            elif c.isupper():
                bit_key = mappings.as_bit(c)
                DOORS[bit_key] = p
                DOOR_POSES[p] = bit_key

            elif c == "#":
                walls.add(p)

            elif c == "@":
                start = p

    assert start

    print("FIRST PART", part_one(start, walls))
    # print("SECOND PART", part_two(walls, keys, doors, start))
