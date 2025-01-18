import sys
from collections import defaultdict, deque
from dataclasses import dataclass
from itertools import product
from pathlib import Path


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)


DIRECTIONS = [Point(-1, 0), Point(0, 1), Point(1, 0), Point(0, -1)]


class PathsCalc:
    def __init__(self, walls: set[Point], key_poses: dict[Point, int], door_poses: dict[Point, int]):
        self._path_cache = {}
        self._walls = walls
        self._key_poses = key_poses
        self._door_poses = door_poses

    def get_paths(self, start: Point) -> dict[int, dict[int, int]]:
        if start in self._path_cache:
            return self._path_cache[start]

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
                if new_p in self._walls:
                    continue

                new_doors_passed = doors_passed
                if new_p in self._door_poses:
                    new_doors_passed |= self._door_poses[new_p]

                if new_p in self._key_poses:
                    key_id = self._key_poses[new_p]
                    if new_doors_passed not in paths[key_id]:
                        paths[key_id][new_doors_passed] = cost + 1

                Q.append((new_p, cost + 1, new_doors_passed))
        self._path_cache[start] = paths
        return paths


def part_one(
    start: Point,
    walls: set[Point],
    keys: dict[int, Point],
    key_poses: dict[Point, int],
    door_poses: dict[Point, int],
) -> int:
    path_calc = PathsCalc(walls, key_poses, door_poses)
    all_keys = sum(keys)

    min_cost = sys.maxsize
    Q = deque([(start, 0, 0)])
    visited = {}
    while Q:
        current_pos, current_cost, collected_keys = Q.popleft()

        if collected_keys == all_keys:
            min_cost = min(current_cost, min_cost)
            continue

        if current_cost > min_cost:
            continue

        if (current_pos, collected_keys) in visited and visited[(current_pos, collected_keys)] <= current_cost:
            continue
        visited[(current_pos, collected_keys)] = current_cost

        paths = path_calc.get_paths(current_pos)
        for key, paths_doors in paths.items():
            if key & collected_keys != 0:
                continue

            for doors, cost in paths_doors.items():
                if (collected_keys & doors) == doors:
                    new_collected = collected_keys | key
                    Q.append((keys[key], current_cost + cost, new_collected))

    return min_cost


def transform(portals, walls):
    start = portals[0]

    walls.add(start)
    for d in DIRECTIONS:
        walls.add(start + d)

    portals = [start + p for p in [Point(-1, -1), Point(-1, 1), Point(1, -1), Point(1, 1)]]
    return portals, walls


def part_two(
    portals: list[Point],
    walls: set[Point],
    keys: dict[int, Point],
    key_poses: dict[Point, int],
    door_poses: dict[Point, int],
) -> int:
    if len(portals) == 1:
        portals, walls = transform(portals, walls)

    path_calc = PathsCalc(walls, key_poses, door_poses)
    all_keys = sum(keys)

    min_cost = sys.maxsize
    Q = deque([(portals, [0, 0, 0, 0], 0)])
    visited = {}
    while Q:
        current_positions, current_costs, collected_keys = Q.popleft()
        possible_combinations = [[(pos, 0)] for pos in current_positions]

        total_cost = sum(current_costs)
        if total_cost > min_cost:
            continue

        visited_key = tuple(current_positions), collected_keys
        if visited_key in visited and visited[visited_key] <= total_cost:
            continue
        visited[visited_key] = total_cost

        if collected_keys == all_keys:
            min_cost = min(min_cost, total_cost)
            continue

        for i in range(4):
            current_pos = current_positions[i]
            paths = path_calc.get_paths(current_pos)
            for key, paths_doors in paths.items():
                if key & collected_keys != 0:
                    continue

                for doors, cost in paths_doors.items():
                    if (collected_keys & doors) == doors:
                        possible_combinations[i].append((keys[key], cost))

        for quadrant_combinations in product(*possible_combinations):
            new_positions = []
            new_collected_keys = collected_keys
            new_costs = []

            for i, (pos, cost) in enumerate(quadrant_combinations):
                new_positions.append(pos)
                new_collected_keys |= key_poses.get(pos, 0)
                new_costs.append(current_costs[i] + cost)

            if not all(current_positions[i] == new_positions[i] for i in range(4)):
                Q.append((new_positions, new_costs, new_collected_keys))

    return min_cost


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
    portals = []
    keys, key_poses, door_poses = {}, {}, {}

    bit_keys = {}
    for i, line in enumerate(data.splitlines()):
        for j, c in enumerate(line):
            p = Point(i, j)

            if c.islower():
                bit_key = mappings.as_bit(c)
                keys[bit_key] = p
                key_poses[p] = bit_key

            elif c.isupper():
                bit_key = mappings.as_bit(c)
                door_poses[p] = bit_key

            elif c == "#":
                walls.add(p)

            elif c == "@":
                portals.append(p)

    print("FIRST PART", part_one(portals[0], walls, keys, key_poses, door_poses))
    print("SECOND PART", part_two(portals, walls, keys, key_poses, door_poses))
