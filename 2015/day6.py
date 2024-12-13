import sys
from pathlib import Path


def part_one(data: list[str]) -> int:
    lights = [[False for _ in range(1000)] for __ in range(1000)]

    for s in data:
        key, p1, __, p2 = s.replace("turn ", "").split()
        x1, y1 = [int(x) for x in p1.split(",")]
        x2, y2 = [int(x) for x in p2.split(",")]
        operation = None
        match key:
            case "off":
                operation = lambda x: False
            case "on":
                operation = lambda x: True
            case "toggle":
                operation = lambda x: not x
        assert operation
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                lights[i][j] = operation(lights[i][j])
    return sum(x for line in lights for x in line)


def part_two(data: list[str]) -> int:
    lights = [[0 for _ in range(1000)] for __ in range(1000)]

    for s in data:
        key, p1, __, p2 = s.replace("turn ", "").split()
        x1, y1 = [int(x) for x in p1.split(",")]
        x2, y2 = [int(x) for x in p2.split(",")]
        operation = None
        match key:
            case "off":
                operation = lambda x: x - 1 if x > 0 else 0
            case "on":
                operation = lambda x: x + 1
            case "toggle":
                operation = lambda x: x + 2
        assert operation
        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                lights[i][j] = operation(lights[i][j])
    return sum(x for line in lights for x in line)


if __name__ == "__main__":
    assert len(sys.argv) > 1, "No input path"
    input_path = Path(sys.argv[1])

    assert input_path.is_file(), "Not file"
    data = input_path.read_text().strip().splitlines()

    print("FIRST PART", part_one(data))
    print("SECOND PART", part_two(data))
