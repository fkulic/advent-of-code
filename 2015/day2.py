import sys
from pathlib import Path


def req_paper(l: int, w: int, h: int) -> int:
    areas = [l * w, w * h, h * l]
    return min(areas) + sum(2 * a for a in areas)


def req_ribbon(l: int, w: int, h: int) -> int:
    d = [l, w, h]
    d.remove(max(l, w, h))

    return 2 * (d[0] + d[1]) + l * w * h


def part_one(data: list[int]) -> int:
    return sum(req_paper(*d) for d in data)


def part_two(data: str) -> int:
    return sum(req_ribbon(*d) for d in data)


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"

    data = [
        [int(x) for x in line.split("x")]
        for line in input_path.read_text().strip().splitlines()
    ]

    print("FIRST PART", part_one(data))
    print("SECOND PART", part_two(data))
