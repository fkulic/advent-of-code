import sys
from collections import defaultdict
from math import atan2, pi
from pathlib import Path


def find_best_asteroid(asteroids: list[tuple[int, int]]):
    best_asteroid = asteroids[0]
    max_visible = defaultdict(list)
    for a in asteroids:
        visible = defaultdict(list)
        for other in asteroids:
            if a == other:
                continue
            dx, dy = other[0] - a[0], other[1] - a[1]
            angle = atan2(dx, -dy)
            if angle < 0:
                angle += 2 * pi
            visible[angle].append(other)
        if len(visible) > len(max_visible):
            max_visible = visible
            best_asteroid = a
    return best_asteroid, max_visible


def part_one(asteroids: list[tuple[int, int]]) -> int:
    _, visible = find_best_asteroid(asteroids)
    return len(visible)


def part_two(asteroids: list[tuple[int, int]]) -> int:
    asteroid, visible = find_best_asteroid(asteroids)
    for angle in visible:
        visible[angle].sort(key=lambda p: abs(p[0] - asteroid[0]) + abs(p[1] - asteroid[1]), reverse=True)

    n = 200
    i = 1
    while i <= n:
        for angle in sorted(visible.keys()):
            if len(visible[angle]) == 0:
                continue
            last = visible[angle].pop()
            if i == n:
                return last[0] * 100 + last[1]
            i += 1
    raise Exception("Not possible")


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"

    data = input_path.read_text().splitlines()
    asteroids = []
    for i, line in enumerate(data):
        for j, c in enumerate(line):
            if c == "#":
                asteroids.append((j, i))

    print("FIRST PART", part_one(asteroids))
    print("SECOND PART", part_two(asteroids))
