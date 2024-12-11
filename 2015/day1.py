import sys
from pathlib import Path


def part_one(data: str) -> int:
    return data.count("(") - data.count(")")

def part_two(data: str) -> int:
    floor = 0
    for i, c in enumerate(data):
        match c:
            case "(":
                floor +=1
            case ")":
                floor -=1
        if floor == -1:
            return i + 1
    return -1


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"
    data = input_path.read_text().strip()

    print("FIRST PART", part_one(data))
    print("SECOND PART", part_two(data))
