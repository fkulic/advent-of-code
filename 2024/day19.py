from functools import cache
import sys
from pathlib import Path


@cache
def can_be_made(design: str):
    if len(design) == 0:
        return 1

    count = 0
    for pattern in PATTERNS:
        if design.startswith(pattern):
            count += can_be_made(design[len(pattern) :])
    return count


def both_parts() -> tuple[int, int]:
    res = [can_be_made(design) for design in DESIGNS]
    return sum(1 if r > 0 else r for r in res), sum(res)


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"
    data = input_path.read_text().strip()

    PATTERNS, DESIGNS = data.split("\n\n")
    PATTERNS = PATTERNS.split(", ")
    PATTERNS.sort(key=len, reverse=True)
    DESIGNS = DESIGNS.splitlines()

    first, second = both_parts()

    print("FIRST PART", first)
    print("SECOND PART", second)
