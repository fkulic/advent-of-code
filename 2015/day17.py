from itertools import combinations
import sys
from pathlib import Path


def get_total_num_combinations(containers: list[int], r: int, combination_sum=150):
    return sum(1 for c in combinations(containers, r) if sum(c) == combination_sum)


def both_parts(containers: list[int]) -> tuple[int, int]:

    sum_per_r = []
    started = False
    for i in range(1, len(containers)):
        s = get_total_num_combinations(containers, i)
        if s:
            started = True
            sum_per_r.append(s)
        elif started:
            break

    return sum(sum_per_r), sum_per_r[0]


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"

    input_path = Path(sys.argv[1])
    assert input_path.is_file(), "Not file"

    containers = [int(x.strip()) for x in input_path.read_text().strip().splitlines()]

    first, second = both_parts(containers)
    print("FIRST PART", first)
    print("SECOND PART", second)
