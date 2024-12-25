import sys
from pathlib import Path


def part_one(locks, keys) -> int:
    lock_combinations = set()
    for lock in locks:
        comb = []
        for c in range(len(lock[0])):
            comb.append(sum(1 for r in range(1, len(lock)) if lock[r][c] == "#"))
        lock_combinations.add(tuple(comb))

    key_combinations = set()
    for key in keys:
        comb = []
        for c in range(len(key[0])):
            comb.append(sum(1 for r in range(len(key) - 1) if key[r][c] == "#"))
        key_combinations.add(tuple(comb))

    key_can_fit = 0
    for lock in lock_combinations:
        for key in key_combinations:
            if len(key) != len(lock):
                continue
            if all(key[i] + lock[i] <= 5 for i in range(len(key))):
                key_can_fit += 1

    return key_can_fit


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"

    patterns = input_path.read_text().strip().split("\n\n")

    locks = []
    keys = []
    for pattern in patterns:
        if pattern[0] == "#":
            locks.append(pattern.splitlines())
        else:
            keys.append(pattern.splitlines())

    print("FIRST PART", part_one(locks, keys))
