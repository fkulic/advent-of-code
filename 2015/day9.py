from itertools import permutations
import sys
from pathlib import Path


def part_one(distances: dict[tuple[str, str], int], cities: set[str]) -> int:
    d = []
    for c in permutations(cities):
        d_c = 0
        for i in range(1, len(c)):
            d_c += distances[(c[i - 1], c[i])]
        d.append(d_c)
    return min(d)


def part_two(distances: dict[tuple[str, str], int], cities: set[str]) -> int:
    d = []
    for c in permutations(cities):
        d_c = 0
        for i in range(1, len(c)):
            d_c += distances[(c[i - 1], c[i])]
        d.append(d_c)
    return max(d)


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"
    data = input_path.read_text().strip().splitlines()

    distances = {}
    cities = set()
    for line in data:
        a, _, b, __, d = line.split()
        cities.update({a, b})
        distances[(a, b)] = int(d)
        distances[(b, a)] = int(d)

    print("FIRST PART", part_one(distances, cities))
    print("SECOND PART", part_two(distances, cities))
