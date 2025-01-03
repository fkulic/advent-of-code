import sys
from collections import defaultdict, deque
from pathlib import Path


def part_one(orbits: dict[str, set[str]], orbiting: dict[str, str]) -> int:
    Q = deque(orbits["COM"])
    to_com = {"COM": 0}
    while Q:
        planet = Q.popleft()
        to_com[planet] = to_com[orbiting[planet]] + 1
        if o := orbits.get(planet):
            Q.extend(o)

    return sum(to_com.values())


def part_two(orbiting) -> int:
    san_orbiting = dict()
    planet = "SAN"
    dist = 0
    while planet != "COM":
        planet = orbiting[planet]
        san_orbiting[planet] = dist
        dist += 1

    planet = "YOU"
    dist = 0
    while planet not in san_orbiting:
        planet = orbiting[planet]
        dist += 1

    return dist + san_orbiting[planet] - 1


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"

    orbits = defaultdict(set)
    orbiting = {}
    for line in input_path.read_text().strip().splitlines():
        a, b = line.split(")")
        orbits[a].add(b)
        orbiting[b] = a

    print("FIRST PART", part_one(orbits, orbiting))
    print("SECOND PART", part_two(orbiting))
