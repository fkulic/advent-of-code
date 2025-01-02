import re
import sys
from pathlib import Path


def ints_in_str(s: str) -> list[int]:
    return [int(x) for x in re.findall(r"(-?\d+)", s)]


def part_one(row: int, col: int) -> int:
    i = 0
    max = 1
    value = 20151125
    while True:
        for i in range(max, 0, -1):
            if i == row and max - i + 1 == col:
                return value
            value = value * 252533 % 33554393
            i += 1
        max += 1


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"

    input_path = Path(sys.argv[1])
    assert input_path.is_file(), "Not file"

    row, col = ints_in_str(input_path.read_text())
    print("FIRST PART", part_one(row, col))
