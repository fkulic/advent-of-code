import json
import re
import sys
from pathlib import Path


def part_one(data: str) -> int:
    return sum(int(x) for x in re.findall(r"(-?\d+)", data))


def count(v) -> int # type: ignore
    if isinstance(v, str):
        return 0
    elif isinstance(v, int):
        return v
    elif isinstance(v, list):
        if len(v) == 1:
            return count(v[0])
        return count(v[0]) + count(v[1:])
    elif isinstance(v, dict):
        if "red" in v or "red" in v.values():
            return 0
        return count(list(v.values()))


def part_two(data: str) -> int:
    return count(json.loads(data))


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"
    data = input_path.read_text().strip()

    print("FIRST PART", part_one(data))
    print("SECOND PART", part_two(data))
