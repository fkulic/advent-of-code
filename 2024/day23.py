from itertools import combinations
import sys
from collections import defaultdict
from pathlib import Path


def get_interconnected(connections: dict[str, set[str]]) -> set[frozenset[str]]:
    interconnected = set()

    for k, connected in connections.items():
        if not k.startswith("t"):
            continue

        for c1 in connected:
            interconnected_kc1 = set([c1, k])
            for c2 in connected:
                if c1 == c2:
                    continue
                if all(c2 in connections.get(ickc1, []) for ickc1 in interconnected_kc1):
                    interconnected_kc1.add(c2)

            interconnected.add(frozenset(interconnected_kc1))
    return interconnected


def part_one(connections: dict[str, set[str]]) -> int:
    interconnected = get_interconnected(connections)
    three_interconnected = set()
    for ikc in interconnected:
        if len(ikc) == 3:
            three_interconnected.add(ikc)
        elif len(ikc) > 3:
            three_interconnected.update(frozenset(c) for c in combinations(ikc, 3) for e in c if e.startswith("t"))
    return len(three_interconnected)


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"

    connections = defaultdict(set)
    for line in input_path.read_text().strip().splitlines():
        a, b = line.split("-")
        connections[a].add(b)
        connections[b].add(a)

    print("FIRST PART", part_one(connections))
    # print("SECOND PART", part_two(connections))
