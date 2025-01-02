import sys
from functools import reduce
from itertools import combinations
from operator import mul
from pathlib import Path


def split_packages(packages: set[int], n: int) -> int:
    total_sum = sum(packages)
    segment_weight = total_sum // n
    min_QE = reduce(mul, packages, 1)
    for i in range(2, len(packages) // n + 1):
        for first in combinations(packages, i):
            if sum(first) != segment_weight:
                continue
            QE = reduce(mul, first, 1)
            min_QE: int = min(min_QE, QE)
            continue

    return min_QE


def part_one(packages: set[int]) -> int:
    return split_packages(packages, 3)


def part_two(packages: set[int]) -> int:
    return split_packages(packages, 4)


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"

    input_path = Path(sys.argv[1])
    assert input_path.is_file(), "Not file"

    packages = set([int(line) for line in input_path.read_text().splitlines()])

    print("FIRST PART", part_one(packages))
    print("SECOND PART", part_two(packages))
