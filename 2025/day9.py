import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path

from shapely.geometry import Point, Polygon


def area(self, other: Point):
    return int((abs(other.x - self.x) + 1) * (abs(other.y - self.y) + 1))


def get_areas(red_tiles: list[Point]):
    areas = defaultdict(set)
    for p1, p2 in combinations(red_tiles, 2):
        areas[area(p1, p2)].add((p1, p2))
    return areas


def part_one(red_tiles: list[Point]) -> int:
    return max(get_areas(red_tiles))


def part_two(red_tiles: list[Point]) -> int:
    areas = get_areas(red_tiles)
    polygon = Polygon(red_tiles)

    for area in sorted(areas.keys(), reverse=True):
        for corner1, corner2 in areas[area]:
            p12 = Point(corner1.x, corner2.y)
            p21 = Point(corner2.x, corner1.y)
            square = Polygon([corner1, p12, corner2, p21])
            if square.within(polygon):
                return area


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    if not input_path.is_file():
        print(f"{input_path} is not a file")
        sys.exit(1)

    red_tiles = []
    for line in input_path.read_text().strip().splitlines():
        red_tiles.append(Point(*[int(x) for x in line.split(",")]))

    print("FIRST PART", part_one(red_tiles))
    print("SECOND PART", part_two(red_tiles))
